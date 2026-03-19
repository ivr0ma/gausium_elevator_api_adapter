from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


# ---------------------------------------------------------------------------
# OAuth
# ---------------------------------------------------------------------------

class TokenRequest(BaseModel):
    grantType: str
    clientId: str
    clientSecret: str


class TokenResponse(BaseModel):
    accessToken: str
    tokenType: str = "Bearer"
    expiresIn: int = 3600


# ---------------------------------------------------------------------------
# WebSocket messages (requests from Gausium)
# ---------------------------------------------------------------------------

class WsRequest(BaseModel):
    """Generic envelope for all WebSocket commands from Gausium."""
    sessionId: Optional[str] = None
    requestId: Optional[str] = None
    timestamp: Optional[int] = None
    type: str

    # elevator ids
    liftId: Optional[str] = None
    liftIds: Optional[List[str]] = None
    carId: Optional[str] = None

    # area ids
    fromAreaId: Optional[str] = None
    toAreaId: Optional[str] = None
    areaId: Optional[str] = None

    # door controls
    duration: Optional[int] = None   # open duration / subscription duration (seconds)
    delay: Optional[int] = None      # close delay (seconds)

    # cancellation / robot status
    reason: Optional[str] = None
    status: Optional[str] = None
    robotSn: Optional[str] = None


# ---------------------------------------------------------------------------
# WebSocket responses (sent back to Gausium)
# ---------------------------------------------------------------------------

class WsResponseData(BaseModel):
    timestamp: int
    sessionId: Optional[str] = None
    requestId: Optional[str] = None


class WsResponse(BaseModel):
    code: int
    msg: str
    data: Any


# ---------------------------------------------------------------------------
# HTTP: GET /v1/lift/config
# ---------------------------------------------------------------------------

class LiftDestination(BaseModel):
    areaId: str
    floorId: str
    displayName: str
    doorId: int


class LiftCar(BaseModel):
    carId: str
    doors: List[int]


class LiftConfig(BaseModel):
    liftId: str
    displayName: str
    destinations: List[LiftDestination]
    cars: List[LiftCar]


class LiftConfigResponse(BaseModel):
    code: int
    msg: str
    data: Any


# ---------------------------------------------------------------------------
# Push payloads (server → Gausium via WebSocket)
# ---------------------------------------------------------------------------

class LiftModePush(BaseModel):
    sessionId: str
    liftId: str
    type: str = "V1_LIFT_MODE"
    status: str          # AVAILABLE | UNAVAILABLE
    timestamp: int
    message: Optional[str] = None


class LiftStatusPush(BaseModel):
    sessionId: str
    liftId: str
    type: str = "V1_LIFT_STATUS"
    carId: str
    areaId: str
    doorId: str
    status: str          # OPENING | OPENED | CLOSING | CLOSED
    direction: str       # UP | DOWN | STOP
    timestamp: int
    duration: Optional[int] = None
