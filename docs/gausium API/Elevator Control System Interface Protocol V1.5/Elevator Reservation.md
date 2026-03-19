# Elevator Reservation

> Source: https://developer-us.gs-robot.com/en_US/Elevator%20Control%20System%20Interface%20Protocol%20V1.5/Elevator%20Reservation

# Elevator Reservation

Remarks

### Description

> Gausium sends a Lift reserve request from the WebSocket client to your server. If the reservation is successful, you should return a "Reservation Successful" message. If the reservation fails, you should return a "Reservation Exception" message.

### Error Codes

| Code | Description | Message |
| --- | --- | --- |
| 0 | OK | Operation completed successfully |
| 29001 | NO\_LIFT\_AVAILABLE | Elevator is unavailable |
| 29008 | LIFT\_FULLY\_RESERVED | Elevator is fully reserved. Robot will pause 1 minute before making a request |

### Request Example

```
{
	"sessionId": "f6518b31-84b2-46a3-8438-898284a5f7c9",
	"requestId": "d6718b31-84b2-46a3-8438-898284a5f4b1",
	"timestamp": 1692448625000,
	"liftId": "1b3ace92-95e7-4d35-89a5-391c0ac8298e",
	"carId": "1001010",
	"type": "V1_RESERVE",
	"fromAreaId": "1000",
	"toAreaId": "2000",
        "robotSn": "GS401-6190-T2R-XXXX"
}
```

### Response Example

- Successful Response

```
{
	"code": 0,
	"msg": "SUCCESS",
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

- Error response for fully reserved Lift.

```
{
	"code": 29008,
	"msg": " LIFT_FULLY_RESERVED",
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
| robotSn | string |  | Robot sn |

Response Data

| Name | Type | Remarks |
| --- | --- | --- |
| code | number | Returned code |
| msg | string | Returned information |
| data | object | Request Parameters |