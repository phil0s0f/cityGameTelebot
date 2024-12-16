# CitiesHistory.py
class CitiesHistory:
    def __init__(self):
        self.city_list = []
        self.not_valid_letter_list = ('ь', 'ъ', 'ы', 'й')
        # self.current_letter = ''

    def add_city(self, city_name):
        city_name_lower = city_name.lower()
        if self.city_list:
            if city_name_lower in self.city_list:
                raise ValueError(f"Город '{city_name}' уже был.")

            if self.get_last_valid_letter() != city_name_lower[0]:
                raise ValueError(f"Город '{city_name}' должен начинаться на последнюю букву предыдущего города.")

        self.city_list.append(city_name_lower)
        return True

    def __contains__(self, city_name):
        return city_name.lower() in self.city_list

    def __str__(self):
        return ', '.join(self.city_list)

    def contains(self, city_name):
        return city_name.lower() in self.city_list

    def get_cities_by_letter(self, start_letter):
        return [city for city in self.city_list if city[0] == start_letter.lower()]

    def get_last_valid_letter(self):
        for letter in reversed(self.city_list[-1]):
            if letter not in self.not_valid_letter_list:
                return letter
        return None

    def __len__(self):
        return len(self.city_list)

    def get_count_cities(self):
        return len(self.city_list)

    def get_history(self):
        result = [f"{self.city_list[i]}-{self.city_list[i + 1] if i + 1 < len(self) else ''}"
                  for i in range(0, len(self), 2)]
        return "\n".join(result)


if __name__ == '__main__':
    cities_history = CitiesHistory()
    print(cities_history.add_city('Москва'))
    print(cities_history.get_last_valid_letter())
    print(cities_history.add_city('Москва'))
    print(cities_history.add_city('Дубай'))
    print(cities_history.add_city('Астрахань'))
    print(cities_history.get_cities_by_letter('М'))
    print(cities_history.get_cities_by_letter('М'))
    print('Москва' in cities_history)
    print(cities_history.contains('Улан-Удэ'))
    print(cities_history.get_last_valid_letter())
