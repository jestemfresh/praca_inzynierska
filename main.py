from user_interface import UserInterface
import pandas
import sqlite3

# create table
'''
cursor.execute("""CREATE TABLE IF NOT EXISTS products (
            SKU text PRIMARY KEY,
            OUR_PRICE real,
            OUR_STOCK integer,
            URL_1 text,
            PRICE_1 real,
            IS_HIGHER_1 text,
            STOCK_1 integer,
            URL_2 text,
            PRICE_2 real,
            IS_HIGHER_2 text,
            STOCK_2 integer
            )""")
'''

# -------------------------------------------------- MAIN ----------------------------------------------------- #
# konkurencja_csv = pandas.read_csv("market_competition.csv")
# database = sqlite3.connect("market_competition.db")
# cursor = database.cursor()
# konkurencja_csv.to_sql('products', database, if_exists='append', index=False)
# database.commit()
# cursor.close()
# database.close()
UI = UserInterface()



