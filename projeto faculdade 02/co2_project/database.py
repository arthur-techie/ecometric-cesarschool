import sqlite3


def conectar():
    return sqlite3.connect("co2.db")