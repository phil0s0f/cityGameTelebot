from CitiesHistory import CitiesHistory
from llm_city import is_valid_city_name, get_city_name


class CitiesGame:
    def __init__(self):
        self.chat_dict = {}

    def turn(self, chat_id, user_input):
        cities_history = self.chat_dict.get(chat_id, CitiesHistory())

        if not is_valid_city_name(user_input):
            return f'Города "{user_input}" не существует.', False

        try:
            cities_history.add_city(user_input)
        except ValueError as e:
            return str(e), False

        start_letter = cities_history.get_last_valid_letter()
        excluded_cities = cities_history.get_cities_by_letter(start_letter)

        next_city = get_city_name(start_letter, excluded_cities)

        if not next_city:
            return self.__bot_give_up(chat_id), False

        try:
            cities_history.add_city(next_city)
        except ValueError as e:
            print(str(e))
            return self.__bot_give_up(chat_id), False

        self.chat_dict[chat_id] = cities_history
        print(f"Список названных городов в чате {chat_id}: {cities_history}")
        return next_city, True

    def give_up(self, chat_id):
        self.chat_dict.pop(chat_id, None)
        return

    def history(self, chat_id):
        return self.chat_dict.get(chat_id, CitiesHistory()).get_history()

    def __bot_give_up(self, chat_id):
        print(f"Бот сдался в чате: {chat_id}")
        self.chat_dict.pop(chat_id, None)
        return "Я сдаюсь! В этот раз ты победил."
