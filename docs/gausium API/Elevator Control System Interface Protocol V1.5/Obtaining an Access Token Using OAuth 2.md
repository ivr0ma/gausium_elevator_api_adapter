# Obtaining an Access Token Using OAuth 2.0 Client Credentials Grant Flow

> Source: https://developer-us.gs-robot.com/en_US/Elevator%20Control%20System%20Interface%20Protocol%20V1.5/Obtaining%20an%20Access%20Token%20Using%20OAuth%202.0%20Client%20Credentials%20Grant%20Flow

# Obtaining an Access Token Using OAuth 2.0 Client Credentials Grant Flow

Remarks

### Description

> Your system should provide an authentication service that supports the OAuth2 authentication mechanism. Gausium obtains authorization by making a POST request to the /v1/oauth2/token endpoint with the following parameters:  
> grantType: The type of authorization, such as client\_credentials  
> clientId: The client identifier, used to uniquely identify the caller.  
> clientSecret: The client secret, used for authentication.  
> Upon successful authentication, the API returns an accessToken, which is required for accessing protected resources.

### Request Example

- CURL Command:

```
curl -X POST "https://${the domain name of your service}/oauth2/token" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "grantType=client_credentials&clientId=your_client_id&clientSecret=your_client_secret"
```

### Response Example

- Successful Response

```
{
	"accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gR G9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
	"tokenType": "Bearer",
	"expiresIn": 3600
}
```

Interface Description

| URL | Request Method |
| --- | --- |
| /v1/oauth2/token | POST |

Headers

| Name | Parameter Value | Required | Example | Remarks |
| --- | --- | --- | --- | --- |
| Content-Type | application/x-www-form-urlencoded | Yes |  |  |

Response Data

| Name | Type | Remarks |
| --- | --- | --- |
| accessToken | string | Obtained access token. (It must be the correct token, and it is necessary to ensure that subsequent interface validation is passed before normal requests can be made) |
| tokenType | string | Token type |
| expiresIn | number | Access token's expiration |