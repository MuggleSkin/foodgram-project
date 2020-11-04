import csv
import sqlite3


con = sqlite3.connect("backend/db.sqlite3")
with con:
    cur = con.cursor()
    with open(f"ingredients.csv", encoding='utf-8') as f:
        data = csv.reader(f)
        table_name = "recipes_ingredient"
        for row in data:
            sql = f"INSERT INTO {table_name}(title, dimension) VALUES{tuple(row)}"
            cur.execute(sql)
