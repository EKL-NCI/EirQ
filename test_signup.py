import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_signup_successful(client):
    # Подготовка данных для успешной регистрации / Prepare data for successful registration
    form_data = {
        'user_pwd0': 'password123',
        'user_pwd1': 'password123',
        'business-name': 'My Business',
        'email': 'test@example.com',
        'name': 'John Dufy'
    }
    # Отправка POST запроса на сервер для регистрации / Sending a POST request to the server for registration
    response = client.post('/Signup', data=form_data)
    
    assert response.status_code == 200  # Проверяем успешность ответа / Check the success of the response


def test_signup_password_mismatch(client):
    # Подготовка данных с несовпадающими паролями / Prepare data with mismatched passwords
    form_data = {
        'user_pwd0': 'password123',
        'user_pwd1': 'password333', # Несовпадающий пароль для подтверждения / Mismatched password for confirmation
        'business-name': 'My Business',
        'email': 'test@example.com',
        'name': 'John Dufy'
    }
    # Отправка POST запроса на сервер для регистрации / Sending a POST request to the server for registration
    response = client.post('/Signup', data=form_data)
    # Проверка, что пользователь остается на странице регистрации и получает сообщение об ошибке / Check that the user remains on the registration page and receives an error message
    assert response.status_code == 200
    assert b"Invalid Email or Passwords do not match" in response.data

def test_invalid_email_format(client):
    # Подготовка данных с недопустимым форматом электронного адреса / Prepare data with an invalid email format
    form_data = {
        'user_pwd0': 'password123',
        'user_pwd1': 'password123',
        'business-name': 'My Business',
        'email': 'invalid_email_format',  # Неправильный формат электронной почты / Incorrect email format
        'name': 'John Dufy'
    }
    # Отправка POST запроса на сервер / Sending a POST request to the server
    response = client.post('/Signup', data=form_data)
    # Проверка, что пользователь остается на странице регистрации и получает сообщение об ошибке о недопустимом формате адреса / Check that the user remains on the registration page and receives an error message about the invalid email format
    assert response.status_code == 200
    assert b"INVALID_EMAIL" in response.data 

