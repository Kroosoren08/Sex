"""
Анализ и визуализация данных магазина.
"""

import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


def orders_dataframe(orders):
    """
    Создаёт DataFrame из заказов.

    Parameters
    ----------
    orders : list
        Список заказов.

    Returns
    -------
    pandas.DataFrame
        Таблица заказов.
    """

    return pd.DataFrame(
        orders,
        columns=[
            "id",
            "client",
            "date",
            "total"
        ]
    )


def top_clients(orders, count=5):
    """
    Возвращает топ клиентов по количеству заказов.

    Parameters
    ----------
    orders : list
        Список заказов.
    count : int
        Количество клиентов.

    Returns
    -------
    pandas.Series
        Топ клиентов.
    """

    df = orders_dataframe(orders)

    if df.empty:
        return pd.Series(dtype=int)

    return (
        df.groupby("client")
        .size()
        .sort_values(ascending=False)
        .head(count)
    )


def orders_by_date(orders):
    """
    Возвращает количество заказов по датам.
    """

    df = orders_dataframe(orders)

    if df.empty:
        return pd.Series(dtype=int)

    df["date"] = pd.to_datetime(df["date"])

    return (
        df.groupby("date")
        .size()
        .sort_index()
    )


def plot_top_clients(orders):
    """Строит график топ-5 клиентов."""

    data = top_clients(orders)

    if data.empty:
        return

    data.plot(
        kind="bar",
        title="Топ-5 клиентов по количеству заказов"
    )

    plt.xlabel("Клиент")
    plt.ylabel("Количество заказов")
    plt.tight_layout()
    plt.show()


def plot_orders_by_date(orders):
    """Строит график динамики заказов."""

    data = orders_by_date(orders)

    if data.empty:
        return

    data.plot(
        kind="line",
        marker="o",
        title="Динамика заказов"
    )

    plt.xlabel("Дата")
    plt.ylabel("Количество заказов")
    plt.grid()
    plt.tight_layout()
    plt.show()


def build_client_graph(orders):
    """
    Создаёт граф клиентов.

    Клиенты соединяются, если делали заказ
    в один день.
    """

    graph = nx.Graph()

    df = orders_dataframe(orders)

    if df.empty:
        return graph

    for client in df["client"].unique():
        graph.add_node(client)

    grouped = df.groupby("date")

    for _, group in grouped:

        clients = list(group["client"])

        for i in range(len(clients)):
            for j in range(i + 1, len(clients)):
                graph.add_edge(
                    clients[i],
                    clients[j]
                )

    return graph


def plot_client_graph(orders):
    """Визуализирует граф клиентов."""

    graph = build_client_graph(orders)

    if len(graph.nodes) == 0:
        return

    nx.draw(
        graph,
        with_labels=True,
        node_size=2000
    )

    plt.title("Граф связей клиентов")
    plt.show()