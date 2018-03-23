import datetime
import os
import re
import requests

from bs4 import BeautifulSoup
# from django.conf import settings
from config import settings


DATA_DIR = os.path.join(settings.ROOT_DIR, '.data')
FILE_PATH = os.path.join(DATA_DIR, f'naver_lotto_result.html')


class LottoNumberData:
    def __init__(self):
        self.win_num_list = []
        self.bonus_num = None
        self.draw = None
        self.date = None

    def get_data_and_save_file(self, draw):
        with open(FILE_PATH, 'wt') as f:
            url = f'http://search.naver.com/search.naver'
            params = {
                'query': draw + '회로또'
            }
            response = requests.get(url, params)
            source = response.text
            f.write(source)

    def get_data(self):
        # --------실제 크롤링 할 때 사용해야 하는 구문----------
        # url = f'http://search.naver.com/search.naver'
        # params = {
        #     'query': '로또'
        # }
        # response = requests.get(url, params)
        # source = response.text

        # --------저장된 파일을 읽을 때 사용하는 구문----------
        source = open(FILE_PATH, 'rt').read()
        # ----------------------------------------------

        soup = BeautifulSoup(source, 'lxml')

        lotto_wrap = soup.select_one('.lotto_wrap')
        lotto_tit = lotto_wrap.select_one('.lotto_tit > h3 > a')
        str_draw = lotto_tit.select_one('em').get_text()
        self.draw = re.search(r'\d*', str_draw).group()
        str_date = lotto_tit.select_one('span').get_text()
        self.date = datetime.datetime.strptime(str_date, '%Y.%m.%d').date()

        num_box = lotto_wrap.select_one('.num_box')
        num_list = []
        for item in num_box:
            if item.name == 'span' and 'num' in item['class']:
                num_list.append(item.get_text())

        for index, number in enumerate(num_list):
            if index == 6:
                self.bonus_num = number
            else:
                self.win_num_list.append(number)

        print(f'get data~~ : {datetime.datetime.now()}')


# test = LottoNumberData()
# test.get_data()
# print(test.draw)
# print(test.date)
# print(test.win_num_list)
# print(test.bonus_num)
# test.get_data_and_save_file('790')
