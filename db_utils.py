import pandas as pd
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG   # ⭐ NEW

TABLE_NAME = "sales_data"

def get_connection():
    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        port=3306,
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        ssl_disabled=False
    )

def import_csv_to_mysql(csv_file):
    df = pd.read_csv(csv_file)

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                order_id INT PRIMARY KEY,
                order_date DATE,
                product_name VARCHAR(255),
                quantity INT,
                price DECIMAL(10,2)
            )
        """)
        conn.commit()

        cursor.execute(f"DELETE FROM {TABLE_NAME}")
        conn.commit()

        rows = []
        for _, row in df.iterrows():
            rows.append((
                int(row['order_id']),
                row['order_date'],
                str(row['product_name']),
                int(row['quantity']),
                float(row['price'])
            ))

        insert_sql = f"""INSERT INTO {TABLE_NAME}
                        (order_id, order_date, product_name, quantity, price)
                        VALUES (%s, %s, %s, %s, %s)"""

        if rows:
            cursor.executemany(insert_sql, rows)
            conn.commit()

        print("✅ Data imported into MySQL successfully!")

    except Error as e:
        print("MySQL error during import:", e)
        raise
    finally:
        if conn:
            conn.close()

def load_data_from_mysql():
    conn = None
    try:
        conn = get_connection()
        df = pd.read_sql(f"SELECT * FROM {TABLE_NAME}", conn, parse_dates=["order_date"]) #type: ignore
        return df
    except Error as e:
        print("MySQL error during load:", e)
        raise
    finally:
        if conn:
            conn.close()