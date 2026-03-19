# Cancel Elevator Usage

> Source: https://developer-us.gs-robot.com/en_US/Elevator%20Control%20System%20Interface%20Protocol%20V1.5/Cancel%20Elevator%20Usage

# Cancel Elevator Usage

Remarks

### Description

> When the robot completes or terminates elevator usage, Gausium sends a "Cancel Elevator Usage" request from the WebSocket client to your server. If the cancellation is successful, you should return a "Cancellation Successful" message; if the cancellation fails, you should return a "Cancellation Failed" message.

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
	"requestId": "d6718b31-84b2-46a3-8438-898284a5f4b3",
	"timestamp": 1692448625003,
	"liftId": "1b3ace92-95e7-4d35-89a5-391c0ac8298e",
	"carId": "1001010",
	"type": "V1_CALL_CANCEL",
	"fromAreaId": "1000",
	"toAreaId": "2000",
	"reason": "COMPLETED"
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

- Error response for lift not reserved.

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
| carId | string |  | Elevator car identifier |
| type | string |  | Request type |
| fromAreaId | string |  | Departure area identifier |
| toAreaId | string |  | Destination area identifier |
| reason | string |  | Reason for cancellation Completed: COMPLETED Terminated: TERMINATED |

Response Data

| Name | Type | Remarks |
| --- | --- | --- |
| code | number | Returned code |
| msg | string | Returned information |
| data | object | Request Parameters |