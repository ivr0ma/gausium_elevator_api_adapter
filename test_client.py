"""
Тестовый клиент, имитирующий Gausium.

Запуск:
    .venv/bin/python test_client.py

Перед запуском убедись, что сервер работает:
    .venv/bin/python main.py
"""

import asyncio
import json
import os
import time
import uuid
from pathlib import Path

import httpx
import websockets
import yaml
from dotenv import load_dotenv

load_dotenv()

BASE_HTTP = "http://localhost:8000"
BASE_WS   = "ws://localhost:8000"

CLIENT_ID     = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]

_config = yaml.safe_load((Path(__file__).parent / "config.yaml").read_text())
_first_lift = _config["lifts"][0]
LIFT_ID = _first_lift["lift_id"]
CAR_ID  = _first_lift["cars"][0]["car_id"]
SESSION  = str(uuid.uuid4())


def ts() -> int:
    return int(time.time() * 1000)


def req_id() -> str:
    return str(uuid.uuid4())


def ok(label: str, code: int) -> None:
    mark = "✓" if code == 0 else "✗"
    print(f"  {mark} {label}: code={code}")


# ---------------------------------------------------------------------------
# HTTP тесты
# ---------------------------------------------------------------------------

def test_oauth() -> str:
    print("\n[HTTP] OAuth token")

    # Неверные credentials
    r = httpx.post(f"{BASE_HTTP}/v1/oauth2/token",
                   data={"grantType": "client_credentials",
                         "clientId": "wrong", "clientSecret": "wrong"},
                   headers={"Content-Type": "application/x-www-form-urlencoded"})
    ok("неверные credentials → 401", 0 if r.status_code == 401 else 1)

    # Верные credentials
    r = httpx.post(f"{BASE_HTTP}/v1/oauth2/token",
                   data={"grantType": "client_credentials",
                         "clientId": CLIENT_ID, "clientSecret": CLIENT_SECRET},
                   headers={"Content-Type": "application/x-www-form-urlencoded"})
    ok("верные credentials → 200", 0 if r.status_code == 200 else 1)

    token = r.json()["accessToken"]
    print(f"  token: {token[:20]}...")
    return token


def test_lift_config(token: str) -> None:
    print("\n[HTTP] GET /v1/lift/config")

    # Без токена
    r = httpx.get(f"{BASE_HTTP}/v1/lift/config")
    ok("без токена → 401", 0 if r.status_code == 401 else 1)

    # Все лифты
    r = httpx.get(f"{BASE_HTTP}/v1/lift/config",
                  headers={"Authorization": f"Bearer {token}"})
    ok("все лифты", r.json()["code"])
    lifts = r.json()["data"]
    print(f"  лифтов: {len(lifts)}, первый: {lifts[0]['displayName']}")

    # Конкретный liftId
    r = httpx.get(f"{BASE_HTTP}/v1/lift/config",
                  params={"liftIds": json.dumps([LIFT_ID])},
                  headers={"Authorization": f"Bearer {token}"})
    ok(f"liftId={LIFT_ID[:8]}...", r.json()["code"])

    # Несуществующий liftId
    r = httpx.get(f"{BASE_HTTP}/v1/lift/config",
                  params={"liftIds": json.dumps(["nonexistent-id"])},
                  headers={"Authorization": f"Bearer {token}"})
    ok("несуществующий liftId → 29001", 0 if r.json()["code"] == 29001 else 1)


# ---------------------------------------------------------------------------
# WebSocket тесты
# ---------------------------------------------------------------------------

async def send_recv(ws, payload: dict) -> dict:
    await ws.send(json.dumps(payload))
    raw = await asyncio.wait_for(ws.recv(), timeout=5)
    return json.loads(raw)


async def test_websocket(token: str) -> None:
    print("\n[WebSocket] подключение")

    # Без токена
    try:
        async with websockets.connect(f"{BASE_WS}/v1/connect") as ws:
            await ws.recv()
        ok("без токена → reject", 1)
    except (websockets.exceptions.ConnectionClosedError,
            websockets.exceptions.InvalidStatus):
        ok("без токена → отклонено", 0)

    # С токеном
    url = f"{BASE_WS}/v1/connect?accessToken={token}"
    async with websockets.connect(url) as ws:
        print("  соединение установлено")

        # --- V1_RESERVE ---
        print("\n[WS] V1_RESERVE")
        resp = await send_recv(ws, {
            "sessionId": SESSION, "requestId": req_id(), "timestamp": ts(),
            "liftId": LIFT_ID, "carId": CAR_ID,
            "type": "V1_RESERVE",
            "fromAreaId": "1000", "toAreaId": "2000",
            "robotSn": "GS401-TEST-001",
        })
        ok("резервирование", resp["code"])

        # --- V1_CALL_FROM ---
        print("\n[WS] V1_CALL_FROM")
        resp = await send_recv(ws, {
            "sessionId": SESSION, "requestId": req_id(), "timestamp": ts(),
            "liftId": LIFT_ID, "carId": CAR_ID,
            "type": "V1_CALL_FROM",
            "fromAreaId": "1000", "toAreaId": "2000",
        })
        ok("вызов на этаж отправления", resp["code"])

        # --- V1_OPEN_DOOR ---
        print("\n[WS] V1_OPEN_DOOR")
        resp = await send_recv(ws, {
            "sessionId": SESSION, "requestId": req_id(), "timestamp": ts(),
            "liftId": LIFT_ID, "carId": CAR_ID,
            "areaId": "1000", "type": "V1_OPEN_DOOR", "duration": 60,
        })
        ok("держать двери открытыми", resp["code"])

        # --- V1_CALL_TO ---
        print("\n[WS] V1_CALL_TO")
        resp = await send_recv(ws, {
            "sessionId": SESSION, "requestId": req_id(), "timestamp": ts(),
            "liftId": LIFT_ID, "carId": CAR_ID,
            "type": "V1_CALL_TO",
            "fromAreaId": "1000", "toAreaId": "2000",
        })
        ok("вызов на этаж назначения", resp["code"])

        # --- V1_CLOSE_DOOR ---
        print("\n[WS] V1_CLOSE_DOOR")
        resp = await send_recv(ws, {
            "sessionId": SESSION, "requestId": req_id(), "timestamp": ts(),
            "liftId": LIFT_ID, "carId": CAR_ID,
            "areaId": "2000", "type": "V1_CLOSE_DOOR", "delay": 5,
        })
        ok("закрыть двери", resp["code"])

        # --- V1_LIFT_STATUS (подписка) ---
        print("\n[WS] V1_LIFT_STATUS (подписка)")
        resp = await send_recv(ws, {
            "sessionId": SESSION, "requestId": req_id(), "timestamp": ts(),
            "liftIds": [LIFT_ID], "type": "V1_LIFT_STATUS", "duration": 1200,
        })
        ok("подписка на статус дверей", resp["code"])

        # --- V1_LIFT_MODE (подписка) ---
        print("\n[WS] V1_LIFT_MODE (подписка)")
        resp = await send_recv(ws, {
            "sessionId": SESSION, "requestId": req_id(), "timestamp": ts(),
            "liftIds": [LIFT_ID], "type": "V1_LIFT_MODE", "duration": 1200,
        })
        ok("подписка на режим работы", resp["code"])

        # --- V1_ROBOT_STATUS ---
        print("\n[WS] V1_ROBOT_STATUS")
        for robot_status in ("WAITING", "ENTERING", "TAKING", "EXITING", "COMPLETED"):
            resp = await send_recv(ws, {
                "sessionId": SESSION, "requestId": req_id(), "timestamp": ts(),
                "liftId": LIFT_ID, "type": "V1_ROBOT_STATUS",
                "status": robot_status, "robotSn": "GS401-TEST-001",
            })
            ok(f"статус робота: {robot_status}", resp["code"])

        # --- V1_CALL_CANCEL ---
        print("\n[WS] V1_CALL_CANCEL")
        resp = await send_recv(ws, {
            "sessionId": SESSION, "requestId": req_id(), "timestamp": ts(),
            "liftId": LIFT_ID, "carId": CAR_ID,
            "type": "V1_CALL_CANCEL",
            "fromAreaId": "1000", "toAreaId": "2000",
            "reason": "COMPLETED",
        })
        ok("отмена использования лифта", resp["code"])

        # --- неизвестный тип ---
        print("\n[WS] неизвестный тип")
        resp = await send_recv(ws, {
            "sessionId": SESSION, "requestId": req_id(), "timestamp": ts(),
            "type": "V1_UNKNOWN",
        })
        ok("неизвестный type → ошибка", 0 if resp["code"] != 0 else 1)

        # --- push-тест: симулируем обновление с сервера ---
        print("\n[WS] push от сервера (симуляция)")
        from app.main import push_lift_mode, push_lift_status
        await push_lift_mode(LIFT_ID, available=False, message="FIRE")
        try:
            push_msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=2))
            ok(f"push V1_LIFT_MODE: status={push_msg.get('status')}", 0)
        except asyncio.TimeoutError:
            ok("push V1_LIFT_MODE не получен", 1)

        await push_lift_status(LIFT_ID, CAR_ID, "1000", "1", "OPENED", "UP", 60)
        try:
            push_msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=2))
            ok(f"push V1_LIFT_STATUS: status={push_msg.get('status')}", 0)
        except asyncio.TimeoutError:
            ok("push V1_LIFT_STATUS не получен", 1)


# ---------------------------------------------------------------------------

async def main() -> None:
    print("=" * 50)
    print("Gausium Elevator Adapter — тест")
    print("=" * 50)

    token = test_oauth()
    test_lift_config(token)
    await test_websocket(token)

    print("\n" + "=" * 50)
    print("Готово")


if __name__ == "__main__":
    asyncio.run(main())
