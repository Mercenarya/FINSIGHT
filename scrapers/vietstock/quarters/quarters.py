from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import unidecode
import requests
import pandas as pd
import numpy as np
import os
import sys
import re
import json

#lớp dữ liệu doanh thu
class Revenue:
    def __init__(self,title,q1,q2,q3,q4,timeline:list):
        self.title = title
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4
        self.timeline = timeline

    # dữ liệu dạng dict
    def get_data(self):
        return {
            "title":self.title,
            "First":self.q1,
            "Second":self.q2,
            "Third":self.q3,
            "Fourth":self.q4,
            "Timeline":self.timeline
        }
    
    def __repr__(self):
        return f"< Revenue {self.title} : {self.q1} - {self.q2} - {self.q3} - {self.q4} - Timeline: {self.timeline}"

#dữ liệu tháng hiện tại
def current_timeline(driver:webdriver.Chrome):
    pass

#dữ liệu tháng trước
def previous_timeline(driver:webdriver.Chrome):
    pass

#dữ liệu tháng tiếp
def next_timeline(driver:webdriver.Chrome):
    pass


def convert_sales_service_data(driver:webdriver.Chrome):
    '''
    Lấy thông tin số liệu của doanh thu bán 
    hàng và dịch vụ từ doanh nghiệp theo
    Class chỉ định 
    '''
    # data = []
    rows = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'tbody'))
    )
    qrt = rows.find_elements(By.CLASS_NAME, "td")

    tt = qrt[0].text
    q1 = qrt[1].text
    q2 = qrt[2].text
    q3 = qrt[3].text
    q4 = qrt[4].text


    return tt,q1,q2,q3,q4


if __name__ == "__main__":
    pass