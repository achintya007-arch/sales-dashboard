import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="achu!2006@",
    database="sales_db"
)
cursor = conn.cursor()

cursor.execute("SHOW TABLES;")
print("Tables in database:")
for (table_name,) in cursor.fetchall():
    print("-", table_name)

cursor.execute("SELECT * FROM sales_data LIMIT 5;")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
