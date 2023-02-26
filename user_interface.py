from tkinter import *
from tkinter import messagebox
import pandas
import sqlite3
from work_on_products import WorkingOnProducts
from ctypes import windll


FONT = ("Ubuntu", 8, "bold")

BG_COLOR = "#daaa9a"
BG_LINE = "#a37768"

GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080


class UserInterface:
    def __init__(self):
        messagebox.showinfo(title=f"Filename",
                            message=f"Make sure that ur CSV filename is 'market_competition.csv'")
        self.window_main = Tk()
        self.window_main.title("Market competition")
        self.window_main.config(width=500, height=300, pady=50, padx=50, bg=BG_COLOR)

        # remove top bar
        self.window_main.overrideredirect(True)
        self.window_main.after(10, lambda: self.set_appwindow())

        # create top bar
        self.top_bar = Frame(self.window_main, bg="#ae887b")
        self.top_bar.grid(column=0, row=0, columnspan=3)
        self.top_bar.config(width=70)

        # create top label
        self.top_label = Label(self.top_bar, text="Market competition App.", bg="#ae887b", fg="white")
        self.top_label.grid(column=0, row=0, columnspan=2)
        self.top_label.config(width=64)
        # bind title bar
        self.top_label.bind("<B1-Motion>", self.move_lab)

        # create close button
        self.close_label = Label(self.top_bar, text="  Close  ", bg="#ae887b", fg="white")
        self.close_label.grid(column=2, row=0)
        self.close_label.bind("<Button-1>", self.on_closing)

        self.shop = WorkingOnProducts()
        # ------------------------ MENU BUTTONS -----------------------#

        # add product to database
        self.button_add_product_to_db = Button(self.window_main, font=FONT, text="Add product to DB", width=20,
                                               command=self.new_window_add_sku)
        self.button_add_product_to_db.grid(row=2, column=0, padx=10, pady=20)

        # show all products
        self.button_show_all_products = Button(self.window_main, font=FONT, text="Show products", width=20,
                                               command=self.show_all_products)
        self.button_show_all_products.grid(row=2, column=1, padx=10, pady=20)

        # remove product from database
        self.button_remove_product_from_db = Button(self.window_main, font=FONT, text="Remove product from DB",
                                                    width=20, command=self.new_window_delete_SKU)
        self.button_remove_product_from_db.grid(row=2, column=2, padx=10, pady=20)

        w = Canvas(self.window_main, width=500, height=100, bd=0, highlightthickness=0)
        w.configure(bg=BG_COLOR)
        w.place(x=10, y=85)
        w.create_line(500, 0, 0, 0, fill=BG_LINE)
        z = Canvas(self.window_main, width=500, height=100, bd=0, highlightthickness=0)
        z.configure(bg=BG_COLOR)
        z.place(x=10, y=150)
        z.create_line(500, 0, 0, 0, fill=BG_LINE)
        v = Canvas(self.window_main, width=500, height=100, bd=0, highlightthickness=0)
        v.configure(bg=BG_COLOR)
        v.place(x=10, y=275)
        v.create_line(500, 0, 0, 0, fill=BG_LINE)

        # find product in DB
        #
        # label enter sku
        self.label_enter_SKU = Label(self.window_main, bg=BG_COLOR, text="Search for a specific SKU:", font=FONT)
        self.label_enter_SKU.grid(row=3, column=0, padx=10, pady=20)
        #
        # enter SKU
        self.enter_SKU = Entry(self.window_main, width=20, font=FONT)
        self.enter_SKU.grid(row=3, column=1, padx=10, pady=20)
        #
        # button search SKU
        self.button_search_SKU = Button(self.window_main, text="Search", width=20,
                                        command=lambda: self.search_product_SKU(self.enter_SKU.get().upper()),
                                        font=FONT)
        self.button_search_SKU.grid(row=3, column=2, padx=10, pady=20)

        # label checkbox
        self.label_checkbox = Label(self.window_main, bg=BG_COLOR, text="Choose what to scrap", font=FONT)
        self.label_checkbox.grid(row=4, column=0, padx=10, pady=20)
        #
        # checkbox only price
        self.checked_state_price = IntVar()
        self.checkbutton_price = Checkbutton(text="Scrap only price", bg=BG_COLOR, variable=self.checked_state_price,
                                             font=FONT)
        self.checked_state_price.get()
        self.checkbutton_price.grid(row=4, column=1)
        #
        # checkbox only stock
        self.checked_state_stock = IntVar()
        self.checkbutton_stock = Checkbutton(text="Scrap only stock", bg=BG_COLOR, variable=self.checked_state_stock,
                                             font=FONT)
        self.checked_state_stock.get()
        self.checkbutton_stock.grid(row=4, column=2)
        #
        # Update database
        self.button_database_update = Button(self.window_main, text="START WEB SCRAPPING", width=70,
                                             command=self.scrap_checkbox, font=FONT)
        self.button_database_update.grid(row=5, column=0, columnspan=3, padx=10, pady=20)

        # enter database to csv
        self.enter_db_to_csv = Entry(self.window_main, width=20, font=FONT)
        self.enter_db_to_csv.grid(row=6, column=0, padx=10, pady=20)
        self.enter_db_to_csv.insert(END, "Your file name")
        #
        #Change prices to lowest
        self.checked_state_to_lowest_price = IntVar()
        self.checkbutton_to_lowest_price = Checkbutton(text="Change your prices to the \nlowest of your competitors", bg=BG_COLOR, variable=self.checked_state_to_lowest_price,
                                             font=FONT)
        self.checked_state_to_lowest_price.get()
        self.checkbutton_to_lowest_price.grid(row=6, column=1)
        #
        # Export database to csv
        self.button_database_export = Button(self.window_main, text="EXPORT DATABASE TO CSV", width=21, font=FONT,
                                             command=self.low_checkbox)
        self.button_database_export.grid(row=6, column=2, padx=10, pady=20)

        self.window_main.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window_main.mainloop()

    def set_appwindow(self):

        top_bar_windll = windll.user32.GetParent(self.window_main.winfo_id())
        window_style_win = windll.user32.GetWindowLongW(top_bar_windll, GWL_EXSTYLE)
        window_style_win = window_style_win & ~WS_EX_TOOLWINDOW
        window_style_win = window_style_win | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(top_bar_windll, GWL_EXSTYLE, window_style_win)
        self.window_main.wm_withdraw()
        self.window_main.after(10, lambda: self.window_main.wm_deiconify())

    def move_lab(self, e):
        self.window_main.geometry(f'+{e.x_root}+{e.y_root}')

    def export_new_csv(self):
        csv_entry = self.enter_db_to_csv.get()
        db_file = "market_competition.db"
        conn = sqlite3.connect(db_file, isolation_level=None, detect_types=sqlite3.PARSE_COLNAMES)
        db_csv = pandas.read_sql_query("SELECT * FROM products", conn)
        db_csv.to_csv(f"{csv_entry}.csv", index=False)

    def on_closing(self, e):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window_main.quit()

    def low_checkbox(self):
        if self.checked_state_to_lowest_price.get() == 1:
            self.shop.change_to_lowest_price()
            self.shop.compare_prices()
            self.shop.calculate_diff_price()
            self.export_new_csv()
        else:
            self.export_new_csv()

    def scrap_checkbox(self):
        if self.checked_state_stock.get() == 1 and self.checked_state_price.get() == 1:
            self.shop.start_web_scrapping_all()
            messagebox.showinfo(title=f"Success",
                                message=f"Scraping done!")
        elif self.checked_state_stock.get() == 0 and self.checked_state_price.get() == 1:
            self.shop.start_web_scrapping_prices()
            messagebox.showinfo(title=f"Success",
                                message=f"Scraping done!")
        elif self.checked_state_stock.get() == 1 and self.checked_state_price.get() == 0:
            self.shop.start_web_scrapping_stocks()
            messagebox.showinfo(title=f"Success",
                                message=f"Scraping done!")
        else:
            messagebox.showinfo(title=f"Error",
                                message=f"U need to check at least one box to scrap the data")

    def new_window_add_sku(self):
        window_add = Toplevel(self.window_main)
        window_add.title("Add new SKU")
        window_add.config(width=200, height=200, pady=50, padx=50, bg=BG_COLOR)

        # label enter sku
        window_add_label_SKU = Label(window_add, bg=BG_COLOR, text="Enter SKU", font=FONT)
        window_add_label_SKU.grid(row=0, column=0, padx=10, pady=20)
        # enter SKU
        window_add_enter_SKU = Entry(window_add, width=20, font=FONT)
        window_add_enter_SKU.grid(row=0, column=1, padx=10, pady=20)

        # label enter price
        window_add_label_PRICE = Label(window_add, bg=BG_COLOR, text="Enter price", font=FONT)
        window_add_label_PRICE.grid(row=1, column=0, padx=10, pady=20)
        # enter price
        window_add_enter_PRICE = Entry(window_add, width=20, font=FONT)
        window_add_enter_PRICE.grid(row=1, column=1, padx=10, pady=20)

        # label enter STOCK
        window_add_label_STOCK = Label(window_add, bg=BG_COLOR, text="Enter stock", font=FONT)
        window_add_label_STOCK.grid(row=2, column=0, padx=10, pady=20)
        # enter STOCK
        window_add_enter_STOCK = Entry(window_add, width=20, font=FONT)
        window_add_enter_STOCK.grid(row=2, column=1, padx=10, pady=20)

        # label enter URL 1
        window_add_label_URL_1 = Label(window_add, bg=BG_COLOR, text="Enter profesmeb URL", font=FONT)
        window_add_label_URL_1.grid(row=3, column=0, padx=10, pady=20)
        # enter URL 1
        window_add_enter_URL_1 = Entry(window_add, width=20, font=FONT)
        window_add_enter_URL_1.grid(row=3, column=1, padx=10, pady=20)

        # label enter URL 2
        window_add_label_URL_2 = Label(window_add, bg=BG_COLOR, text="Enter pozmebel URL", font=FONT)
        window_add_label_URL_2.grid(row=4, column=0, padx=10, pady=20)
        # enter URL 2
        window_add_enter_URL_2 = Entry(window_add, width=20, font=FONT)
        window_add_enter_URL_2.grid(row=4, column=1, padx=10, pady=20)

        window_add_button_add = Button(window_add, font=FONT, text="Add product to database",
                                       command=lambda: self.add_new_product_to_db(window_add,
                                                                                  window_add_enter_SKU.get().upper(),
                                                                                  window_add_enter_PRICE.get(),
                                                                                  window_add_enter_STOCK.get(),
                                                                                  window_add_enter_URL_1.get(),
                                                                                  window_add_enter_URL_2.get()))
        window_add_button_add.grid(row=5, column=0, columnspan=2, padx=10, pady=20)

    def new_window_delete_SKU(self):
        window_delete = Toplevel(self.window_main)
        window_delete.title("Delete product")
        window_delete.config(width=100, height=100, pady=50, padx=50, bg=BG_COLOR)

        # label enter sku
        window_delete_label_SKU = Label(window_delete, bg=BG_COLOR,
                                        text="If u want to delete multiple rows, \nplease add more SKUs in that format\n SKU1, SKU2, SKU3",
                                        font=FONT)
        window_delete_label_SKU.grid(row=0, column=0, padx=10, pady=20)
        # enter SKU
        window_delete_enter_SKU = Entry(window_delete, width=20, font=FONT)
        window_delete_enter_SKU.grid(row=0, column=1, padx=10, pady=20)

        window_add_button_add = Button(window_delete, font=FONT, text="Delete product from database",
                                       command=lambda: self.delete_product_from_db(window_delete,
                                                                                   window_delete_enter_SKU.get().upper()))
        window_add_button_add.grid(row=1, column=0, columnspan=2, padx=10, pady=20)

    def search_product_SKU(self, sku):
        search_database = sqlite3.connect("market_competition.db")
        search_cursor = search_database.cursor()

        search_cursor.execute(
            "SELECT OUR_PRICE, PRICE_1, PRICE_2 FROM products WHERE SKU=(:SKU)", {'SKU': sku})
        show = search_cursor.fetchone()
        messagebox.showinfo(title=f"Info about {sku}",
                            message=f"Our price | Profesmeb price | Pozmebel price\n\n{show}")
        search_database.commit()
        search_cursor.close()
        search_database.close()

    def show_all_products(self):
        window_show_all_products = Toplevel(self.window_main)
        window_show_all_products.title("All database products")
        window_show_all_products.config(width=400, height=400, pady=50, padx=10, bg=BG_COLOR)

        display_db = sqlite3.connect("market_competition.db")
        display_cursor = display_db.cursor()
        display_cursor.execute(
            "SELECT SKU, OUR_PRICE, OUR_STOCK, PRICE_1, IS_HIGHER_1, DIFF_1, STOCK_1, PRICE_2, IS_HIGHER_2, DIFF_2, STOCK_2 FROM products")
        data = display_cursor.fetchall()

        display_tab = [("SKU", "OUR PRICE", "OUR STOCK", "PROFESMEB PRICE", "IS HIGHER", "DIFFERENCE", "PROFESMEB STOCK", "POZMEBEL PRICE",
                        "IS HIGHER", "DIFFERENCE", "POZMEBEL STOCK")] + data

        # Main frame
        main_frame = Frame(window_show_all_products)
        main_frame.pack(fill=BOTH, expand=1)

        # canvas
        canvas = Canvas(main_frame, width=300, height=300)

        # scrollbar_y canvas
        scrollbar_y = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
        scrollbar_y.pack(side=RIGHT, fill=Y)

        # scrollbar_x canvas
        scrollbar_x = Scrollbar(main_frame, orient=HORIZONTAL, command=canvas.xview)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        # configure canvas
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # frame canvas
        canvas_frame = Frame(canvas)

        # add frame canvas
        canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

        for i in range(len(display_tab)):
            for j in range(len(display_tab[0])):
                temp_label = Label(canvas_frame, text=display_tab[i][j], width=17, font=('Arial', 12))
                temp_label.grid(row=i, column=j)

        display_db.commit()
        display_cursor.close()
        display_db.close()

    def add_new_product_to_db(self, window, sku, price, stock, url_1, url_2):
        add_database = sqlite3.connect('market_competition.db')
        add_cursor = add_database.cursor()
        if sku != '' and price != '' and stock != '' and url_1 != '' and url_2 != '':
            add_cursor.execute(
                "INSERT INTO products (SKU, OUR_PRICE, OUR_STOCK, URL_1, URL_2) VALUES (:sku, :price, :stock, :url_1, :url_2)",
                {
                    'sku': sku,
                    'price': price,
                    'stock': stock,
                    'url_1': url_1,
                    'url_2': url_2
                }
                )
            messagebox.showinfo(title="Success", message="Successfully added a new product")
            window.destroy()
        else:
            messagebox.showerror(title="Error", message="One of the fields is empty")

        add_database.commit()
        add_cursor.close()
        add_database.close()
        self.shop.db_to_csv()

    def delete_product_from_db(self, window, sku):
        delete_database = sqlite3.connect('market_competition.db')
        delete_cursor = delete_database.cursor()
        multiple_skus = sku.split(", ")

        query = "DELETE FROM products WHERE SKU in ({seq})".format(
            seq=','.join(['?'] * len(multiple_skus)))

        if sku != '':
            delete_cursor.execute(query, multiple_skus)
            messagebox.showinfo(title="Success", message=f"Successfully deleted correct SKUs")
            window.destroy()
        else:
            messagebox.showerror(title="Error", message="U cannot leave empty field")

        delete_database.commit()
        delete_cursor.close()
        delete_database.close()
        self.shop.db_to_csv()
