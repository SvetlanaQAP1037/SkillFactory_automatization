import pytest
from api import PetFriends
from settings import valid_email, valid_password
from faker import Faker
import random

pf = PetFriends()
fake = Faker()

def test_get_api_key_with_invalid_email(email='123456', password=valid_password):
    '''Проверяем получение ключа с не корректным email'''
    status, result = pf.get_api_key(email, password)
    assert status == 403 #доступ пользователя с неизвестным email запрещен, значит тест пройден
    assert 'key' not in result

def test_get_api_key_with_invalid_password(email=valid_email, password='hgfdukj'):
    '''Проверяем получение ключа с не корректным паролем'''
    status, result = pf.get_api_key(email, password)
    assert status == 403 #доступ пользователя с неизвестным password запрещен, значит тест пройден
    assert 'key' not in result

def test_get_api_key_with_empty_fields_email_and_password(email='', password=''):
    '''Проверяем получение ключа с незаполненными (пустыми) полями email и password'''
    status, result = pf.get_api_key(email, password)
    assert status == 403 #доступ пользователя с неизвестным password запрещен, значит тест пройден
    assert 'key' not in result

def test_impossible_add_photo_of_other_user_pet(pet_photo="images\\fox.jpeg"):
    """Проверяем, что нельзя добавить фото чужому питомцу"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id_my_pets = my_pets['pets'][0]['id']
    pet_id = all_pets['pets'][0]['id']

    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
    if pet_id == pet_id_my_pets:
        assert status == 200 #если фото добавилось к питомцу из моего списка, ошибки нет
    else:
        assert status == 500 #если сервер не может обработать запрос, значит тест пройден

def test_impossible_update_other_user_pet_info(name=fake.first_name(), animal_type='попугай',
                                               age=random.randint(1, 20)):
    """Проверяем, что нельзя обновить инфо о чужом питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(all_pets['pets']) > 0 and all_pets['pets'][0]['id'] != my_pets['pets'][0]['id']:
        status, result = pf.update_pet_info(auth_key, all_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 500 # статус кода 200, тест провален, заводим баг, сервер дает обновить информацию по чужим питомцам
        assert result['name'] == name
    else:
        raise Exception("There are no pets")

def test_impossible_delete_other_user_pet():
    """Проверяем, что нельзя удалить чужого питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = all_pets['pets'][0]['id']

    if all_pets['pets'][0]['id'] != my_pets['pets'][0]['id']:
        status, _ = pf.delete_pet(auth_key, pet_id)
        assert status == 500 # статус кода 200, тест провален, заводим баг, сервер дает удалить чужого питомца
    else:
        print('There is pet from my list')

def test_add_new_pet_with_invalid_photo(name=fake.first_name(), animal_type='yozhik',
                                     age=str(random.randint(1, 20)), pet_photo='images/domashniy-yozh.bmp'):
    """Проверяем можно ли добавить фото питомца в другом формате .bmp"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 500 # статус кода 200, тест провален, заводим баг,
    # сервер дает загрузить картинку питомца в формате, не соответствующей документации

def test_add_new_pet_with_invalid_animal_type(name=fake.first_name(), animal_type='s82tepFRFbuxXmsCssp8L7ngmQC5Ni04hOk'
                                                                                  'xEIXh1tjxbdoqpHWkJTf2wdG0Uu0D0yAUOA8'
                                                                                  '54QFf2dd3c6LkJWbFhbD3r57X969XpRj96oC'
                                                                                  'TvUay2wGMC8XOfXrcmLkuyEwqZCZwUUMTMDx'
                                                                                  '8KNCbUpqvvhIgYSEwP8BNVMazHeCrjmNzS89'
                                                                                  'n8LHwD2RQSuJfN4htaceyozaB0J8ran1UHff'
                                                                                  'kq6tw2FPuz509nnR9aqn0fF6fZmsRQwsH7yU'
                                                                                  '2CMlB9',
                                     age=str(random.randint(1, 20)), pet_photo='images/Cat_deadline.jpg'):
    """Проверяем можно ли добавить в поле "Вид животного" 257 буквенно-символьных значений"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 500 # статус кода 200, тест провален, заводим баг,сервер дает ввести не корректные данные

def test_add_new_pet_with_invalid_minus_age(name=fake.first_name(), animal_type='енотик',
                                     age=str(-138), pet_photo='images/raccoon.jpg'):
    """Проверяем можно ли добавить в поле "Возраст" отрицательные значения"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 500 # статус кода 200, тест провален, заводим баг,сервер дает ввести отрицательный возраст

def test_create_pet_simple_with_empty_data(name='', animal_type='',
                                     age=''):
    """Проверяем можно ли добавить питомца без заполнения полей информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    assert status == 500 # статус кода 200, тест провален, заводим баг,сервер дает создать питомца без данных








