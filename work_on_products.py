import requests
import regex
from bs4 import BeautifulSoup
import sqlite3
import pandas



class WorkingOnProducts:

    def __init__(self):
        self.work_file = pandas.read_csv("market_competition.csv")
        self.URL_1 = self.work_file.URL_1
        self.URL_2 = self.work_file.URL_2

        self.prices_1 = []
        self.prices_2 = []
        self.stocks_1 = []
        self.stocks_2 = []
        self.flat_stock = []

        self.i = 0

    def get_price_from_shop_1(self, urls):
        response = requests.get(urls)
        url_info = response.text
        soup = BeautifulSoup(url_info, "html.parser")
        price_1 = soup.find(name="td", class_="big-green-price").text
        spl = price_1.replace("zł", "")
        spl2 = spl.replace(" ", "")
        spl3 = spl2.replace(",", ".")
        float_num = float(spl3)
        self.prices_1.append(float_num)

    def get_price_from_shop_2(self, urls):
        response = requests.get(urls)
        url_info = response.text
        soup = BeautifulSoup(url_info, "html.parser")
        price_2 = soup.find(name="span", id="our_price_display").text
        spl = price_2.replace("zł", "")
        spl2 = spl.replace(" ", "")
        spl3 = spl2.replace(",", ".")
        float_num = float(spl3)
        self.prices_2.append(float_num)

    def update_price_to_db_shop_1(self):
        database = sqlite3.connect("market_competition.db")
        self.work_file = pandas.read_csv("market_competition.csv")
        cursor = database.cursor()
        self.i = 0
        for url in self.work_file.URL_1:
            self.get_price_from_shop_1(url)
            cursor.execute(
                "UPDATE products SET PRICE_1 = (:price) WHERE URL_1 = (:url)",
                {'price': self.prices_1[self.i], 'url': url}
            )
            self.i += 1
        database.commit()
        cursor.close()
        database.close()

    def calculate_diff_price(self):
        database = sqlite3.connect("market_competition.db")
        cursor = database.cursor()

        cursor.execute(
            "update products set DIFF_1 = round(PRICE_1-OUR_PRICE,2)"
        )
        cursor.execute(
            "update products set DIFF_2 = round(PRICE_2-OUR_PRICE,2)"
        )
        database.commit()
        cursor.close()
        database.close()

    def update_price_to_db_shop_2(self):
        database = sqlite3.connect("market_competition.db")
        self.work_file = pandas.read_csv("market_competition.csv")
        cursor = database.cursor()
        self.i = 0
        for url in self.work_file.URL_2:
            self.get_price_from_shop_2(url)
            cursor.execute(
                "UPDATE products SET PRICE_2 = (:price) WHERE URL_2 = (:url)",
                {'price': self.prices_2[self.i], 'url': url}
            )
            self.i += 1
        database.commit()
        cursor.close()
        database.close()

    def compare_prices(self):
        database = sqlite3.connect("market_competition.db")
        cursor = database.cursor()
        cursor.execute(
            "UPDATE products SET IS_HIGHER_1 = True WHERE PRICE_1 >= OUR_PRICE",
        )
        cursor.execute(
            "UPDATE products SET IS_HIGHER_1 = False WHERE PRICE_1 < OUR_PRICE",
        )
        cursor.execute(
            "UPDATE products SET IS_HIGHER_2 = True WHERE PRICE_2 >= OUR_PRICE",
        )
        cursor.execute(
            "UPDATE products SET IS_HIGHER_2 = False WHERE PRICE_2 < OUR_PRICE",
        )
        database.commit()
        cursor.close()
        database.close()

    def change_to_lowest_price(self):
        database = sqlite3.connect("market_competition.db")
        cursor = database.cursor()
        cursor.execute("""UPDATE products SET OUR_PRICE = 
            CASE 
            WHEN(PRICE_1 < OUR_PRICE OR PRICE_2 < OUR_PRICE) and PRICE_1 <= PRICE_2 THEN PRICE_1 
            WHEN(PRICE_1 < OUR_PRICE OR PRICE_2 < OUR_PRICE) and PRICE_2 <= PRICE_1 THEN PRICE_2 
            ELSE OUR_PRICE 
            END""")
        database.commit()
        cursor.close()
        database.close()

    def get_stock_info_1(self):
        self.work_file = pandas.read_csv("market_competition.csv")

        for url in self.work_file.URL_1:
            response = requests.get(url)
            url_info = response.text
            soup = BeautifulSoup(url_info, "html.parser")
            stock_1 = soup.find(name="div", class_="description").text
            number = regex.findall(r"([\d.]+)\s*(sztuk)", stock_1)
            number_listed = list(map(lambda x: x[0], number))
            if number_listed == []:
                number_listed = ["NOT GIVEN"]
            self.stocks_1.append(number_listed)
        self.flatten_list(self.stocks_1)

    def flatten_list(self, data):
        for element in data:
            if type(element) == list:
                self.flatten_list(element)
            else:
                self.flat_stock.append(element)

    def update_stock_to_db_shop_1(self):
        self.stocks_1 = []
        database = sqlite3.connect("market_competition.db")
        self.work_file = pandas.read_csv("market_competition.csv")
        cursor = database.cursor()
        self.i = 0
        self.get_stock_info_1()

        for url in self.work_file.URL_1:
            cursor.execute(
                "UPDATE products SET STOCK_1 = (:stock) WHERE URL_1 = (:url)",
                {'stock': self.flat_stock[self.i], 'url': url}
            )
            self.i += 1
        database.commit()
        cursor.close()
        database.close()

    def get_stock_info_2(self, urls):
        response = requests.get(urls)
        url_info = response.text
        soup = BeautifulSoup(url_info, "html.parser")
        stock_2 = soup.find(name="span", id="quantityAvailable").text
        self.stocks_2.append(stock_2)

    def update_stock_to_db_shop_2(self):
        self.stocks_2 = []
        database = sqlite3.connect("market_competition.db")
        self.work_file = pandas.read_csv("market_competition.csv")
        cursor = database.cursor()
        self.i = 0
        for url in self.work_file.URL_2:
            self.get_stock_info_2(url)
            cursor.execute(
                "UPDATE products SET STOCK_2 = (:stock) WHERE URL_2 = (:url)",
                {'stock': self.stocks_2[self.i], 'url': url}
            )
            self.i += 1
        database.commit()
        cursor.close()
        database.close()

    def db_to_csv(self):
        db_file = "market_competition.db"
        conn = sqlite3.connect(db_file, isolation_level=None, detect_types=sqlite3.PARSE_COLNAMES)
        self.calculate_diff_price()
        db_df = pandas.read_sql_query("SELECT * FROM products", conn)
        db_df.to_csv("market_competition.csv", index=False)

    def start_web_scrapping_all(self):
        self.update_price_to_db_shop_1()
        self.update_stock_to_db_shop_1()
        self.update_price_to_db_shop_2()
        self.update_stock_to_db_shop_2()
        self.compare_prices()
        self.db_to_csv()

    def start_web_scrapping_prices(self):
        self.update_price_to_db_shop_1()
        self.update_price_to_db_shop_2()
        self.compare_prices()
        self.db_to_csv()

    def start_web_scrapping_stocks(self):
        self.update_stock_to_db_shop_1()
        self.update_stock_to_db_shop_2()
        self.db_to_csv()
