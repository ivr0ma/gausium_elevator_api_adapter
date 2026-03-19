"""
In-memory state for sessions, tokens, subscriptions and (stub) elevator data.

Replace / extend the elevator data and subscription push logic to integrate
with your real elevator control system.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

from fastapi import WebSocket

from .models import LiftCar, LiftConfig, LiftDestination


# ---------------------------------------------------------------------------
# Stub elevator catalogue
# ---------------------------------------------------------------------------
# Populate this with real data or load from a database / config file.

LIFTS: Dict[str, LiftConfig] = {
    "1b3ace92-95e7-4d35-89a5-391c0ac8298e": LiftConfig(
        liftId="1b3ace92-95e7-4d35-89a5-391c0ac8298e",
        displayName="Elevator 1",
        destinations=[
            LiftDestination(areaId="1000", floorId="1", displayName="1F", doorId=1),
            LiftDestination(areaId="2000", floorId="2", displayName="2F", doorId=1),
            LiftDestination(areaId="3000", floorId="3", displayName="3F", doorId=2),
        ],
        cars=[
            LiftCar(carId="1001010", doors=[1, 2]),
            LiftCar(carId="1001011", doors=[1, 2]),
        ],
    ),
}


# ---------------------------------------------------------------------------
# Active OAuth tokens  {token_string: expiry_unix_ms}
# ---------------------------------------------------------------------------

_tokens: Dict[str, int] = {}


def store_token(token: str, expires_in_seconds: int = 3600) -> None:
    _tokens[token] = int(time.time() * 1000) + expires_in_seconds * 1000


def token_is_valid(token: str) -> bool:
    expiry = _tokens.get(token)
    if expiry is None:
        return False
    return int(time.time() * 1000) < expiry


# ---------------------------------------------------------------------------
# WebSocket session registry
# ---------------------------------------------------------------------------

@dataclass
class Session:
    session_id: str
    websocket: WebSocket
    # liftIds subscribed for mode changes
    mode_sub_lifts: Set[str] = field(default_factory=set)
    # liftIds subscribed for status changes
    status_sub_lifts: Set[str] = field(default_factory=set)


_sessions: Dict[str, Session] = {}


def add_session(session_id: str, ws: WebSocket) -> Session:
    session = Session(session_id=session_id, websocket=ws)
    _sessions[session_id] = session
    return session


def get_session(session_id: str) -> Optional[Session]:
    return _sessions.get(session_id)


def remove_session(session_id: str) -> None:
    _sessions.pop(session_id, None)


def sessions_subscribed_to_mode(lift_id: str) -> List[Session]:
    return [s for s in _sessions.values() if lift_id in s.mode_sub_lifts]


def sessions_subscribed_to_status(lift_id: str) -> List[Session]:
    return [s for s in _sessions.values() if lift_id in s.status_sub_lifts]
