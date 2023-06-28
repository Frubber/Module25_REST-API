from app import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()

########################################### ПОЗИТИВНЫЕ ТЕСТЫ ####################################################

def test_get_api_key_valid_user(email=valid_email, password=valid_password):
    '''Проверяем что код статуса запроса 200 и в переменной result
    содержится слово key'''
    status, result = pf.get_app_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    '''Проверяем что код статуса запроса 200 и список всех питомцев не пустой'''
    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(api_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_pets_with_valid_data(name='Vasya', animal_type='cat', age='4', pet_photo='images/Vasya.jpg'):
    '''Проверяем что код статуса запроса 200 и что список с добавленными данными не пустой для этого
    в переменную pet_photo сохраняем путь к файлу фотографии питомца, сохраняем ключ в переменную api_key,
    проверяем статус ответа и что в ответе содержатся добавленные данные.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_delete_pet():
    '''Проверяем возможность удаления питомца'''
    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pets(api_key, 'Vasya', 'cat', '5', 'images/Vasya.jpg')
        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']

    status, _ = pf.delete_pets(api_key, pet_id)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()


def test_update_pet_info(name='Snejok', animal_type='британец_апдейт', age='3'):
    '''Проверяем возможность изменения данных питомца'''
    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(api_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Питомцы отсутствуют")


def test_add_pets_with_valid_data_without_photo(name='Безфото', animal_type='кошка', age='2'):
    '''Проверяем возможность добавления нового питомца без фото'''
    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_add_photo_at_pet(pet_photo='images/Barsik.jpg'):
    '''Проверяем возможность добавления новой фотографии питомца'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(api_key, my_pets['pets'][0]['id'], pet_photo)

        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception("Питомцы отсутствуют")

########################################### НЕГАТИВНЫЕ ТЕСТЫ ####################################################

def test_add_pet_negative_age_number(name='Vasya', animal_type='cat', age='-5', pet_photo='images/Vasya.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с отрицательным числом в переменной age.
    Тест не будет пройден если питомец будет добавлен на сайт с отрицательным числом в поле возраст.
     '''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    assert age not in result['age'], 'Питомец добавлен на сайт с отрицательным числом в поле возраст'


def test_add_pet_with_invalid_age(name='Vasya', animal_type='cat', age='4356', pet_photo='images/Vasya.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с числом более трех знаков в переменной age.
    Тест не будет пройден ели питомец будет добавлен на сайт с числом превышающим три знака в поле возраст.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    number = result['age']

    assert len(number) < 4, 'Питомец добавлен на сайт с числом привышающим 3 знака в поле возраст'


def test_add_pet_with_empty_name(name='', animal_type='cat', age='2', pet_photo='images/Vasya.jpg'):
    '''Проверяем возможность добавления питомца с пустым значением в переменной name
    Тест не будет пройден если питомец будет добавлен на сайт с пустым значением в поле "имя"'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] != '', 'Питомец добавлен на сайт с пустым значением в имени'


def test_add_pet_with_special_characters(name='Vasya', age='3', pet_photo='images/Vasya.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с специальными символами вместо букв в переменной animal_type.
    Тест не будет пройден если питомец будет добавлен на сайт с спец.символами вместо букв в поле порода.
    '''
    animal_type = '###!@'
    symbols = '!@#%#^#%^##@'
    symbol = []

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    for i in symbols:
        if i in result['animal_type']:
            symbol.append(i)
    assert symbol[0] not in result['animal_type'], 'Питомец добавлен с недопустимыми спец.символами'


def test_add_pet_with_numbers_animal_type(name='Vasya', animal_type='754', age='4',
                                                      pet_photo='images/Vasya.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с цифрами вместо букв в переменной animal_type.
    Тест не будет пройден если питомец будет добавлен на сайт с цифрами вместо букв в поле порода.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert animal_type not in result['animal_type'], 'Питомец добавлен на сайт с цифрами вместо букв в поле порода'

