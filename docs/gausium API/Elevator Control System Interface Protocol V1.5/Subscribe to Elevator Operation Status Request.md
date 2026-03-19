# Subscribe to Elevator Operation Status Request

> Source: https://developer-us.gs-robot.com/en_US/Elevator%20Control%20System%20Interface%20Protocol%20V1.5/Subscribe%20to%20Elevator%20Operation%20Status%20Request

# Subscribe to Elevator Operation Status Request

Remarks

### Description

> Gausium sends a "Subscribe to Elevator Operation Status" request from the WebSocket client to your server. If the subscription is successful, you should return a "Subscription Successful" message and push elevator status updates whenever there is a change during the subscription period. If the subscription fails, you should return a "Subscription Failed" message.

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
	"requestId": "d6718b31-84b2-46a3-8438-898284a5f4b6",
	"timestamp": 1692448625006,
	"liftIds": ["1b3ace92-95e7-4d35-89a5-391c0ac8298e", "2b3ace92-95e7-4d35-89a5- 391c0ac82986c"],
	"type": "V1_LIFT_STATUS",
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

### Example of Door Status Push

| Parameter Name | Type | Description | Required or not | Example |
| --- | --- | --- | --- | --- |
| sessionId | string | Session unique identifier | Y | f6518b31-84b2-46a3- 8438-898284a5f7c9 |
| liftId | string | Elevator unique identifier | Y | 1b3ace92-95e7-4d35-89a5-391c0ac8298e |
| type | string | Request type | Y | V1\_LIFT\_STATUS |
| carId | string | Elevator car ID | Y | 1001010 |
| areaId | string | Area ID | Y | 1000 |
| doorId | string | Door identifier | Y | 1 |
| status | string | Door status | Y | OPENING、OPENED、 CLOSING、CLOSED |
| direction | string | The expected direction of elevator operation | Y | UP、DOWN、STOP |
| timestamp | long | Request timestamp (in millisecond) | Y | 1692448631000 |
| duration | int | Duration of door status (in second) | It’s 'Y' when the door status is OPENED | 60 |

```
{
	"sessionId": "f6518b31-84b2-46a3-8438-898284a5f7c9",
	"liftId": "1b3ace92-95e7-4d35-89a5-391c0ac8298e",
	"type": "V1_LIFT_STATUS",
	"carId": "1001010",
	"areaId": "1000",
	"doorId": "1",
	"status": "OPENED",
	"direction": "UP",
	"timestamp": 1692448631000,
	"duration": 60
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
| liftIds | array |  | Elevator unique identification array. The maximum length of the array is 100 |
| type | string |  | Request type V1\_LIFT\_STATUS |
| duration | number |  | Subscription duration (in second) |

Response Data

| Name | Type | Remarks |
| --- | --- | --- |
| code | number | Returned code |
| msg | string | Returned message |
| data | object | Request parameters |