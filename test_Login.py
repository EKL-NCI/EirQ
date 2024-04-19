import pytest # Testing fot Python To run 
from flask import session
from app import app #Unit testing Login Functionality using Pytest - Morris Ouedraogo
import time     

@pytest.fixture
def client():  #Define EirQ app as client being tested
    app.config['EirqSecretKey'] = True #secret key for EirQ App
    with app.test_client() as client:
        yield client

def test_login_success(client):  #Test1: used to check when logged in successfully redirected to Dashboard
    # Request to login with valid credentials
    response = client.post('/Login', data={'email': 'morrisoue19@icloud.com', 'password': 'Moneyman'}, follow_redirects=True)
    assert response.status_code == 200  # Once verified Checking if it redirects  to dashboard
    
    # Checking to see if session stores user's email
    with client.session_transaction() as sess:
        assert sess['user'] == 'morrisoue19@icloud.com'


def test_login_failure_invalid_credentials(client): #Test2: used to check to if user enters wrond cred error message displays
    # Request to logint with invalid cred
    response = client.post('/Login', data={'email': 'morrisou19@icloud.com', 'password': 'mandem1'}, follow_redirects=False)
    assert b'Invalid email or password. Please try again.' in response.data  # Check if error message is displayed
    
    # Checking to session does not store user's email
    with client.session_transaction() as sess:
        assert 'user' not in sess


def test_login_failure_unverified_user(client):#Test3: used to check if user is verified and prompt user to verify
    # Request to login with unverified user cred
    response = client.post('/Login', data={'email': 'admin@test.com', 'password': 'MONEY1234'}, follow_redirects=False)
    assert b'Email not verified. Please verify your email to login.' in response.data  # Check if verified message is displayed
    
    # Check if session does not store user's email
    with client.session_transaction() as sess:
        assert 'user' not in sess



def test_login_too_many_attempts(client): #Test3: used to check if user enters password many times wrong account locks
    #Request to login user cred wrong multiple times
    for _ in range(5):
        response = client.post('/Login', data={'email': 'morrisoue19@icloud.com', 'password': 'Moneyman6'}, follow_redirects=False)
        assert b'Too many failed login attempts. Please try again later or contact support.' not in response.data  # Check if error message is not displayed
        time.sleep(2) #to ensure the message was loaded before final try.

    response = client.post('/Login', data={'email': 'morrisoue19@icloud.com', 'password': 'Moneyman6'}, follow_redirects=False)
    assert b'Too many failed login attempts. Please try again later or contact support.' in response.data  # Check if error message is displayed
    
    # Check if session does not store user's email after multiple failed entries
    with client.session_transaction() as sess:
       assert 'user' not in sess
