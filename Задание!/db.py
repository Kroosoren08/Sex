"""
Работа с базой данных SQLite.
"""

import sqlite3


class Database:
    """Класс для работы с SQLite."""

    def __init__(self, database="shop.db"):
        self.database = database
        self.create_tables()

    def connect(self):
        """Создаёт подключение к базе."""
        return sqlite3.connect(self.database)

    def create_tables(self):
        """Создаёт необходимые таблицы."""

        try:
            with self.connect() as conn:

                cursor = conn.cursor()

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS clients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        city TEXT NOT NULL
                    )
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        category TEXT NOT NULL,
                        price REAL NOT NULL,
                        stock INTEGER NOT NULL
                    )
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_id INTEGER NOT NULL,
                        order_date TEXT NOT NULL,
                        total REAL DEFAULT 0,
                        FOREIGN KEY(client_id)
                        REFERENCES clients(id)
                    )
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS order_items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        order_id INTEGER NOT NULL,
                        product_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL,
                        FOREIGN KEY(order_id)
                        REFERENCES orders(id),
                        FOREIGN KEY(product_id)
                        REFERENCES products(id)
                    )
                """)

                conn.commit()

        except sqlite3.Error as error:
            print("Ошибка создания БД:", error)

    # ---------------- CLIENTS ----------------

    def add_client(self, name, email, phone, city):
        """Добавляет клиента."""

        try:
            with self.connect() as conn:
                conn.execute(
                    """
                    INSERT INTO clients
                    (name, email, phone, city)
                    VALUES (?, ?, ?, ?)
                    """,
                    (name, email, phone, city)
                )
                conn.commit()

        except sqlite3.Error as error:
            print("Ошибка добавления клиента:", error)

    def get_clients(self):
        """Возвращает список клиентов."""

        with self.connect() as conn:
            return conn.execute(
                "SELECT * FROM clients ORDER BY id DESC"
            ).fetchall()

    def delete_client(self, client_id):
        """Удаляет клиента."""

        try:
            with self.connect() as conn:
                conn.execute(
                    "DELETE FROM clients WHERE id = ?",
                    (client_id,)
                )
                conn.commit()

        except sqlite3.Error as error:
            print("Ошибка удаления:", error)

    # ---------------- PRODUCTS ----------------

    def add_product(self, name, category, price, stock):
        """Добавляет товар."""

        try:
            with self.connect() as conn:
                conn.execute(
                    """
                    INSERT INTO products
                    (name, category, price, stock)
                    VALUES (?, ?, ?, ?)
                    """,
                    (name, category, price, stock)
                )
                conn.commit()

        except sqlite3.Error as error:
            print("Ошибка добавления товара:", error)

    def get_products(self):
        """Возвращает список товаров."""

        with self.connect() as conn:
            return conn.execute(
                "SELECT * FROM products ORDER BY id DESC"
            ).fetchall()

    def delete_product(self, product_id):
        """Удаляет товар."""

        try:
            with self.connect() as conn:
                conn.execute(
                    "DELETE FROM products WHERE id = ?",
                    (product_id,)
                )
                conn.commit()

        except sqlite3.Error as error:
            print("Ошибка удаления:", error)

    # ---------------- ORDERS ----------------

    def add_order(self, client_id, product_id, quantity):
        """Создаёт заказ."""

        try:
            with self.connect() as conn:

                cursor = conn.cursor()

                product = cursor.execute(
                    "SELECT price, stock FROM products WHERE id = ?",
                    (product_id,)
                ).fetchone()

                if product is None:
                    raise ValueError("Товар не найден.")

                price, stock = product

                if quantity > stock:
                    raise ValueError("Недостаточно товара на складе.")

                total = price * quantity

                cursor.execute(
                    """
                    INSERT INTO orders
                    (client_id, order_date, total)
                    VALUES (?, date('now'), ?)
                    """,
                    (client_id, total)
                )

                order_id = cursor.lastrowid

                cursor.execute(
                    """
                    INSERT INTO order_items
                    (order_id, product_id, quantity)
                    VALUES (?, ?, ?)
                    """,
                    (order_id, product_id, quantity)
                )

                cursor.execute(
                    """
                    UPDATE products
                    SET stock = stock - ?
                    WHERE id = ?
                    """,
                    (quantity, product_id)
                )

                conn.commit()

        except sqlite3.Error as error:
            print("Ошибка заказа:", error)

    def get_orders(self):
        """Возвращает все заказы."""

        with self.connect() as conn:
            return conn.execute("""
                SELECT
                    orders.id,
                    clients.name,
                    orders.order_date,
                    orders.total
                FROM orders
                JOIN clients
                ON clients.id = orders.client_id
                ORDER BY orders.id DESC
            """).fetchall()