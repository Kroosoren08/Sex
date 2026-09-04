import unittest

from analysis import (
    top_clients,
    orders_by_date
)


class TestAnalysis(unittest.TestCase):

    def setUp(self):

        self.orders = [
            (1, "Иван", "2026-01-01", 1000),
            (2, "Иван", "2026-01-01", 2000),
            (3, "Пётр", "2026-01-02", 500),
            (4, "Иван", "2026-01-03", 1500),
            (5, "Пётр", "2026-01-03", 700)
        ]

    def test_top_clients(self):

        result = top_clients(
            self.orders
        )

        self.assertEqual(
            result.iloc[0],
            3
        )

        self.assertEqual(
            result.index[0],
            "Иван"
        )

    def test_orders_by_date(self):

        result = orders_by_date(
            self.orders
        )

        self.assertEqual(
            result["2026-01-01"],
            2
        )


if __name__ == "__main__":
    unittest.main()