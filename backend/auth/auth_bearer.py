# библиотеки
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# зависимости проекта
from auth_handler import decode_jwt
from backend.response_codes import Responses

# экземпляр класса нужен чтобы вызывать коды ошибок из Responses
server_responses = Responses()


def verify_jwt(jwtoken: str) -> bool:
    """Функция для того чтобы проверять на валидность токены которые есть у пользователей"""

    is_token_valid: bool = False

    try:
        payload = decode_jwt(jwtoken)
    except Exception:
        payload = None
    if payload:
        is_token_valid = True
    return is_token_valid


class JWTBearer(HTTPBearer):
    """Класс для обработки jwt-токенов и создания защищённых endpoint-ов
    доступ к которым будут иметь только авторизованные пользователи"""

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(server_responses.invalid_auth_scheme[0], server_responses.invalid_auth_scheme[1])
            if not verify_jwt(credentials.credentials):
                raise HTTPException(server_responses.invalid_token[0], server_responses.invalid_token[1])
            return credentials.credentials
        else:
            raise HTTPException(server_responses.invalid_auth_code[0], server_responses.invalid_auth_code[1])
