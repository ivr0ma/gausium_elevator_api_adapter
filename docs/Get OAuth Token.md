У меня есть .env файл, в котором имеются такеи ключи: 
- ClientID
- ClientSecret
- AccessKeyID
- AccessKeySecret

### Получение токена:
```bash
curl --location 'https://openapi.gs-robot.com/gas/api/v1alpha1/oauth/token'   
--header 'Content-Type: application/json'   
--data '{  
   "grant_type":"urn:gaussian:params:oauth:grant-type:open-access-token",  
    "client_id":"{{ClientID}}",  
    "client_secret":"{{ClientSecret}}",  
    "open_access_key":"{{AccessKeySecret}}"  
}'
```

Ответ:
```bash
{
  "token_type" : "bearer",
  "access_token" : "...",
  "expires_in" : 1772804832183,
  "refresh_token" : "..."
}
```

### Обновление токена
```bash
curl --location 'https://openapi.gs-robot.com/gas/api/v1alpha1/oauth/token' 
--header 'Content-Type: application/json'
--data '{
   "grant_type":"refresh_token",
   "refresh_token":"{{refresh_token}}"
}'
```

Ответ:
```bash
{
  "token_type" : "bearer",
  "access_token" : "...",
  "expires_in" : 1772805612714,
  "refresh_token" : "..."
}
```

Тут выданные `access_token` и `refresh_token` отличаются от прошлых
