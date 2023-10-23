import os
import json

from dotenv import load_dotenv


SECRET_MANAGER_ENV_PATH = '/envs/.env'
SECRET_MANAGER_AUTH_PATH = '/firebase/auth/firebase_auth.json'
SECRET_MANAGER_CONFIG_PATH = '/firebase/config/firebase_config.json'

load_dotenv(SECRET_MANAGER_ENV_PATH)


INSTANCE_CONNECTION_NAME = os.environ.get('INSTANCE_CONNECTION_NAME')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_DB = os.environ.get('REDIS_DB')

with open(SECRET_MANAGER_AUTH_PATH, 'r') as file:
    FIREBASE_AUTH: dict = json.load(file)

with open(SECRET_MANAGER_CONFIG_PATH, 'r') as file:
    FIREBASE_CONFIG: dict = json.load(file)

FRONTEND_URL = os.environ.get('FRONTEND_URL')
