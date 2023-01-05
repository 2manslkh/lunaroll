import requests
import os

from dotenv import load_dotenv


load_dotenv()  # take environment variables from .env.

BASE_URI = os.getenv("BACKEND_BASE_URL")


def get_balance(telegramId):
    url = f'{BASE_URI}/account/getBalance'
    response = requests.get(url, params={'telegramId': telegramId})
    return response.json()

def get_deposit_address(telegramId):
    # url = f'http://www.google.com'
    url = f'{BASE_URI}/account/getDepositAddress'

    # response = requests.get(url)
    response = requests.get(url, params={'telegramId': telegramId}, headers={'Connection':'close'})
    print("ASDASD")
    print(response.content)
    return response.json()

def withdraw(telegramId, address, currency, amount):
    url = f'{BASE_URI}/account/withdraw'

    response = requests.post(url, data={'telegramId': telegramId, 'withdrawAddress': amount, 'currency': currency, 'amount':amount})
    return response.json()

def create(telegramId):
    url = f'{BASE_URI}/account/create'

    response = requests.post(url, data={'telegramId': telegramId})
    return response.json()