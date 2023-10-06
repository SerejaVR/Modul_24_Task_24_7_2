Тестовый проект к 24 модулю SkillFactory курса QAP.

В директории /tests располагается файл test_pet_friends.py - с тестами из модуля и тестами для задания 24.7.2.

В директории /tests/images - лежат фото для теста добавления питомца и теста добавления фото.

В корневой директории лежит файл settings.py - содержит информацию о валидном логине и пароле, а также о невалидных, для негативных тестов.

В корневой директории лежит файл api.py с методами - который является библиотекой к REST api сервису веб приложения Pet Friends.

Библиотека api написана в классе, что соответствует принципам ООП и позволяет удобно пользоваться её методами. При инициализации библиотеки объявляется переменная base_url которая используется при формировании url для запроса.

Методы и тесты имеют подробное описание.

Тесты проверяют работу методов используя api библиотеку.
