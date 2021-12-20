from queue import Queue
from threading import Thread
from bs4 import BeautifulSoup
import requests

from config import BASE_LINK
from crypto_symbols import crypto_symbols


class CurrencyCrawler:
    def __init__(self, currency_list):
        self.currency_list = currency_list
        self.queue = self.create_queue()

    def create_queue(self):
        """
        put all the links in the queue for multithreading
        """
        queue = Queue()
        for curr in self.currency_list:
            currency_name = crypto_symbols[curr]
            queue.put({'name': currency_name, 'link': BASE_LINK.format(currency_name)})
        return queue

    def start(self):
        thread_count = len(self.currency_list) if len(self.currency_list) < 10 else 10
        for _ in range(thread_count):
            thread = Thread(target=self.crawl)
            thread.start()
        self.queue.join()

    def crawl(self):
        while True:
            curr = self.queue.get()
            curr_data = {'Currency Name': curr['name'], **self.parse_currency_data(self.get(curr['link']).text)}
            print(curr_data)
            self.queue.task_done()
            if self.queue.empty():
                break

    @staticmethod
    def parse_currency_data(html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        stat_values = soup.find_all('div', {'class': 'statsValue'})
        total_supply = soup.find_all('div', {'class': 'maxSupplyValue'})[1]

        return {
            'Market Cap': stat_values[0].text,
            'Fully Diluted Market Cap': stat_values[1].text,
            'Circulating Supply': stat_values[3].text,
            'total supply': total_supply.text,
        }

    @staticmethod
    def get(url, header=None, proxy=None):
        try:
            response = requests.get(url, headers=header, proxies=proxy)
        except requests.HTTPError:
            return None
        return response



