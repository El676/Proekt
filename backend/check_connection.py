import psycopg2

try:
    conn = psycopg2.connect(host='localhost', dbname='postgres', user='postgres', password='PASS')
    print("Подключение к базе данных успешно")
    conn.close()
except Exception as e:
    print(f"Ошибка подключения к базе данных: {e}")
