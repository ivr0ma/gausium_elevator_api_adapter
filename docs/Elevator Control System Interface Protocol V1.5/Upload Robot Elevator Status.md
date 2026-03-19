# Upload Robot Elevator Status

> Source: https://developer-us.gs-robot.com/en_US/Elevator%20Control%20System%20Interface%20Protocol%20V1.5/Upload%20Robot%20Elevator%20Status

# Upload Robot Elevator Status

Remarks

### Description

> Gausium sends this request to your server via the WebSocket client when there is a change in the robot's elevator riding status, informing the server of the robot's current elevator riding status.

### Error Codes

| Code | Description | Message |
| --- | --- | --- |
| 0 | OK | Operation completed successfully |
| 29001 | NO\_LIFT\_AVAILABLE | Elevator is unavailable |
| 29009 | LIFT\_NOT\_RESERVED | Elevator cannot be used without reservation |

### Request Example

```
{
        "sessionId": "f6518b31-84b2-46a3-8438-898284a5f7c9",
        "requestId":"d6718b31-84b2-46a3-8438-898284a5f4b7",
        "timestamp":1692448625007,
        "liftId":"1b3ace92-95e7-4d35-89a5-391c0ac8298e",
        "type":"V1_ROBOT_STATUS",
        "status": "WAITING",
        "reason": "TASK_TIMEOUT",
        "robotSn": "GS401-6190-T2R-XXXX"
}
```

### Response Example

- Successful Response

```
{
	"code": 0,
	"msg": " SUCCESS",
	"data": {
		"timestamp": 1692448632000,
		"sessionId": "f6518b31-84b2-46a3-8438-898284a5f7c9",
		"requestId": "d6718b31-84b2-46a3-8438-898284a5f4b7"
	}
}
```

- Error response for no lift available

```
{
	"code": 29001,
	"msg": " NO_LIFT_AVAILABLE",
	"data": {
		"timestamp": 1692448632000,
		"sessionId": "f6518b31-84b2-46a3-8438-898284a5f7c9",
		"requestId": "d6718b31-84b2-46a3-8438-898284a5f4b7"
	}
}
```

- Error response for lift not reserved

```
{
	"code": 29009,
	"msg": " LIFT_NOT_RESERVED",
	"data": {
		"timestamp": 1692448632000,
		"sessionId": "f6518b31-84b2-46a3-8438-898284a5f7c9",
		"requestId": "d6718b31-84b2-46a3-8438-898284a5f4b7"
	}
}
```

Interface Description

| URL | Request Method |
| --- | --- |
| /v1/connect | WEBSOCKET |

Headers

| Name | Parameter Value | Required | Example | Remarks |
| --- | --- | --- | --- | --- |
| Content-Type | application/json | Yes |  |  |

Body

| Name | Type | Required | Remarks |
| --- | --- | --- | --- |
| sessionId | string |  | Session unique identifier |
| requestId | string |  | Request unique identifier |
| timestamp | number |  | Request timestamp (in millisecond) |
| liftId | string |  | Elevator unique identifier |
| type | string |  | Request typeV1\_ROBOT\_STATUS |
| status | string |  | Robot Elevator Riding Status WAITING：waiting the elevator ENTERING：entering the elevator TAKING：taking the elevator EXITING：exiting the elevator COMPLETED：Elevator ride completed FAILED：Elevator ride failed |
| reason | string |  | Reason for end state TIMEOUT STOP |
| robotSn | string |  | GS401-6190-T2R-XXXX |

Response Data

| Name | Type | Remarks |
| --- | --- | --- |
| code | number | Returned code |
| msg | string | Returned message |
| data | object | Request parameters |