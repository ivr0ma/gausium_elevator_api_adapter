# Creating a WebSocket Connection

> Source: https://developer-us.gs-robot.com/en_US/Elevator%20Control%20System%20Interface%20Protocol%20V1.5/Creating%20a%20WebSocket%20Connection

# Creating a WebSocket Connection

Remarks

### Description

> Gausium establish a connection to your WebSocket service by sending a request to the /v1/connect endpoint with the accessToken.

### Request Example

```
wss://${the domain name of your service}/v1/connect?accessToken=ACCESS_TOKEN
```

Interface Description

| URL | Request Method |
| --- | --- |
| /v1/connect | WEBSOCKET |

Query

| Parameter Name | Required | Example | Remarks |
| --- | --- | --- | --- |
| accessToken |  | Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ zdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Ikpva G4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.Sfl KxwRJSMeKKF2QT4fwpMeJf36POk6yJV\_ad Qssw5c | Obtained access token |