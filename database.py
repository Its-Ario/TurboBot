import sqlite3
import json

def create_database():
    conn = sqlite3.connect('Data/database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS key_value_store
                        (key TEXT PRIMARY KEY, value TEXT)''')
    conn.commit()
    conn.close()
def read_database():
    conn = sqlite3.connect('Data/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM key_value_store")
    rows = cursor.fetchall()
    conn.close()
    return {key: json.loads(value) for key, value in rows}
def write_database(data_dict):
    conn = sqlite3.connect('Data/database.db')
    cursor = conn.cursor()
    for key, value in data_dict.items():
        cursor.execute("INSERT OR REPLACE INTO key_value_store (key, value) VALUES (?, ?)",
                        (key, json.dumps(value, default=list)))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()