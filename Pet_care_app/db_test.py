import psycopg2

try:
    conn = psycopg2.connect(
        host="172.17.235.199",
        database="pet_care",
        user="wufy1234",
        password="wufy1234",
        port=5432
    )
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")