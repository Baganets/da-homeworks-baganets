import sqlite3
import pandas as pd

conn = sqlite3.connect('D:/games/homework/da-homeworks-baganets/Parcing/Aromati.db')

cursor = conn.cursor()

cursor.execute('''
WITH avg_price AS (
    SELECT Aromati2.type, AVG(Aromati1.price) AS avg_price
    FROM Aromati1
    JOIN Aromati2 ON Aromati1.id = Aromati2.id
    GROUP BY Aromati2.type
)
SELECT name, (avg_price.avg_price - Aromati1.price) AS avg_price_difference
FROM Aromati1
JOIN Aromati2 ON Aromati1.id = Aromati2.id
JOIN avg_price ON Aromati2.type = avg_price.type;
''')

results = cursor.fetchall()

for row in results:
    print(row)

conn.close()