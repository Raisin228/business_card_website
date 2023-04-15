# библиотеки
import uvicorn
from fastapi import FastAPI, HTTPException

from auth import auth_handler
from db.db import register_user_in_db
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8081, reload=True)