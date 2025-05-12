import pytest
import allure
import requests

class ApiPage:
    def __init__(self, url, anon_token):
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


# URL и анонимный токен
BASE_URL = "https://web-gate.chitai-gorod.ru/api/v2/search/product/"
ANON_TOKEN = "<ваш_токен>"
api = ApiPage(url=BASE_URL, anon_token=ANON_TOKEN)

@allure.story("API")
@allure.feature("Анонимный поиск")
@pytest.mark.api_positive
@pytest.mark.parametrize("search_phrase", [
    "Мастер и Маргарита",
    "Нос",
    "1984"
])
@allure.title("Анонимный поиск книги: {search_phrase}")
def test_anonymous_search(search_phrase):
    response = api.search_book(search_phrase)
    assert response.status_code == 200
    assert search_phrase.lower() in response.text.lower()


@allure.feature("Негативный поиск")
@pytest.mark.api_negative
@pytest.mark.parametrize("negative_search_phrase", [
    "+?:№?\/#№"
])
@allure.title("Негативный поиск книги: {negative_search_phrase}")
def test_negative_search(negative_search_phrase):
    response = api.search_book(negative_search_phrase)
    assert response.status_code == 400  # Ожидаем статус код 400


@allure.feature("Поиск книги со значением превышающим допустимый максимум символов")
@pytest.mark.api_negative
@pytest.mark.parametrize("negative_max_search_phrase", [
    # Убедитесь, что строка правильно закодирована или используйте обычные символы для теста.
    'a' * 256  # Пример строки превышающей допустимый максимум символов.
])
@allure.title("Негативный поиск книги: {negative_max_search_phrase}")
def test_negative_max_symbols_search(negative_max_search_phrase):
    response = api.search_book(negative_max_search_phrase)
    assert response.status_code == 400