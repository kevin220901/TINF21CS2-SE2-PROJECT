



CLIENT_ID_BYTELENGTH:int = 16
NETWORK_OBJECT_HEAD_SIZE_BYTES:int = 3

HOST:str = "localhost"
PORT:int = 6666

#URL_RESTAPI_BASE = 'authentication-1/'
URL_RESTAPI_BASE = 'http://auth-service:8000/'
URL_RESTAPI_LOGIN = URL_RESTAPI_BASE + 'auth/login/'
URL_RESTAPI_REGISTER = URL_RESTAPI_BASE + 'auth/register/'
URL_RESTAPI_PROFILE = URL_RESTAPI_BASE + 'auth/profile/'