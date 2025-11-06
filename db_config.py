import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysql",   # 🔹 Replace with your MySQL password
            database="Agriculture_Weather_db_system"   # ✅ Correct database name
        )
        return conn
    except mysql.connector.Error as e:
        print("❌ MySQL Connection Error:", e)
        return None
