"""
Модели приложения учёта интернет-магазина.

Содержит классы Client, Product и Order.
"""

from datetime import datetime


class Person:
    """Базовый класс человека."""

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        """Возвращает имя."""
        return self._name

    def get_info(self):
        """Возвращает информацию о человеке."""
        return self._name


class Client(Person):
    """Клиент интернет-магазина."""

    def __init__(self, name, email, phone, city):
        super().__init__(name)
        self.__email = email
        self.__phone = phone
        self.city = city

    @property
    def email(self):
        """Возвращает email клиента."""
        return self.__email

    @property
    def phone(self):
        """Возвращает телефон клиента."""
        return self.__phone

    def get_info(self):
        """Полиморфный метод получения информации."""
        return f"{self.name}, {self.email}, {self.phone}, {self.city}"


class Product:
    """Товар магазина."""

    def __init__(self, name, category, price, stock):
        self.name = name
        self.category = category
        self.price = float(price)
        self.stock = int(stock)

    def total_price(self, quantity):
        """Возвращает стоимость указанного количества товара."""
        return self.price * quantity


class Order:
    """Заказ клиента."""

    def __init__(self, client_id, order_date=None):
        self.client_id = client_id
        self.order_date = order_date or datetime.now().strftime("%Y-%m-%d")
        self.items = []

    def add_product(self, product, quantity):
        """Добавляет товар в заказ."""
        self.items.append((product, quantity))

    def get_total(self):
        """Вычисляет общую стоимость заказа."""
        return sum(
            product.total_price(quantity)
            for product, quantity in self.items
        )


def recursive_sum(numbers):
    """
    Рекурсивно вычисляет сумму списка чисел.

    Parameters
    ----------
    numbers : list
        Список чисел.

    Returns
    -------
    float
        Сумма элементов.
    """
    if not numbers:
        return 0

    return numbers[0] + recursive_sum(numbers[1:])


def sort_orders(orders, key="date"):
    ##Собственная сортировка заказов.
    result = orders.copy()

    # Сортировка пузырьком
    for i in range(len(result)):
        for j in range(0, len(result) - i - 1):

            if key == "date":
                a = result[j].order_date
                b = result[j + 1].order_date
            else:
                a = result[j].get_total()
                b = result[j + 1].get_total()

            if a > b:
                result[j], result[j + 1] = result[j + 1], result[j]

    return result