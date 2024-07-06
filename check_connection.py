import psycopg2

try:
    # Подключение к базе данных
    conn = psycopg2.connect(host='localhost', dbname='postgres', user='postgres', password='PASS')
    print("Подключение к базе данных успешно")
    conn.close()
except Exception as e:
    print(f"Ошибка подключения к базе данных: {e}")
