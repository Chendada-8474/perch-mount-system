import os
import sys
import requests
from urllib.parse import urljoin

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import configs.config as config


def get(api_url: str):
    response = requests.get(urljoin(config.HOST, api_url))
    return response.json()
