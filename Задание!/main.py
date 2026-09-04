"""
Точка входа в приложение.
"""

import tkinter as tk

from gui import ShopGUI


def main():
    """Запускает приложение."""

    root = tk.Tk()

    ShopGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()