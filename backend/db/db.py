import psycopg2
from fastapi import HTTPException

from backend.config import db_host, db_user, db_password, db_name
from backend.response_codes import Responses

# экземпляр класса нужен чтобы вызывать коды ошибок из Responses
server_responses = Responses()


class ConnectToDb:
    """создаём класс для подключения к бд и курсор"""

    def __init__(self):
        try:

            with psycopg2.connect(host=db_host, user=db_user, password=db_password,
                                  database=db_name) as self.connection:
                self.cursor = self.connection.cursor()
        except ConnectionError:
            print('[ERROR] Не удалось подключиться к бд возможно есть проблемы в сети')


# экземпляр класса который мы будем использовать для обращения к бд
connected_db = ConnectToDb()


def user_exist_in_db(user_login: str) -> list:
    """Функция для проверки наличия пользователя в бд
        если пользователь существует возвращается его id иначе -1"""
    try:
        connected_db.cursor.execute("SELECT * FROM users")

        for user_in_db in connected_db.cursor.fetchall():
            if user_in_db[2].lower() == user_login.lower():
                return user_in_db
    except Exception:
        return []
    return []


def register_user_in_db(newuser_login: str, newuser_password: str):
    """Функция которая записывает данные о пользователе в бд
    если пользователя с таким логином и паролем не существует"""

    # проверяем уникальность логина нового пользователя
    flag = user_exist_in_db(newuser_login)

    if flag:
        raise HTTPException(server_responses.confilct[0], server_responses.confilct[1])
    else:
        # добавляем пользователя в бд если такого же не существует
        connected_db.cursor.execute(
            f"INSERT INTO users (username, user_password) VALUES ('{newuser_login}', '{newuser_password}');"
        )
        connected_db.connection.commit()
        return user_exist_in_db(newuser_login)
