"""
Импорт и экспорт данных CSV и JSON.
"""

import csv
import json


def export_clients_csv(clients, filename):
    """Экспорт клиентов в CSV."""

    with open(filename, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Имя",
            "Email",
            "Телефон",
            "Город"
        ])

        writer.writerows(clients)


def import_clients_csv(filename):
    """Импорт клиентов из CSV."""

    clients = []

    with open(filename, "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:
            clients.append({
                "name": row["Имя"],
                "email": row["Email"],
                "phone": row["Телефон"],
                "city": row["Город"]
            })

    return clients


def export_json(data, filename):
    """Экспорт данных в JSON."""

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


def import_json(filename):
    """Импорт данных из JSON."""

    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)