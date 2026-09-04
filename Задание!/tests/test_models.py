import unittest

from models import (
    Client,
    Product,
    Order,
    recursive_sum,
    sort_orders
)


class TestModels(unittest.TestCase):

    def test_client(self):
        client = Client(
            "Иван",
            "ivan@mail.ru",
            "+79991234567",
            "Москва"
        )

        self.assertEqual(
            client.name,
            "Иван"
        )

    def test_product(self):

        product = Product(
            "Ноутбук",
            "Электроника",
            50000,
            10
        )

        self.assertEqual(
            product.total_price(2),
            100000
        )

    def test_order(self):

        product = Product(
            "Мышь",
            "Компьютеры",
            1000,
            20
        )

        order = Order(1)

        order.add_product(
            product,
            3
        )

        self.assertEqual(
            order.get_total(),
            3000
        )

    def test_recursive_sum(self):

        self.assertEqual(
            recursive_sum([1, 2, 3, 4]),
            10
        )

    def test_sort(self):

        product = Product(
            "Товар",
            "Категория",
            100,
            10
        )

        order1 = Order(
            1,
            "2026-01-01"
        )

        order1.add_product(
            product,
            5
        )

        order2 = Order(
            2,
            "2026-01-02"
        )

        order2.add_product(
            product,
            2
        )

        result = sort_orders(
            [order2, order1],
            "date"
        )

        self.assertEqual(
            result[0].order_date,
            "2026-01-01"
        )


if __name__ == "__main__":
    unittest.main()