from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
import socket
import speedtest
import asyncio
import time
import matplotlib.pyplot as plt
import pythonping
from pythonping import ping
import unidecode
import json

# chuyển đổi kí tự từ hoa sang thường
def convert_string(data:str):
    try:
        unidecode_key = unidecode.unidecode(input).lower()
        data = "-".join(unidecode_key.split())
        return data
    except Exception as error:
        return error


def get_ul_list_results(driver):
    try:
        pass
    except Exception as error:
        return {

        }