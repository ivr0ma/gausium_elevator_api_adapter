"""
Handlers for each WebSocket command type sent by Gausium.

Every handler receives a parsed WsRequest and the active Session, and returns
a WsResponse dict ready to be JSON-serialised and sent back over the socket.

Replace the stub logic (success/fail decisions) with calls to your real
elevator control system.
"""

from __future__ import annotations

import time
from typing import Any, Dict

from .models import WsRequest, WsResponse, WsResponseData
from .state import LIFTS, Session

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ts() -> int:
    return int(time.time() * 1000)


def _ok(req: WsRequest) -> Dict[str, Any]:
    return WsResponse(
        code=0,
        msg="SUCCESS",
        data=WsResponseData(
            timestamp=_ts(),
            sessionId=req.sessionId,
            requestId=req.requestId,
        ).model_dump(),
    ).model_dump()


def _err(code: int, msg: str, req: WsRequest) -> Dict[str, Any]:
    return WsResponse(
        code=code,
        msg=msg,
        data=WsResponseData(
            timestamp=_ts(),
            sessionId=req.sessionId,
            requestId=req.requestId,
        ).model_dump(),
    ).model_dump()


def _lift_exists(lift_id: str | None) -> bool:
    return lift_id is not None and lift_id in LIFTS


# ---------------------------------------------------------------------------
# V1_RESERVE — Elevator Reservation
# ---------------------------------------------------------------------------

def handle_reserve(req: WsRequest, session: Session) -> Dict[str, Any]:
    if not _lift_exists(req.liftId):
        return _err(29001, "NO_LIFT_AVAILABLE", req)

    # TODO: check capacity / conflicts with real system
    # Return 29008 / LIFT_FULLY_RESERVED if all cars are taken.

    return _ok(req)


# ---------------------------------------------------------------------------
# V1_CALL_FROM — Call elevator to departure area
# ---------------------------------------------------------------------------

def handle_call_from(req: WsRequest, session: Session) -> Dict[str, Any]:
    if not _lift_exists(req.liftId):
        return _err(29001, "NO_LIFT_AVAILABLE", req)

    # TODO: instruct elevator to go to req.fromAreaId

    return _ok(req)


# ---------------------------------------------------------------------------
# V1_CALL_TO — Call elevator to destination area
# ---------------------------------------------------------------------------

def handle_call_to(req: WsRequest, session: Session) -> Dict[str, Any]:
    if not _lift_exists(req.liftId):
        return _err(29001, "NO_LIFT_AVAILABLE", req)

    # TODO: instruct elevator to go to req.toAreaId

    return _ok(req)


# ---------------------------------------------------------------------------
# V1_CALL_CANCEL — Cancel elevator usage
# ---------------------------------------------------------------------------

def handle_cancel(req: WsRequest, session: Session) -> Dict[str, Any]:
    if not _lift_exists(req.liftId):
        return _err(29001, "NO_LIFT_AVAILABLE", req)

    # TODO: release reservation in real system (reason: COMPLETED | TERMINATED)

    return _ok(req)


# ---------------------------------------------------------------------------
# V1_OPEN_DOOR — Keep elevator doors open
# ---------------------------------------------------------------------------

def handle_open_door(req: WsRequest, session: Session) -> Dict[str, Any]:
    if not _lift_exists(req.liftId):
        return _err(29001, "NO_LIFT_AVAILABLE", req)

    # TODO: send "hold open for req.duration seconds" to elevator

    return _ok(req)


# ---------------------------------------------------------------------------
# V1_CLOSE_DOOR — Close elevator doors
# ---------------------------------------------------------------------------

def handle_close_door(req: WsRequest, session: Session) -> Dict[str, Any]:
    if not _lift_exists(req.liftId):
        return _err(29001, "NO_LIFT_AVAILABLE", req)

    # TODO: send "close door after req.delay seconds" to elevator

    return _ok(req)


# ---------------------------------------------------------------------------
# V1_LIFT_MODE — Subscribe to elevator operation mode
# ---------------------------------------------------------------------------

def handle_lift_mode_subscribe(req: WsRequest, session: Session) -> Dict[str, Any]:
    lift_ids = req.liftIds or ([req.liftId] if req.liftId else [])
    if not lift_ids:
        return _err(29001, "NO_LIFT_AVAILABLE", req)

    unknown = [lid for lid in lift_ids if lid not in LIFTS]
    if unknown:
        return _err(29001, "NO_LIFT_AVAILABLE", req)

    for lid in lift_ids:
        session.mode_sub_lifts.add(lid)

    # TODO: schedule unsubscribe after req.duration seconds if needed

    return _ok(req)


# ---------------------------------------------------------------------------
# V1_LIFT_STATUS — Subscribe to elevator operation status
# ---------------------------------------------------------------------------

def handle_lift_status_subscribe(req: WsRequest, session: Session) -> Dict[str, Any]:
    lift_ids = req.liftIds or ([req.liftId] if req.liftId else [])
    if not lift_ids:
        return _err(29001, "NO_LIFT_AVAILABLE", req)

    unknown = [lid for lid in lift_ids if lid not in LIFTS]
    if unknown:
        return _err(29001, "NO_LIFT_AVAILABLE", req)

    for lid in lift_ids:
        session.status_sub_lifts.add(lid)

    # TODO: schedule unsubscribe after req.duration seconds if needed

    return _ok(req)


# ---------------------------------------------------------------------------
# V1_ROBOT_STATUS — Upload robot elevator status
# ---------------------------------------------------------------------------

def handle_robot_status(req: WsRequest, session: Session) -> Dict[str, Any]:
    if not _lift_exists(req.liftId):
        return _err(29001, "NO_LIFT_AVAILABLE", req)

    # TODO: record robot status in your system
    # req.status: WAITING | ENTERING | TAKING | EXITING | COMPLETED | FAILED
    # req.reason: TIMEOUT | STOP (only on terminal states)
    # req.robotSn: robot serial number

    return _ok(req)


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

HANDLERS = {
    "V1_RESERVE":      handle_reserve,
    "V1_CALL_FROM":    handle_call_from,
    "V1_CALL_TO":      handle_call_to,
    "V1_CALL_CANCEL":  handle_cancel,
    "V1_OPEN_DOOR":    handle_open_door,
    "V1_CLOSE_DOOR":   handle_close_door,
    "V1_LIFT_MODE":    handle_lift_mode_subscribe,
    "V1_LIFT_STATUS":  handle_lift_status_subscribe,
    "V1_ROBOT_STATUS": handle_robot_status,
}


def dispatch(req: WsRequest, session: Session) -> Dict[str, Any]:
    handler = HANDLERS.get(req.type)
    if handler is None:
        return _err(40000, f"UNKNOWN_TYPE: {req.type}", req)
    return handler(req, session)
