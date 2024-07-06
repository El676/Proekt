import requests
import psycopg2

DB_HOST = 'localhost'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASS = 'PASS'


HH_API_URL = 'https://api.hh.ru/vacancies'
HEADERS = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

def create_tables():
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            company VARCHAR(255),
            city VARCHAR(255),
            salary_from INTEGER,
            salary_to INTEGER,
            currency VARCHAR(10),
            description TEXT
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

def fetch_vacancies(params=None):
    response = requests.get(HH_API_URL, headers=HEADERS, params=params)
    
    if response.status_code != 200:
        print(f"Ошибка: статус код {response.status_code}")
        print(f"Текст ответа: {response.text}")
        return None

    try:
        response.encoding = 'utf-8'
        return response.json()
    except requests.exceptions.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}")
        print(f"Текст ответа: {response.text}")
        return None
    except UnicodeDecodeError as e:
        print(f"Ошибка декодирования строки: {e}")
        print(f"Текст ответа: {response.text.encode('latin1')}")
        return None

def save_vacancies(vacancies):
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    cur = conn.cursor()
    for vacancy in vacancies:
        title = vacancy['name']
        company = vacancy['employer']['name']
        city = vacancy['area']['name']
        salary_from = vacancy['salary']['from'] if vacancy['salary'] else None
        salary_to = vacancy['salary']['to'] if vacancy['salary'] else None
        currency = vacancy['salary']['currency'] if vacancy['salary'] else None
        description = vacancy['snippet']['requirement']

        cur.execute('''
            INSERT INTO vacancies (title, company, city, salary_from, salary_to, currency, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (title, company, city, salary_from, salary_to, currency, description))
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    create_tables()
    params = {
        'text': '',
        'area': '113',  
        'per_page': 20
    }
    data = fetch_vacancies(params)
    if data and 'items' in data:
        save_vacancies(data['items'])
    else:
        print("Нет данных для сохранения")
