import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="kashish",   # 🔹 Replace with your MySQL password
            database="Agriculture_Weather_db_system"   # ✅ Correct database name
        )

        # Ensure `Users` table exists and create a default admin if missing.
        try:
            cur = conn.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS Users (
              Username VARCHAR(50) PRIMARY KEY,
              Password VARCHAR(255) NOT NULL,
              Role VARCHAR(20) NOT NULL
            )
            """)

            # Insert default admin if not present
            cur.execute("SELECT COUNT(*) FROM Users WHERE Username=%s", ('admin',))
            row = cur.fetchone()
            if row is None or row[0] == 0:
                cur.execute(
                    "INSERT INTO Users (Username, Password, Role) VALUES (%s, %s, %s)",
                    ('admin', 'admin123', 'Admin')
                )
                conn.commit()
            # Insert default normal user if not present
            cur.execute("SELECT COUNT(*) FROM Users WHERE Username=%s", ('user',))
            row2 = cur.fetchone()
            if row2 is None or row2[0] == 0:
                cur.execute(
                    "INSERT INTO Users (Username, Password, Role) VALUES (%s, %s, %s)",
                    ('user', 'userpass', 'User')
                )
                conn.commit()
            cur.close()
        except mysql.connector.Error as e2:
            # Non-fatal: warn but still return the connection
            print("⚠️ Warning while ensuring Users table:", e2)

        return conn
    except mysql.connector.Error as e:
        print("❌ MySQL Connection Error:", e)
        return None
