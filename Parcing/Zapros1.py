import sqlite3

conn = sqlite3.connect('D:/games/homework/da-homeworks-baganets/Parcing/Aromati.db')

cursor = conn.cursor()

cursor.execute('''
SELECT type, AVG(price) as avg_price
FROM Aromati1
JOIN Aromati2 ON Aromati1.id = Aromati2.id
GROUP BY Aromati2.type;
''')

results = cursor.fetchall()

for row in results:
    print(f' Формат продукта: {row[0]}, Средняя цена: {row[1]}')

conn.close()

