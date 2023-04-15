from fastapi import HTTPException


class Responses:
    """класс в котором хранятся коды ответов от сервера"""

    def __init__(self):
        self.ok = (200, 'OK')
        self.unauthorized_invalid_password = HTTPException(status_code=401, detail='Unauthorized (неверный пароль)')
        self.unauthorized_invalid_login = HTTPException(status_code=401,
                                                        detail='Unauthorized (неверный логин или пользователя с таким '
                                                               'логином не существует)')
        self.unauthorized_user_exist = (401, 'Unauthorized (Пользователь с таким логином существует)')

        self.invalid_auth_scheme = HTTPException(status_code=403, detail="Invalid authentication scheme.")
        self.invalid_token = (403, "Invalid token or expired token.")
        self.invalid_auth_code = HTTPException(status_code=403, detail="Invalid authorization code.")
        self.not_found = (404, 'Not found')

        self.confilct = (409, 'Conflict (пользователь с таким логином существует)')
        self.internal_server_error = (500, 'Internal Server Error')
