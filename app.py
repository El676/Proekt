from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:PASS@localhost/postgres'
db = SQLAlchemy(app)

class Vacancies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    company = db.Column(db.String(255))
    city = db.Column(db.String(255))
    salary_from = db.Column(db.Integer, nullable=True)
    salary_to = db.Column(db.Integer, nullable=True)
    currency = db.Column(db.String(10), nullable=True)
    description = db.Column(db.Text)

@app.route('/')
def index():
    vacancies = Vacancies.query.all()
    return render_template('index.html', vacancies=vacancies)

@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('search')
    city = request.args.get('city')
    company = request.args.get('company')
    vacancies = Vacancies.query

    if search_query:
        vacancies = vacancies.filter(Vacancies.title.ilike(f'%{search_query}%'))
    if city:
        vacancies = vacancies.filter(Vacancies.city == city)
    if company:
        vacancies = vacancies.filter(Vacancies.company == company)

    vacancies = vacancies.all()
    return render_template('result.html', vacancies=vacancies)

if __name__ == '__main__':
    app.run(debug=True)

