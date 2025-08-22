import sqlite3
import os

db_path = os.path.join("/home/zcemg08/PycharmProjects/effici/data/output", "simulations.db")
print(db_path)
con = sqlite3.connect(db_path)
# Дальше можно создавать таблицы и работать с данными
con.close()