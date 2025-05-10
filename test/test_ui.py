import time
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.config import Config
from config.test_data import TestData


@allure.feature("Авторизация")
@allure.story("Изменение цвета кнопки при вводе телефона")
def test_button_color_change_on_phone_input(driver):
    try:
        # 1. Открытие страницы и переход к форме авторизации
        driver.get(Config.BASE_URL)
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.header-controls__text'))).click()

        # 2. Получение элементов
        button = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#tid-form > button")))
        phone_input = driver.find_element(By.CSS_SELECTOR, "input[type='tel']")

        # 3. Запоминаем исходный цвет кнопки
        initial_color = button.value_of_css_property("background-color")

        # 4. Вводим номер телефона
        phone_input.send_keys(TestData.TEST_PHONE)

        # 5. Ожидаем изменение цвета кнопки
        WebDriverWait(driver, 10).until(
            lambda _: button.value_of_css_property("background-color") != initial_color)

        # 6. Проверяем изменение цвета
        new_color = button.value_of_css_property("background-color")
        assert new_color != initial_color, "Цвет кнопки должен измениться после ввода телефона"
    except Exception as e:
        driver.save_screenshot("button_color_error.png")
        pytest.fail(f"Тест не пройден: {str(e)}")


@allure.feature("Поиск")
@allure.story("Поиск несуществующего товара")
def test_search_nonexistent_item(driver):
    try:
        with allure.step("1. Открыть главную страницу"):
            driver.get(Config.BASE_URL)

        with allure.step("2. Ввести несуществующий запрос"):
            search_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input.search-form__input')))
            search_input.send_keys(TestData.INVALID_SEARCH_PHRASE)

            with allure.step("3. Нажать кнопку поиска"):
                search_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
            search_button.click()

            with allure.step("4. Проверить сообщение об отсутствии результатов"):
                result_element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.catalog-stub__content h4')))
            assert "Похоже, у нас такого нет" in result_element.text
    except Exception as e:
        driver.save_screenshot("search_error.png")
        pytest.fail(f"Тест не пройден: {str(e)}")


@allure.feature("Геолокация")
@allure.story("Смена города на Санкт-Петербург")
def test_change_city_to_spb(driver):
    try:
        with allure.step("1. Открыть главную страницу"):
            driver.get(Config.BASE_URL)
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body')))
            allure.attach(driver.get_screenshot_as_png(),
                          name="main_page_loaded",
                          attachment_type=allure.attachment_type.PNG)

        with allure.step("2. Закрыть мешающие элементы (куки, баннеры)"):
            try:
                cookie_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(., "Принять куки")]')))
                cookie_btn.click()
                # Ожидаем исчезновение куки-баннера
                WebDriverWait(driver, 5).until(
                    EC.invisibility_of_element_located((By.XPATH, '//button[contains(., "Принять куки")]')))
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(),
                              name="cookie_button_not_found",
                              attachment_type=allure.attachment_type.PNG)
                pass

        with allure.step("3. Нажать кнопку изменения города"):
            city_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Изменить город")]')))
            city_btn.click()
            # Ожидаем появление попапа выбора города
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder*="город"]')))
            allure.attach(driver.get_screenshot_as_png(),
                          name="city_popup_opened",
                          attachment_type=allure.attachment_type.PNG)

        with allure.step("4. Ввести 'Санкт-Петербург' в поиск"):
            search_input = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder*="город"]')))
            search_input.clear()
            search_input.send_keys(TestData.SPB_CITY)
            # Ожидаем появление результатов поиска
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//li[contains(@class, "city-list-item") and contains(., "Санкт-Петербург")]')))
            allure.attach(driver.get_screenshot_as_png(),
                          name="city_search_entered",
                          attachment_type=allure.attachment_type.PNG)

        with allure.step("5. Выбрать город из списка"):
            city_option = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//li[contains(@class, "city-list-item") and contains(., "Санкт-Петербург")]')))
            city_option.click()
            # Ожидаем обновление информации о городе
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//button[@class="header-location" and contains(text(), "Санкт-Петербург")]')))
            allure.attach(driver.get_screenshot_as_png(),
                          name="city_selected",
                          attachment_type=allure.attachment_type.PNG)

        with allure.step("6. Проверить отображение нового города"):
            locator = (By.XPATH, '//button[@class="header-location" and contains(text(), "Санкт-Петербург")]')
            city_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(locator)
            )
            allure.attach(driver.get_screenshot_as_png(),
                          name="city_button_found",
                          attachment_type=allure.attachment_type.PNG)

    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(),
                      name="city_verification_failed",
                      attachment_type=allure.attachment_type.PNG)
        raise e


@allure.feature("Сертификаты")
@allure.story("Выбор и покупка сертификата")
def test_select_certificate(driver):
    try:
        with allure.step("1. Открыть главную страницу"):
            driver.get(Config.BASE_URL)
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//body")))

        with allure.step("2. Перейти в корзину"):
            cart_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//span[contains(@class, 'header-controls__text') and contains(., 'Корзина')]")))
            cart_button.click()

        with allure.step("3. Проверить и очистить корзину, если она не пуста"):
            try:
                cart_items = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'cart-item')]")))

                if cart_items:
                    with allure.step("3.1. Корзина не пуста - очищаем"):
                        clear_cart_button = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "//span[contains(@class, 'cart-page__clear-cart-title')]")))
                        clear_cart_button.click()

                        confirm_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//button[contains(., 'Да') or contains(., 'Очистить')]")))
                        confirm_button.click()

                        WebDriverWait(driver, 10).until(
                            EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'cart-item')]")))
            except TimeoutException:
                pass

        with allure.step("4. Перейти в раздел сертификатов"):
            cert_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(@href, 'certificates') or contains(., 'Подарочные сертификаты')]")))
            cert_button.click()

            with allure.step("5. Выбрать пластиковый сертификат"):
                plastic_cert = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//a[contains(., 'Пластиковый сертификат') or contains(@href, 'plastic')]")))
            plastic_cert.click()

            with allure.step("6. Нажать кнопку 'Купить сертификат'"):
                buy_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Купить сертификат')]")))
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buy_button)
                driver.execute_script("arguments[0].click();", buy_button)

            with allure.step("7. Проверить появление формы ввода телефона"):
                phone_input = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//input[@id='tid-input' or contains(@name, 'phone')]")))
                assert phone_input.is_displayed(), "Поле ввода телефона не отображается"
    except Exception as e:
        driver.save_screenshot("certificate_error.png")
        pytest.fail(f"Тест не пройден: {str(e)}")


@allure.title("Проверка перехода на страницу акций")
@allure.description("Тест проверяет переход на страницу акций")
@allure.feature("Акции")
@allure.severity("normal")
def test_promo_page_navigation(driver):
    try:
        with allure.step("1. Открыть главную страницу"):
            driver.get(Config.BASE_URL)

            # Закрытие всех возможных попапов
            for btn_xpath in [
                "//button[contains(., 'Принять')]",
                "//button[contains(., 'Согласен')]",
                "//button[contains(@class, 'close')]"
            ]:
                try:
                    WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, btn_xpath))).click()
                    time.sleep(1)
                except:
                    pass

        with allure.step("2. Перейти на страницу акций"):
            driver.get("https://www.chitai-gorod.ru/promotions")

        with allure.step("3. Проверить успешный переход"):
            WebDriverWait(driver, 20).until(
                EC.url_contains("/promotions"))
            allure.attach(driver.get_screenshot_as_png(),
                          name="promo_page",
                          attachment_type=allure.attachment_type.PNG)
            assert True
    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(),
                      name="error",
                      attachment_type=allure.attachment_type.PNG)
        pytest.fail(f"Тест не пройден: {str(e)}")