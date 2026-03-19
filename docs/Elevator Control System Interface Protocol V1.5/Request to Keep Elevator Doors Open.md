# Request to Keep Elevator Doors Open

> Source: https://developer-us.gs-robot.com/en_US/Elevator%20Control%20System%20Interface%20Protocol%20V1.5/Request%20to%20Keep%20Elevator%20Doors%20Open

# Request to Keep Elevator Doors Open

Remarks

### Description

> When the robot entering or exiting the elevator, Gausium sends a "Keep Elevator Doors Open" request from the WebSocket client to your server. If the request is successful, you should return a "Door Opening Successful" message and keep the elevator doors open. If the request fails, you should return a "Door Opening Failed" message.

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
	"requestId": "d6718b31-84b2-46a3-8438-898284a5f4b4",
	"timestamp": 1692448625004,
	"liftId": "1b3ace92-95e7-4d35-89a5-391c0ac8298e",
	"carId": "1001010",
	"areaId": "1000",
	"type": "V1_OPEN_DOOR",
	"duration": 60
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
| liftId | string |  | The unique identifier of the elevator. The operation is performed only when liftId is the same as the identifier of the elevator in the current session. |
| carId | string |  | The unique identifier of elevator car. The operation is performed only when carId is the same as the identifier of the elevator car in the current session. |
| areaId | string |  | The unique identifier of area. The operation is performed only when areaId is the same as the fromAreaId or toAreaIdin the current session. |
| type | string |  | Request type |
| duration | number |  | Door open duration (in second) |

Response Data

| Name | Type | Remarks |
| --- | --- | --- |
| code | number | Returned code |
| msg | string | Returned message |
| data | object | Request parameters |