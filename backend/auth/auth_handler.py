import time

import jwt

# импортируем все ключи и секреты для шифрования
from backend.config import SECRET as JWT_SECRET, ALGORITHM as JWT_ALGORITHM


def sign_jwt(user_id: int, user_name: str):
    """создание jwt-токена и отправка пользователю"""
    payload = {
        'user_id': user_id,
        'user_name': user_name,
        # при выдаче jwt-токена он будет валидным 3 часа после придётся пройти log in снова
        'expires_at': time.time() + 10_800
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token


def decode_jwt(token: str) -> dict:
    """функция для декодирования jwt-токенов"""
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token['expires_at'] >= time.time() else None

    except Exception as _ex:
        return {422: f'{_ex}'}
