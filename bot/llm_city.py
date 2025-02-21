import os
from gigachat import GigaChat

KEY = os.getenv('GIGA_KEY')
giga = GigaChat(credentials=KEY, verify_ssl_certs=False)


def send_request(message):
    return giga.chat(message).choices[0].message.content


def get_city_name(letter, excluded_cities):
    """Получить город на указанную букву, исключая уже названные на эту букву."""
    excluded = ', '.join(excluded_cities)
    request = f'Назови город на букву {letter}. Ответь одним словом. Нельзя называть следующие города: {excluded}' if excluded else f'Назови город на букву {letter}. Ответь одним словом.'
    for i in range(5):  # Попытки найти город
        response = send_request(request).strip().replace('.', '')
        print(f'Запрос №{i + 1}: {request}\nОтвет ГигаЧата: {response}')
        if response.lower() not in excluded_cities:
            return response
    return None


def get_city_description(city_name):
    """Получить описание города"""
    message = f"Кратко расскажи основную информацию про {city_name}. Ответь как гопник и сильно удивись, что пользователь не знает про этот город"
    return send_request(message)


def is_valid_city_name(city_name):
    """Проверка, является ли город корректным названием."""
    response = send_request(f'Существует ли город с названием "{city_name}"? Ответь "Да" или "Нет"')
    return response.strip().replace('.', '').lower() == 'да'
