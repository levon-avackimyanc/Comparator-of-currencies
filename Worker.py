import requests
from bs4 import BeautifulSoup as bs
from configs import CB_URL, UNISTREAM_URL

class Worker():
    def __init__(self)
        self._currencys_cb = {}
        self._currencys_uni = {}

    def get_data_from_cb(self):
        responce_cb = requests.get(CB_URL)
        soup = bs(responce_cb.text)
        data_table = soup.find('table', {'class': 'data'})
        data_table_tr = data_table.find_all('tr')

        rows = list()

        for tr in range(len(data_table_tr)):
            rows.append(str(data_table_tr[tr].find_all('td')))

        rows.pop(0)

        for row in range(len(rows)):
            data = rows[row].replace('<td>', '').replace('</td>', '')
            data = data.strip('][').split(', ')

            quantity = int(data[2])
            rate = float(data[-1].replace(',', '.'))

            key = data[1]
            value = rate / quantity

            self._currencys_cb[key] = round(value, 4)

    def get_data_from_uni(self):
        responce_uni = requests.get(UNISTREAM_URL)
        responce_uni_new = responce_uni.json()

        for i in range(len(responce_uni_new)):
            if responce_uni_new[i]["currency"]:
                self._currencys_uni[responce_uni_new[i]["currency"]] = round(responce_uni_new[i]["rate"], 4)
            else:
                continue

    def view_currencies_from_uni(self):
        for key, value in self._currencys_uni.items():
            print(f'Unistream currencys {key} rate {value}')

    def view_currencies_from_cb(self):
        for key, value in self._currencys_cb.items():
            print(f'CB currency {key} rate {value}')

    def compare_currencies(self):
        result_file = open('result_file', 'w')
        for key, value in self._currencys_cb.items():
            if key not in self._currencys_uni:
                result_file.write(f'В Юнистриме нет курса для валюты {key}\n')
            elif value != self._currencys_uni[key]:
                result_file.write(
                    f'Значение курса {key} {self._currencys_uni[key]} в Юнистриме не совпадает с курсом на сайте ЦБ '
                    f'{value}\n')
        result_file.close()

    def run_script(self):
        self.get_data_from_cb()
        self.get_data_from_uni()
        self.compare_currencies()