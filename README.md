# Автотесты сайта "Читай-город" 

Проект содержит автотесты UI и API веб-сайта "Читай-город" 
Ссылка на проект по курсовой работе ручного тестировония:
https://skyprozheka-tester.yonote.ru/share/927339df-08f8-4026-9af0-e43b832fff0d/doc/test-plan-vOhKCwTmux

##  Установка и настройка окружающей среды

1. Клонируйте репозиторий:
   ```bash
   git clone <repository-url>
   cd 
   
установите зависимости: pip install -r requirements.txt
Запуск всех тестов pytest: DiploM_Final/tests
Запуск API тестов pytest: DiploM_Final/tests/test_api.py   
Запуск Ui тестов pytest pytest: DiploM_Final/tests/test_ui.py
Запуск отчетов ALLURE  pytest: --alluredir=allure-results
Просмотр результатов: allure serve allure-results