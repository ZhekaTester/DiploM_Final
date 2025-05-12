import pytest
import allure
from page.api_page import ApiPage

# URL и анонимный токен
BASE_URL = "https://web-gate.chitai-gorod.ru/api/v2/search/product/"
ANON_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDcyMTc3MTcsImlhdCI6MTc0NzA0OTcxNywiaXNzIjoiL2FwaS92MS9hdXRoL2Fub255bW91cyIsInN1YiI6IjdlZjA2OTdhMjRlYTNmYzc4ODI2YmIyYjc5NjVlZGRhZGI1OWYzMWRhMjJjYjYxZDY1ZTY4ZDgwNjg3ZDE3Y2MiLCJ0eXBlIjoxMH0.6bqQUGSMPqaYbkEOzhtNlGBsC_ZKjayuZ0woGYhM4t8"
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
@allure.title("Поиск книги со значением превышающим допустимый максимум символов")
@pytest.mark.parametrize("negative_max_search_phrase", [
    "%D1%8D%D1%85%D1%84%D1%8D%D0%B9%D0%BF%D1%88%D0%B6%D0%B9%D1%86%D0%B9%D1%8F%D1%85%D0%B6%D1%8F%D0%B3%D1%91%D1%8D%D0%BC%D0%B1%D0%BC%D1%8E%D0%B3%D0%B7%D0%B0%D0%B1%D0%BB%D1%8E%D1%8F%D0%BC%D1%8E%D0%BF%D1%86%D1%80%D1%87%D1%8F%D1%83%D1%91%D0%B3%D1%84%D0%BC%D1%8D%D1%89%D0%B0%D1%87%D0%B9%D1%84%D0%B8%D0%BC%D0%B2%D1%85%D1%85%D0%BB%D1%83%D1%86%D0%BC%D1%83%D0%B0%D0%B2%D1%8C%D0%BB%D1%83%D0%B1%D1%88%D0%B8%D0%BB%D0%B8%D0%B9%D0%B2%D1%84%D1%84%D0%B9%D0%BE%D1%83%D1%85%D1%83%D1%83%D1%82%D0%BB%D0%B6%D0%B0%D0%BC%D0%BD%D1%91%D0%B1%D1%85%D1%8C%D0%B6%D1%8F%D0%B4%D1%85%D1%91%D0%B5%D0%BF%D1%91%D0%BA%D0%B6%D0%BA%D1%91%D0%BF%D1%85%D1%8E%D1%82%D1%8F%D1%81%D1%91%D1%8B%D0%BA%D1%8D%D1%8F%D0%BC%D0%BE%D0%BC%D1%83%D0%BE%D1%80%D0%B1%D0%B3%D0%B1%D1%87%D1%8D%D1%82%D0%B5%D0%B6%D1%8B%D0%B7%D0%B1%D0%B0%D1%88%D0%B1%D1%8F%D1%8A%D0%B5%D0%B2%D0%BF%D1%8C%D1%85%D0%B6%D0%BF%D0%B7%D1%8F%D0%B4%D0%B7%D1%82%D1%86%D0%BC%D0%BC%D1%84%D1%87%D1%8F"
])
def test_negative_max_symbols_search(negative_max_search_phrase):
    response = api.search_book(negative_max_search_phrase)
    assert response.status_code == 400

@allure.feature("Негативный поиск")
@allure.title("Негативный поиск книги с недопустимыми символами")
@pytest.mark.api_negative
@pytest.mark.parametrize("negative_invalid_search_phrase", [
    "№№№№№№№№№№№№№№№№№№№№"
])
def test_negative_invalid_symbols_search(negative_invalid_search_phrase):
    response = api.search_book(negative_invalid_search_phrase)
    assert response.status_code == 422