#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os.path
import pathlib


def add_prod(products, name, price, shope):
    """
    Добавить данные о товаре.
    """
    products.append(
        {
            "name": name,
            "price": price,
            "shope": shope,
        }
    )
    return products


def show_list(products):
    """
    Вывести список товаров
    """
    if products:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 5,
            '-' * 20,
            '-' * 14,
            '-' * 17
        )
        print(line)
        print(
            '| {:^5} | {:^20} | {:^14} | {:^17} |'.format(
                "№",
                "Название товара",
                "Цена",
                "Название магазина"
            )
        )
        print(line)

        # Вывести данные о всех товарах.
        for idx, product in enumerate(products, 1):
            print(
                '| {:>5} | {:<20} | {:<14.2f} | {:>17} |'.format(
                    idx,
                    product.get('name', ''),
                    product.get('price', 0),
                    product.get('shope', '')
                )
            )
        print(line)
    else:
        print("Список товаров пуст.")


def show_selected(products, pr):
    """
    Проверить наличие товара
    """
    # Сформировать список товаров.
    result = [product for product in products if pr == product.get('name', '')]

    # Возвратить список выбранных товаров.
    return result


def save_products(file_name, products):
    """
    Сохранение товаров
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(products, fout, ensure_ascii=False, indent=4)
    directory = pathlib.Path.cwd().joinpath(file_name)
    directory.replace(pathlib.Path.home().joinpath(file_name))


def load_products(file_name):
    """
    Загрузить товары
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("products")
    parser.add_argument(
        "--version",
        action="version",
        help="The main parser",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления товара.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new product"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="The product's name"
    )
    add.add_argument(
        "-p",
        "--price",
        type=float,
        action="store",
        help="The product's price"
    )
    add.add_argument(
        "-sh",
        "--shope",
        action="store",
        required=True,
        help="The product's shope"
    )

    # Создать субпарсер для отображения всех товаров.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all products"
    )

    # Создать субпарсер для выбора товаров.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the products"
    )
    select.add_argument(
        "-s",
        "--select",
        action="store",
        required=True,
        help="The required select"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Загрузить все продукты из файла, если файл существует.
    is_dirty = False
    if os.path.exists(args.filename):
        products = load_products(args.filename)
    else:
        products = []

    # Добавить товар.
    if args.command == "add":
        products = add_prod(
            products,
            args.name,
            args.price,
            args.shope
        )
        is_dirty = True

    # Отобразить все товары.
    elif args.command == "display":
        show_list(products)

    # Выбрать требуемый товар.
    elif args.command == "select":
        selected = show_selected(products, args.select)
        show_list(selected)

    # Сохранить данные в файл, если список товаров был изменен.
    if is_dirty:
        save_products(args.filename, products)


if __name__ == '__main__':
    main()
