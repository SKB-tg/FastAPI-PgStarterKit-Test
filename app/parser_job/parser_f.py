import re
import os.path
import sys
import json
import time
import requests, lxml
from bs4 import BeautifulSoup
from pathlib import Path
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from typing import Callable, Dict, Any, Awaitable, Union, List, Optional, BinaryIO, cast
from fastapi import Depends
from sqlalchemy.orm import Session
#from app.api import deps


#import parser_job.headers
from app.parser_job.csv_handler import CsvHandler_W
from app.parser_job.u_utils import get_date_flag
from app import crud

# def get_db() -> Session:
#     try:
#         db = SessionLocal()
#         return db
#     finally:
        # db.close()

class MyUniParser:
    def __init__(self, driver_path: str = "parser_job/chromedriver",
     filename: str = 'vacancy_data2.csv', chat_id=None, bot_token=None):
        self.driver_path = driver_path
        self.filename = filename
        self.chat_id = chat_id
        self.bot_token = bot_token

    def get_html(self, url):
        options = uc.ChromeOptions()
        options.add_argument('--headless')

        driver_executable_path = str(Path.cwd() / self.driver_path)
        driver = uc.Chrome(options=options,  suppress_welcome=False, driver_executable_path = driver_executable_path) #seleniumwire_options=options_proxy)

        try:
            driver.get(url)

            print('oo')
            time.sleep(2)
            html = driver.page_source########## копируем код страницу в перем 
        except Exception as ex:
            print(ex)
            time.sleep(3)
            html = None
        finally:
            driver.close()
            driver.quit()

        return html

    def get_cart_product_html(self, url):
        options = uc.ChromeOptions()

        options.add_argument('--headless')
        driver_executable_path = str(Path.cwd() / self.driver_path)

        driver = uc.Chrome(options=options,  suppress_welcome=False, driver_executable_path = driver_executable_path)

        try:
            driver.get(url)
            print('oooooo')
            time.sleep(2)
            html = driver.page_source
        except Exception as ex:
            print(ex)
            html = None
        finally:
            driver.close()
            driver.quit()
            # print("На аварийное отключение 10с")
            # time.sleep(10)
            print("Придется ожидать след возможости")
        return html

    def get_requests_html(self, url: str, port: str='443'):
        # from requests_html_playwright import HTMLSession
        # session = HTMLSession()
        print(url)
        if str(url)[8:9] == "r":
            url1 = url[:17] + ':' + port + url[17:]
        else:
            return None
            url1 = url[:13] + ':' + port + url[13:]
        try:
            # Send an HTTP request to the provided URL
            headers = {
            # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'accept-encoding': 'gzip, deflate, br',
            # 'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            # 'cache-control': 'no-cache',
            # 'cookie': '__ddg1_=iNzf56w8vhO3n8fmaN2F; region_clarified=NOT_SET; hhuid=E3GEvYOjEIVGOWWADv8u4g--; regions=1002; _xsrf=280c784fea8a063d50fdb36513d85bc8; hhrole=anonymous; display=desktop; total_searches=1; hhtoken=vXKgCTYlA_vfXLiQh6R5cnD5WV0q; GMT=3; device_magritte_breakpoint=s; device_breakpoint=s',
            # 'pragma': 'no-cache',
            # 'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            # 'sec-ch-ua-platform': '"Windows"',
            # 'sec-fetch-dest': 'document',
            # 'sec-fetch-mode': 'navigate',
            # 'sec-fetch-site': 'none',
            #****************************
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':
            'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'DNT': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
            }
            params={'key': 'value'}
            #headers={'User-Agent': 'Mozilla/5.0'}
            proxies= {"http": "http://1925095-all-country-GB:1kx7rsw9hp@194.88.107.159:55403", "https": "http://1925095-all-country-GB:1kx7rsw9hp@194.88.107.159:55403"}# "http://1925095-all-country-GB:1kx7rsw9hp@194.88.107.159:55403"
            response = requests.get(url1, headers=headers)#, proxies=proxies)
            #response = requests.get(url)
            response.raise_for_status()
            #time.sleep(2)
            print(122, response.status_code)
            return response.text  # Raise an error if the status code is not 2xx
        except requests.exceptions.RequestException as e:
            print("Failed to fetch the Gumroad site:")
            print(str(e))
            return None

    def parse_data(self, markup, kategory: str, x: int, fd: int, db: Session, max_count: int=2) -> List[Dict]:
        if markup == None: return None
        soup = BeautifulSoup(markup, 'html5lib')
        item_home_page_vacancy = soup.find_all('div', attrs={'class': 'vacancy-serp-item__layout'})
        nom = 0 + 50*(x-1)
        list_vakancy = []
        k=0
        for x in item_home_page_vacancy:
            payload = {}
            link_vakancy = self.get_link(x)[:34] if self.get_link(x)[8] == "r" else self.get_link(x)[:30]
            description_full = self.get_description_full(link_vakancy)
            day_back = self.get_srok(description_full[1])
            if ((day_back <= fd) & (day_back != 0)):
                name_vakancy = self.get_h3(x) or "--"
                _kategory = self.get_kategory(x) or kategory
                price = self.get_price(x) or "--"
                hanter = self.get_hanter(x) or "--"
                description = self.get_description(x)
                description_full_out = description_full[0][:-444] if sys.getsizeof(description_full[0]) < 7000 else description_full[0][:7000]
                id_v = self.get_id(link_vakancy)
                nom += 1
                payload = {
                    '№': f'00{nom}',
                    'ID вакансии': int(id_v),
                    'категории': _kategory,
                    'Наименование vakancy': name_vakancy,
                    'Компания': hanter,
                    'Заработок': price, 
                    'Краткое описание': description,
                    'link_vakancy': link_vakancy,
                    'Подробное описание': description_full_out,
                    'Дата размещения': description_full[1],
                }

                res = crud.vakancy.get_col(db, payload["ID вакансии"])
                if res:
                    print(164, res.mess_id, res.id_vakancy)
                    payload['message_id'] = res.mess_id
                    if  res.mess_id == 1:
                        resul = self.send_message_to_telegram(self.chat_id, self.bot_token, payload)
                        payload['message_id'] = resul
                        print(167, resul)
                else:
                    resul = self.send_message_to_telegram(self.chat_id, self.bot_token, payload)
                    payload['message_id'] = resul
                    print(169, resul)
                #self.write_to_csv(payload)
                #payload['link_vakancy'] = link_vakancy
                list_vakancy.append(payload)

                if len(list_vakancy) == max_count:
                    print(172, nom, list_vakancy)
                    return list_vakancy
            if (day_back - fd) >= 2:
                k += 1
                if k > 5:
                    return list_vakancy

    def write_to_csv(self, data):        #print (data)

        CsvHandler_W(self.filename, data, f_creat=False)

    def send_message_to_telegram(self, chat_id, token, message_dict):
        #message_dict.pop('link_vakancy')
        message_dict.pop("№")
        message_dict["message_id"] = 1
        message_dict.pop("message_id")
        message_dict["категории"] = f"#{message_dict['категории']}"
        #Проверяем на дублирование

        # Формируем текст сообщения из словаря
        message_text = "\n".join([f"{key}:\n {value}\n" for key, value in message_dict.items() if key != "link_vakancy"])
        message_text = f"Последние обновления по вакансиям\n\n" + message_text
        print(200, token, chat_id)
        # Отправляем запрос на API Telegram с помощью библиотеки requests
        url = f"https://api.telegram.org/bot{token}/sendmessage"
        payload = {"chat_id": chat_id, "text": message_text}
        try:
            response = requests.post(url, data=payload)
            data1 = json.loads(response.text)['result']
            print(186, data1)
            if response.status_code < 300:
                return data1['message_id']
        except Exception as e:
            print(e)
            return 1
        # Проверяем статус код ответа и возвращаем результат



    def try_except(func):
        def wrapper(*args, **kwargs):
            try:
                data = func(*args, **kwargs)
            except:
                data = None
            return data
        return wrapper

    @staticmethod
    @try_except
    def get_id(link) -> int:
        return str(link).split('vacancy/')[1].split('?')[0]

    @staticmethod  
    @try_except
    def get_kategory(soup):
        return soup.find('h1', attrs={'class': "search-catalog-header"}).get_text()
        
    @staticmethod
    @try_except
    def get_h3(soup):
        return soup.find('span', attrs={'class': "serp-item__title"}).get_text()

    @staticmethod
    @try_except
    def get_link(soup):
        return soup.find('a', attrs={'class': "bloko-link"})['href'].strip()

    @staticmethod
    @try_except
    def get_hanter(soup):
        return soup.find('div', attrs={'class': 'vacancy-serp-item-company'}).find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'}).a.get_text()

    @staticmethod
    @try_except
    def get_price(soup):
        return soup.find('span', attrs={'class': 'bloko-header-section-2'}).get_text()

    @staticmethod
    def get_description(x):
        try:
            description = x.find('div', attrs={'class': 'vacancy-serp-item__skills'}).get_text()
        except:
            description = "--"
        return description

    @staticmethod
    def get_srok(date_str_in):
        if date_str_in == "--": return 0
        p1 = date_str_in.split(" ")
        p = [ i[1] for i in [("январь", 1), ("февраль", 2), ("март", 3), ("апрель", 4), ("октябрь", 10), ("ноябрь", 11), ("декабрь", 12)] if (i[0][:-2] == p1[1][:-2])]
        if date_str_in == None:
            return 0
        else:
            date_str=f"{p1[2]}-{p[0]}-{p1[0]}"
            d = get_date_flag(date_str)
            print(d)
            return d

    @staticmethod
    def get_description_full(link_vakancy) -> List:
        html_vacancy = MyUniParser().get_requests_html(link_vakancy) or ""
        soup = BeautifulSoup(html_vacancy, 'html5lib')
        try:
            box_text = soup.find('div', attrs={'class': 'vacancy-description'}).get_text().strip().replace('\\n\\n\\n', ' ')
            date = soup.find('p', attrs={'class': 'vacancy-creation-time-redesigned'}).find('span').get_text()
        except:
            box_text = "--"
            date = "--"
      
        return [box_text.replace("\xa0", ' '), date.replace("\xa0", ' ')]


# Теперь для использования модуля нужно создать объект класса `MyUniParser` и вызывать его методы, например:

# ```python
# parser = MyUniParser()
# html = parser.get_html(url)
# list_vacancy = parser.parse_data(html, 1, 1)
# ```


