"""
Gausium Elevator API Adapter
============================

Implements the Elevator Control System Interface Protocol V1.5 that the
Gausium cloud platform (robot side) expects to find on YOUR server.

Endpoints
---------
POST /v1/oauth2/token          – issue an access token (OAuth 2.0 client-credentials)
GET  /v1/lift/config           – return elevator configuration
WS   /v1/connect?accessToken=  – main WebSocket channel for all elevator commands

Usage
-----
    uvicorn app.main:app --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

import json
import logging
import os
import secrets
import time
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from fastapi import (
    FastAPI,
    Header,
    HTTPException,
    Query,
    Request,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.responses import JSONResponse

from .handlers import dispatch
from .models import (
    LiftConfigResponse,
    TokenRequest,
    TokenResponse,
    WsRequest,
)
from .state import (
    LIFTS,
    add_session,
    remove_session,
    store_token,
    token_is_valid,
)

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

app = FastAPI(
    title="Gausium Elevator API Adapter",
    description="Adapter server implementing the Gausium Elevator Control System Interface Protocol V1.5",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# Configuration (loaded from .env)
# ---------------------------------------------------------------------------

CLIENT_ID     = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
TOKEN_TTL     = int(os.getenv("TOKEN_TTL_SECONDS", "3600"))


# ---------------------------------------------------------------------------
# POST /v1/oauth2/token  — OAuth 2.0 client-credentials
# ---------------------------------------------------------------------------

@app.post("/v1/oauth2/token", response_model=TokenResponse)
async def oauth_token(request: Request) -> TokenResponse:
    """
    Gausium calls this endpoint to obtain an accessToken before opening the
    WebSocket connection.  Accepts application/x-www-form-urlencoded or JSON.
    """
    content_type = request.headers.get("content-type", "")

    if "application/x-www-form-urlencoded" in content_type:
        form = await request.form()
        grant_type    = form.get("grantType", "")
        client_id     = form.get("clientId", "")
        client_secret = form.get("clientSecret", "")
    else:
        # fall back to JSON body
        try:
            body = await request.json()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid request body")
        grant_type    = body.get("grantType", "")
        client_id     = body.get("clientId", "")
        client_secret = body.get("clientSecret", "")

    if grant_type != "client_credentials":
        raise HTTPException(status_code=400, detail="Unsupported grant_type")

    if client_id != CLIENT_ID or client_secret != CLIENT_SECRET:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client credentials",
        )

    token = secrets.token_urlsafe(48)
    store_token(token, TOKEN_TTL)

    log.info("Issued token for clientId=%s", client_id)
    return TokenResponse(accessToken=token, tokenType="Bearer", expiresIn=TOKEN_TTL)


# ---------------------------------------------------------------------------
# GET /v1/lift/config  — elevator configuration
# ---------------------------------------------------------------------------

@app.get("/v1/lift/config")
async def get_lift_config(
    requestId: Optional[str] = Query(default=None),
    timestamp: Optional[int] = Query(default=None),
    liftIds: Optional[str]   = Query(default=None),   # JSON-encoded array
    type: Optional[str]      = Query(default=None),
    authorization: Optional[str] = Header(default=None),
) -> JSONResponse:
    """
    Returns the configuration for the requested elevator IDs.
    Authorization header must contain the accessToken obtained via /v1/oauth2/token.
    """
    token = _extract_bearer(authorization)
    if not token or not token_is_valid(token):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Parse liftIds query param (URL-encoded JSON array)
    requested_ids: List[str] = []
    if liftIds:
        try:
            parsed = json.loads(liftIds)
            if isinstance(parsed, list):
                requested_ids = [str(i) for i in parsed]
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="liftIds must be a JSON array")

    if not requested_ids:
        # Return all known lifts if no filter specified
        requested_ids = list(LIFTS.keys())

    result = [LIFTS[lid].model_dump() for lid in requested_ids if lid in LIFTS]

    if not result:
        return JSONResponse(
            content={"code": 29001, "msg": "NO_LIFT_AVAILABLE",
                     "data": {"timestamp": _ts(), "requestId": requestId}}
        )

    return JSONResponse(content={"code": 0, "msg": "SUCCESS", "data": result})


# ---------------------------------------------------------------------------
# WebSocket /v1/connect
# ---------------------------------------------------------------------------

@app.websocket("/v1/connect")
async def ws_connect(websocket: WebSocket, accessToken: Optional[str] = Query(default=None)):
    """
    Main WebSocket endpoint.  Gausium connects here after obtaining a token.
    All elevator commands arrive as JSON messages routed by the `type` field.
    """
    # --- authentication ---
    if not accessToken or not token_is_valid(accessToken):
        await websocket.close(code=4001, reason="Invalid or expired token")
        return

    await websocket.accept()

    # Generate a server-side session id (Gausium sends its own sessionId per
    # message; we keep a per-connection session for subscription tracking).
    import uuid
    conn_id = str(uuid.uuid4())
    session = add_session(conn_id, websocket)
    log.info("WebSocket connected: conn_id=%s", conn_id)

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                payload: Dict[str, Any] = json.loads(raw)
            except json.JSONDecodeError:
                await _send(websocket, {"code": 40000, "msg": "INVALID_JSON", "data": {}})
                continue

            log.debug("← %s", payload)

            try:
                req = WsRequest.model_validate(payload)
            except Exception as exc:
                await _send(websocket, {"code": 40001, "msg": f"BAD_REQUEST: {exc}", "data": {}})
                continue

            response = dispatch(req, session)
            log.debug("→ %s", response)
            await _send(websocket, response)

    except WebSocketDisconnect:
        log.info("WebSocket disconnected: conn_id=%s", conn_id)
    finally:
        remove_session(conn_id)


# ---------------------------------------------------------------------------
# Push helpers (call from your elevator integration layer)
# ---------------------------------------------------------------------------

async def push_lift_mode(lift_id: str, available: bool, message: Optional[str] = None) -> None:
    """
    Push an elevator availability change to all sessions subscribed to mode
    updates for the given lift_id.

    Call this from your elevator control integration whenever the elevator
    availability status changes.
    """
    from .state import sessions_subscribed_to_mode

    payload: Dict[str, Any] = {
        "type": "V1_LIFT_MODE",
        "liftId": lift_id,
        "status": "AVAILABLE" if available else "UNAVAILABLE",
        "timestamp": _ts(),
    }
    if message:
        payload["message"] = message

    for sess in sessions_subscribed_to_mode(lift_id):
        payload["sessionId"] = sess.session_id
        await _send(sess.websocket, payload)


async def push_lift_status(
    lift_id: str,
    car_id: str,
    area_id: str,
    door_id: str,
    door_status: str,   # OPENING | OPENED | CLOSING | CLOSED
    direction: str,     # UP | DOWN | STOP
    duration: Optional[int] = None,
) -> None:
    """
    Push a door/status change to all sessions subscribed to status updates
    for the given lift_id.

    Call this from your elevator control integration whenever door state changes.
    """
    from .state import sessions_subscribed_to_status

    payload: Dict[str, Any] = {
        "type": "V1_LIFT_STATUS",
        "liftId": lift_id,
        "carId": car_id,
        "areaId": area_id,
        "doorId": door_id,
        "status": door_status,
        "direction": direction,
        "timestamp": _ts(),
    }
    if duration is not None:
        payload["duration"] = duration

    for sess in sessions_subscribed_to_status(lift_id):
        payload["sessionId"] = sess.session_id
        await _send(sess.websocket, payload)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

async def _send(ws: WebSocket, payload: Dict[str, Any]) -> None:
    try:
        await ws.send_text(json.dumps(payload, ensure_ascii=False))
    except Exception as exc:
        log.warning("Failed to send message: %s", exc)


def _extract_bearer(authorization: Optional[str]) -> Optional[str]:
    if not authorization:
        return None
    parts = authorization.split(" ", 1)
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return authorization  # allow raw token as fallback


def _ts() -> int:
    return int(time.time() * 1000)
