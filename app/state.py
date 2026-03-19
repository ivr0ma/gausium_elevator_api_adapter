"""
In-memory state for sessions, tokens, subscriptions and (stub) elevator data.

Replace / extend the elevator data and subscription push logic to integrate
with your real elevator control system.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import yaml
from fastapi import WebSocket

from .models import LiftCar, LiftConfig, LiftDestination


# ---------------------------------------------------------------------------
# Elevator catalogue — loaded from config.yaml
# ---------------------------------------------------------------------------

def _load_lifts() -> Dict[str, LiftConfig]:
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path) as f:
        data = yaml.safe_load(f)

    result: Dict[str, LiftConfig] = {}
    for lift in data["lifts"]:
        lift_id = lift["lift_id"]
        result[lift_id] = LiftConfig(
            liftId=lift_id,
            displayName=lift["display_name"],
            destinations=[
                LiftDestination(
                    areaId=d["area_id"],
                    floorId=d["floor_id"],
                    displayName=d["display_name"],
                    doorId=d["door_id"],
                )
                for d in lift["destinations"]
            ],
            cars=[
                LiftCar(carId=c["car_id"], doors=c["doors"])
                for c in lift["cars"]
            ],
        )
    return result


LIFTS: Dict[str, LiftConfig] = _load_lifts()


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
