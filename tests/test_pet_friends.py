from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password, invalid_email_2, invalid_password_2, invalid_email_3, invalid_password_3
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0



def test_add_new_pet_with_valid_data(name='Nika', animal_type='Alabay',
                                     age='5', pet_photo='images/dog1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/dog2.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_add_pet_without_photo(name='Nikol', animal_type='Alab', age= 3):
    """Проверяем возможностьдобавления питомца без фото."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_successfu_add_photo_of_pet(pet_photo='images/dog2.jpg'):
    """Проверяем возможность добавления фото питомца."""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    """Если список не пустой добавляем фото."""
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

        assert status == 200
        assert result['pet_photo'] == pet_photo
    else:
        raise Exception("There is no my pets")


# ТЕСТЫ ДЛЯ ПРАКТИЧЕСКОГО ЗАДАНИЯ 24.7.2.

def test_get_api_key_for_invalid_email(email=invalid_email, password=valid_password):
    """ТЕСТ №_1.Проверяем запрос api ключа с НЕ валидным email (без @ 'собаки') и валидным password"""
    status, _ = pf.get_api_key(email, password)
    """Отправляем запрос."""
    assert status == 403
    """Сверяем полученные данные с нашими ожиданиями."""

def test_get_api_key_for_invalid_password(email=valid_email, password=invalid_password):
    """ТЕСТ №_2.Проверяем запрос api ключа с валидным email и НЕ валидным (спецсимволы) password"""
    status, _ = pf.get_api_key(email, password)
    """Отправляем запрос."""
    assert status == 403
    """Сверяем полученные данные с нашими ожиданиями."""

def test_get_api_key_for_invalid_email_2(email=invalid_email_2, password=valid_password):
    """ТЕСТ №_3.Проверяем запрос api ключа с НЕ валидным email (Верхний регистр) и валидным password"""
    status, _ = pf.get_api_key(email, password)
    """Отправляем запрос."""
    assert status == 403
    """Сверяем полученные данные с нашими ожиданиями."""
    """Здесь тест возвращает статус 200. ЭТО БАГ!!!"""

def test_get_api_key_for_invalid_password_2(email=valid_email, password=invalid_password_2):
    """ТЕСТ №_4.Проверяем запрос api ключа с валидным email и НЕ валидным (Пустое значение.) password"""
    status, _ = pf.get_api_key(email, password)
    """Отправляем запрос."""
    assert status == 403
    """Сверяем полученные данные с нашими ожиданиями."""

def test_get_api_key_for_invalid_email_3(email=invalid_email_3, password=valid_password):
    """ТЕСТ №_5.Проверяем запрос api ключа с НЕ валидным email (Ввод цифр вместо текста.) и валидным password"""
    status, _ = pf.get_api_key(email, password)
    """Отправляем запрос."""
    assert status == 403
    """Сверяем полученные данные с нашими ожиданиями."""

def test_get_api_key_for_invalid_password_3(email=valid_email, password=invalid_password_3):
    """ТЕСТ №_6.Проверяем запрос api ключа с валидным email и НЕ валидным (Пробел в пароле.) password"""
    status, _ = pf.get_api_key(email, password)
    """Отправляем запрос."""
    assert status == 403
    """Сверяем полученные данные с нашими ожиданиями."""

def test_add_pet_without_photo_without_name(animal_type='Alab', age= 3):
    """ТЕСТ №_7.Проверяем возможность добавления питомца без параметра 'name'."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    """Запрашиваем ключ 'api'."""
    status, _ = pf.add_new_pet_without_photo(auth_key, name=None, animal_type=animal_type, age=age)
    """Добавляем питомца."""
    assert status == 400
    """Сверяем полученные данные с нашими ожиданиями."""

def test_add_pet_without_photo_without_animal_type(name = 'Nika', age= 3):
    """ТЕСТ №_8.Проверяем возможность добавления питомца без параметра 'animal_type'."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    """Запрашиваем ключ 'api'."""
    status, _ = pf.add_new_pet_without_photo(auth_key, name=name, animal_type=None, age=age)
    """Добавляем питомца."""
    assert status == 400
    """Сверяем полученные данные с нашими ожиданиями."""

def test_add_pet_without_photo_incorrect_age(name='Nikol', animal_type='Alab', age= -3):
    """ТЕСТ №_9.Проверяем возможность добавления питомца с отрицательным параметром 'age'."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    """Запрашиваем ключ 'api'."""
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    """Добавляем питомца."""
    assert status == 400
    assert result['name'] == name
    """Сверяем полученные данные с нашими ожиданиями."""
    """Здесь тест возвращает статус 200. ЭТО БАГ!!!"""

def test_add_pet_without_photo_incorrect_big_age(name='Nikol', animal_type='Alab', age= 1000):
    """ТЕСТ №_10.Проверяем возможность добавления питомца с нереальным параметром 'age'."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    """Запрашиваем ключ 'api'."""
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    """Добавляем питомца."""
    assert status == 400
    assert result['name'] == name
    """Сверяем полученные данные с нашими ожиданиями."""
    """Здесь тест возвращает статус 200. ЭТО БАГ!!!"""



















