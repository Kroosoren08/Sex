"""
Графический интерфейс приложения.
"""

import re
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from db import Database
from import_export import (
    export_clients_csv,
    import_clients_csv,
    export_json,
    import_json
)

from analysis import (
    plot_top_clients,
    plot_orders_by_date,
    plot_client_graph
)


class ShopGUI:
    """Главное окно приложения."""

    def __init__(self, root):
        self.root = root
        self.root.title("Система учёта интернет-магазина")
        self.root.geometry("1000x650")

        self.db = Database()

        self.create_interface()

    def create_interface(self):
        """Создаёт интерфейс."""

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)

        self.clients_tab = ttk.Frame(notebook)
        self.products_tab = ttk.Frame(notebook)
        self.orders_tab = ttk.Frame(notebook)
        self.analysis_tab = ttk.Frame(notebook)

        notebook.add(
            self.clients_tab,
            text="Клиенты"
        )

        notebook.add(
            self.products_tab,
            text="Товары"
        )

        notebook.add(
            self.orders_tab,
            text="Заказы"
        )

        notebook.add(
            self.analysis_tab,
            text="Аналитика"
        )

        self.create_clients_tab()
        self.create_products_tab()
        self.create_orders_tab()
        self.create_analysis_tab()

    # ================= CLIENTS =================

    def create_clients_tab(self):
        """Создаёт вкладку клиентов."""

        frame = ttk.LabelFrame(
            self.clients_tab,
            text="Добавить клиента"
        )

        frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.client_name = tk.Entry(frame)
        self.client_email = tk.Entry(frame)
        self.client_phone = tk.Entry(frame)
        self.client_city = tk.Entry(frame)

        labels = [
            ("Имя", self.client_name),
            ("Email", self.client_email),
            ("Телефон", self.client_phone),
            ("Город", self.client_city)
        ]

        for i, (text, entry) in enumerate(labels):

            ttk.Label(
                frame,
                text=text
            ).grid(row=0, column=i)

            entry.grid(
                row=1,
                column=i,
                padx=5
            )

        ttk.Button(
            frame,
            text="Добавить",
            command=self.add_client
        ).grid(row=1, column=4, padx=10)

        ttk.Button(
            frame,
            text="Удалить",
            command=self.delete_client
        ).grid(row=1, column=5)

        ttk.Button(
            frame,
            text="Экспорт CSV",
            command=self.export_csv
        ).grid(row=1, column=6, padx=5)

        ttk.Button(
            frame,
            text="Импорт CSV",
            command=self.import_csv
        ).grid(row=1, column=7)

        self.clients_tree = ttk.Treeview(
            self.clients_tab,
            columns=(
                "id",
                "name",
                "email",
                "phone",
                "city"
            ),
            show="headings"
        )

        headings = {
            "id": "ID",
            "name": "Имя",
            "email": "Email",
            "phone": "Телефон",
            "city": "Город"
        }

        for column, title in headings.items():

            self.clients_tree.heading(
                column,
                text=title
            )

        self.clients_tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.load_clients()

    def add_client(self):
        """Добавляет клиента."""

        name = self.client_name.get()
        email = self.client_email.get()
        phone = self.client_phone.get()
        city = self.client_city.get()

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        phone_pattern = r"^\+?[0-9\s\-\(\)]{7,20}$"

        if not re.match(email_pattern, email):
            messagebox.showerror(
                "Ошибка",
                "Некорректный email."
            )
            return

        if not re.match(phone_pattern, phone):
            messagebox.showerror(
                "Ошибка",
                "Некорректный номер телефона."
            )
            return

        if not name or not city:
            messagebox.showerror(
                "Ошибка",
                "Заполните все поля."
            )
            return

        self.db.add_client(
            name,
            email,
            phone,
            city
        )

        self.load_clients()

        self.client_name.delete(0, tk.END)
        self.client_email.delete(0, tk.END)
        self.client_phone.delete(0, tk.END)
        self.client_city.delete(0, tk.END)

    def load_clients(self):
        """Загружает клиентов."""

        for item in self.clients_tree.get_children():
            self.clients_tree.delete(item)

        for client in self.db.get_clients():

            self.clients_tree.insert(
                "",
                tk.END,
                values=client
            )

    def delete_client(self):
        """Удаляет выбранного клиента."""

        selected = self.clients_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Внимание",
                "Выберите клиента."
            )
            return

        client_id = self.clients_tree.item(
            selected[0]
        )["values"][0]

        self.db.delete_client(client_id)
        self.load_clients()

    # ================= PRODUCTS =================

    def create_products_tab(self):
        """Создаёт вкладку товаров."""

        frame = ttk.LabelFrame(
            self.products_tab,
            text="Добавить товар"
        )

        frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.product_name = tk.Entry(frame)
        self.product_category = tk.Entry(frame)
        self.product_price = tk.Entry(frame)
        self.product_stock = tk.Entry(frame)

        labels = [
            ("Название", self.product_name),
            ("Категория", self.product_category),
            ("Цена", self.product_price),
            ("Количество", self.product_stock)
        ]

        for i, (text, entry) in enumerate(labels):

            ttk.Label(
                frame,
                text=text
            ).grid(row=0, column=i)

            entry.grid(
                row=1,
                column=i,
                padx=5
            )

        ttk.Button(
            frame,
            text="Добавить",
            command=self.add_product
        ).grid(row=1, column=4)

        ttk.Button(
            frame,
            text="Удалить",
            command=self.delete_product
        ).grid(row=1, column=5)

        self.products_tree = ttk.Treeview(
            self.products_tab,
            columns=(
                "id",
                "name",
                "category",
                "price",
                "stock"
            ),
            show="headings"
        )

        headings = {
            "id": "ID",
            "name": "Название",
            "category": "Категория",
            "price": "Цена",
            "stock": "На складе"
        }

        for column, title in headings.items():
            self.products_tree.heading(
                column,
                text=title
            )

        self.products_tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.load_products()

    def add_product(self):
        """Добавляет товар."""

        try:
            name = self.product_name.get()
            category = self.product_category.get()
            price = float(self.product_price.get())
            stock = int(self.product_stock.get())

            if not name or not category:
                raise ValueError(
                    "Заполните все поля."
                )

            if price < 0 or stock < 0:
                raise ValueError(
                    "Цена и количество не могут быть отрицательными."
                )

            self.db.add_product(
                name,
                category,
                price,
                stock
            )

            self.load_products()

        except ValueError as error:
            messagebox.showerror(
                "Ошибка",
                str(error)
            )

    def load_products(self):
        """Загружает товары."""

        for item in self.products_tree.get_children():
            self.products_tree.delete(item)

        for product in self.db.get_products():

            self.products_tree.insert(
                "",
                tk.END,
                values=product
            )

    def delete_product(self):
        """Удаляет товар."""

        selected = self.products_tree.selection()

        if not selected:
            return

        product_id = self.products_tree.item(
            selected[0]
        )["values"][0]

        self.db.delete_product(product_id)
        self.load_products()

    # ================= ORDERS =================

    def create_orders_tab(self):
        """Создаёт вкладку заказов."""

        frame = ttk.LabelFrame(
            self.orders_tab,
            text="Создать заказ"
        )

        frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            frame,
            text="Клиент ID"
        ).grid(row=0, column=0)

        self.order_client = tk.Entry(frame)
        self.order_client.grid(row=1, column=0)

        ttk.Label(
            frame,
            text="Товар ID"
        ).grid(row=0, column=1)

        self.order_product = tk.Entry(frame)
        self.order_product.grid(row=1, column=1)

        ttk.Label(
            frame,
            text="Количество"
        ).grid(row=0, column=2)

        self.order_quantity = tk.Entry(frame)
        self.order_quantity.grid(row=1, column=2)

        ttk.Button(
            frame,
            text="Создать заказ",
            command=self.add_order
        ).grid(row=1, column=3, padx=10)

        ttk.Button(
            frame,
            text="Обновить",
            command=self.load_orders
        ).grid(row=1, column=4)

        self.orders_tree = ttk.Treeview(
            self.orders_tab,
            columns=(
                "id",
                "client",
                "date",
                "total"
            ),
            show="headings"
        )

        headings = {
            "id": "ID",
            "client": "Клиент",
            "date": "Дата",
            "total": "Стоимость"
        }

        for column, title in headings.items():
            self.orders_tree.heading(
                column,
                text=title
            )

        self.orders_tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.load_orders()

    def add_order(self):
        """Создаёт заказ."""

        try:

            client_id = int(
                self.order_client.get()
            )

            product_id = int(
                self.order_product.get()
            )

            quantity = int(
                self.order_quantity.get()
            )

            if quantity <= 0:
                raise ValueError(
                    "Количество должно быть больше нуля."
                )

            self.db.add_order(
                client_id,
                product_id,
                quantity
            )

            self.load_orders()
            self.load_products()

            messagebox.showinfo(
                "Успешно",
                "Заказ создан."
            )

        except ValueError as error:

            messagebox.showerror(
                "Ошибка",
                str(error)
            )

    def load_orders(self):
        """Загружает заказы."""

        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)

        for order in self.db.get_orders():

            self.orders_tree.insert(
                "",
                tk.END,
                values=order
            )

    # ================= ANALYSIS =================

    def create_analysis_tab(self):
        """Создаёт вкладку аналитики."""

        ttk.Label(
            self.analysis_tab,
            text="Анализ данных магазина",
            font=("Arial", 18)
        ).pack(pady=30)

        ttk.Button(
            self.analysis_tab,
            text="Топ-5 клиентов",
            command=self.show_top_clients
        ).pack(pady=10)

        ttk.Button(
            self.analysis_tab,
            text="Динамика заказов",
            command=self.show_orders_graph
        ).pack(pady=10)

        ttk.Button(
            self.analysis_tab,
            text="Граф клиентов",
            command=self.show_client_graph
        ).pack(pady=10)

        ttk.Button(
            self.analysis_tab,
            text="Экспорт JSON",
            command=self.export_json_data
        ).pack(pady=10)

    def show_top_clients(self):
        """Показывает топ клиентов."""

        orders = self.db.get_orders()

        plot_top_clients(orders)

    def show_orders_graph(self):
        """Показывает динамику заказов."""

        orders = self.db.get_orders()

        plot_orders_by_date(orders)

    def show_client_graph(self):
        """Показывает граф клиентов."""

        orders = self.db.get_orders()

        plot_client_graph(orders)

    # ================= IMPORT / EXPORT =================

    def export_csv(self):
        """Экспортирует клиентов в CSV."""

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV files", "*.csv")
            ]
        )

        if filename:
            export_clients_csv(
                self.db.get_clients(),
                filename
            )

    def import_csv(self):
        """Импортирует клиентов из CSV."""

        filename = filedialog.askopenfilename(
            filetypes=[
                ("CSV files", "*.csv")
            ]
        )

        if filename:

            try:

                clients = import_clients_csv(
                    filename
                )

                for client in clients:

                    self.db.add_client(
                        client["name"],
                        client["email"],
                        client["phone"],
                        client["city"]
                    )

                self.load_clients()

            except Exception as error:

                messagebox.showerror(
                    "Ошибка",
                    str(error)
                )

    def export_json_data(self):
        """Экспортирует данные в JSON."""

        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[
                ("JSON files", "*.json")
            ]
        )

        if not filename:
            return

        data = {
            "clients": self.db.get_clients(),
            "products": self.db.get_products(),
            "orders": self.db.get_orders()
        }

        export_json(data, filename)


if __name__ == "__main__":
    root = tk.Tk()

    app = ShopGUI(root)

    root.mainloop()