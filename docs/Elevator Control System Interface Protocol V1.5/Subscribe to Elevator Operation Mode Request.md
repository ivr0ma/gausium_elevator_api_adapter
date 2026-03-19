# Subscribe to Elevator Operation Mode Request

> Source: https://developer-us.gs-robot.com/en_US/Elevator%20Control%20System%20Interface%20Protocol%20V1.5/Subscribe%20to%20Elevator%20Operation%20Mode%20Request

# Subscribe to Elevator Operation Mode Request

Remarks

### Description

> Gausium sends a "Subscribe to Elevator Operation Mode" request from the WebSocket client to your server. If the subscription is successful, you should return a "Subscription Successful" message and push status updates whenever the elevator availability status changes during the subscription period. If the subscription fails, you should return a "Subscription Failed" message.

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
	"requestId": "d6718b31-84b2-46a3-8438-898284a5f4b7",
	"timestamp": 1692448625007,
	"liftIds": ["1b3ace92-95e7-4d35-89a5-391c0ac8298e", "2b3ace92-95e7-4d35-89a5- 391c0ac82986c"],
	"type": "V1_LIFT_MODE",
	"duration": 1200
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

### Example of Elevator Operation Mode Push

| Parameter Name | Type | Description | Required or not | Example |
| --- | --- | --- | --- | --- |
| sessionId | string | Session unique identifier | Y | f6518b31-84b2-46a3- 8438-898284a5f7c9 |
| liftId | string | Elevator unique identifier | Y | 1b3ace92-95e7-4d35-89a5-391c0ac8298e |
| type | string | Request type | Y | V1\_LIFT\_MODE |
| status | string | Elevator status | Y | AVAILABLE、 UNAVAILABLE |
| timestamp | long | Request timestamp (in millisecond) | Y | 1692448631000 |
| message | string | Elevator unavailable reason | N | FIRE |

- Elevator available

```
{
	"sessionId": "f6518b31-84b2-46a3-8438-898284a5f7c9",
	"liftId": "1b3ace92-95e7-4d35-89a5-391c0ac8298e",
	"type": "V1_LIFT_MODE",
	"status": "AVAILABLE",
	"timestamp": 1692448633000
}
```

- Elevator Unavailable

```
{
	"sessionId": "f6518b31-84b2-46a3-8438-898284a5f7c9",
	"liftId": "1b3ace92-95e7-4d35-89a5-391c0ac8298e",
	"type": "V1_LIFT_MODE",
	"status": "UNAVAILABLE",
	"timestamp": 1692448633000,
	"message": "FIRE"
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
| liftIds | array |  | Array of elevator unique identifiers. The maximum length of the array is 100 |
| type | string |  | Request type V1\_LIFT\_MODE |
| duration | number |  | Subscription duration (in second) |

Response Data

| Name | Type | Remarks |
| --- | --- | --- |
| code | number | Returned code |
| msg | string | Returned message |
| data | object | Request parameters |