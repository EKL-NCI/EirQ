import pytest #testing for python
import flask
from unittest.mock import patch
from flask import session
from app import app 
import time


@pytest.fixture
def client():  #define EirQ app as client being tested
    app.config['TESTING'] = True #enable testing mode
    app.config['EirqSecretKey'] = True # secret key for EirQ app
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'/' in response.data

def test_login_route(client):
    response = client.get('/Login')
    assert response.status_code == 200
    assert b'/Login' in response.data
    
def test_Signup_route(client):
    response = client.get('/Signup')
    assert response.status_code == 200
    assert b'/Signup' in response.data

def test_Dashboard_route_not_logged_in(client):
    response = client.get('/Dashboard', follow_redirects=True) #try to get dashboard
    assert response.status_code == 200 
    assert b'/' in response.data #Home page is rendered as user cannot access dashboard without authentication 

def test_Dashboard_route(client):
    credentials = {'email': 'morrisoue19@icloud.com', 'password': 'Moneyman'} #using Morris's login as I forgot my password
    client.post('/Login', data=credentials) #Must go through login and validate credentials first
    response = client.get('/Dashboard') #THEN get dashboard
    assert response.status_code == 200 #route provides direct response to the dashboard page
    
    
def test_Sensors_route(client):
    credentials = {'email': 'morrisoue19@icloud.com', 'password': 'Moneyman'} 
    client.post('/Login', data=credentials) 
    response = client.get('/Sensors') 
    assert response.status_code == 200

def test_Verify_route(client):
    credentials = {'email': 'morrisoue19@icloud.com', 'password': 'Moneyman'} 
    client.post('/Login', data=credentials) 
    response = client.get('/Verify') 
    assert response.status_code == 200

def test_orderSubmitted_route(client):
    credentials = {'email': 'morrisoue19@icloud.com', 'password': 'Moneyman'} 
    client.post('/Login', data=credentials) 
    response = client.get('/orderSubmitted') 
    assert response.status_code == 200
    
def test_orderSensor_route(client):
    credentials = {'email': 'morrisoue19@icloud.com', 'password': 'Moneyman'} 
    client.post('/Login', data=credentials) 
    response = client.get('/orderSensor')
    assert response.status_code == 200