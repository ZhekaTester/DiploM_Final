import requests
import allure


class ApiPage:
    def __init__(self, url, anon_token):  # Должен быть конструктор с параметрами
        self.url = url
        self.anon_token = anon_token
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7",
            "Authorization": f"Bearer {anon_token}",
            "Origin": "https://www.chitai-gorod.ru",
            "Referer": "https://www.chitai-gorod.ru/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }
        self.cookies = {
            "access-token": f"Bearer {anon_token}"
        }

    @allure.step("Поиск книги по фразе: {search_phrase}")
    def search_book(self, search_phrase: str):
        params = {
            "customerCityId": 213,
            "sortPreset": "relevance",
            "products[page]": 1,
            "products[per-page]": 60,
            "phrase": search_phrase
        }

        response = requests.get(
            self.url,
            headers=self.headers,
            params=params,
            cookies=self.cookies
        )

        allure.attach(
            response.text,
            name="Ответ API",
            attachment_type=allure.attachment_type.TEXT
        )

        return response

