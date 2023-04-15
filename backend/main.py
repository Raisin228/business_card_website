# библиотеки
import uvicorn
from fastapi import FastAPI, HTTPException

from auth import auth_handler
from auth.auth_handler import sign_jwt
from db.db import register_user_in_db
from db.db import user_exist_in_db
# мои импорты
from response_codes import Responses

app = FastAPI(title='business_card_website')

# экземпляр класса нужен чтобы вызывать коды ошибок из Responses
server_responses = Responses()


@app.post('/registration')
def register_user(login: str, password: str):
    """роут для регистрации пользователя в бд
    в случае ошибки возвращается код 401"""

    reg_user_in_db = register_user_in_db(login, password)

    if reg_user_in_db == -1:
        raise HTTPException(server_responses.unauthorized_user_exist[0], server_responses.unauthorized_user_exist[1])
    else:
        return {'access_token': auth_handler.sign_jwt(reg_user_in_db[3], login)}


@app.post('/login')
def login_user(login: str, password: str) -> dict:
    """вход пользователя в систему при успехе user получает новый jwt"""
    inform_user_was_reg = user_exist_in_db(login)

    # некорректный пароль
    if len(inform_user_was_reg) != 0 and inform_user_was_reg[4] != password:
        raise server_responses.unauthorized_invalid_password
    # неверный логин
    elif not inform_user_was_reg:
        raise server_responses.unauthorized_invalid_login
    # если пользователь есть в системе отсылаем ему новый jwt
    else:
        return {'status': 200, 'access_token': sign_jwt(inform_user_was_reg[3], login)}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8081, reload=True)
