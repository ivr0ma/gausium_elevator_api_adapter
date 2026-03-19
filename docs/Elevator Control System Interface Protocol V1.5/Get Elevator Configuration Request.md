# Get Elevator Configuration Request

> Source: https://developer-us.gs-robot.com/en_US/Elevator%20Control%20System%20Interface%20Protocol%20V1.5/Get%20Elevator%20Configuration%20Request

# Get Elevator Configuration Request

Remarks

### Description

> You provide a list of elevator IDs, and Gausium queries and retrieves the elevator configuration information through this interface.

### Error Codes

| Code | Description | Message |
| --- | --- | --- |
| 0 | OK | Operation completed successfully |
| 29001 | NO\_LIFT\_AVAILABLE | Elevator is unavailable |

### Request Example

- CURL Command:

```
curl --location --globoff 'https://${the domain name of your service}/v1/lift/config?requestId=d6718b31-84b2-46a3-8438-898284a5f4b7&timestamp=1692448625007&liftIds=[%221b3ace92-95e7-4d35-89a5-391c0ac8298e%22%2C%222b3ace92-95e7-4d35-89a5-391c0ac82986c%22]&type=V1_LIFT_CONFIG' \
--header 'authorization: ${accessToken}'
```

### Response Example

- Successful Response

```
{
	"code": 0,
	"msg": "SUCCESS",
	"data": [{
		"liftId": "d6718b31-84b2-46a3-8438-898284a5f4b7",
		"displayName": "电梯1",
		"destinations": [{
				"areaId": "1000",
				"floorId": "1",
				"displayName": "-1F",
				"doorId": 1
			},
			{
				"areaId": "2000",
				"floorId": "2",
				"displayName": "11F",
				"doorId": 1
			},
			{
				"areaId": "3000",
				"floorId": "3",
				"displayName": "2F",
				"doorId": 2
			}
		],
		"cars": [{
				"carId": "1001010",
				"doors": [1, 2]
			},
			{
				"carId": "1001011",
				"doors": [1, 2]
			}
		]
	}]
}
```

- Error response for no lift available

```
{
	"code": 29001,
	"msg": "NO_LIFT_AVAILABLE",
	"data": {
		"timestamp": 1692448632000,
		"requestId": "d6718b31-84b2-46a3-8438-898284a5f4b7"
	}
}
```

Interface Description

| URL | Request Method |
| --- | --- |
| /v1/lift/config | GET |

Query

| Parameter Name | Required | Example | Remarks |
| --- | --- | --- | --- |
| requestId |  |  | Request unique identifier |
| timestamp |  |  | Request timestamp (in millisecond) |
| liftIds |  |  | Array of elevator unique identifiers. The maximum length of the array is 100 |
| type |  |  | Request type |

Response Data

| Name | Type | Remarks |
| --- | --- | --- |
| code | number | Returned code |
| msg | string | Returned message |
| data | array | Elevator configuration |