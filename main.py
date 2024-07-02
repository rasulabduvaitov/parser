import requests
import csv


def fetch_vacancies(company_name):
    url = 'https://api.hh.ru/vacancies'
    params = {'text': f'COMPANY_NAME:{company_name}', 'per_page': 100, 'page': 0}
    response = requests.get(url, params=params)
    response.raise_for_status()  
    data = response.json()
    return data['items'], data['found']


def parse_vacancies(vacancies):
    parsed_vacancies = []
    for vacancy in vacancies:
        parsed_vacancies.append({
            'id': vacancy['id'],
            'name': vacancy['name'],
            'area': vacancy['area']['name'],
            'salary_from': vacancy['salary']['from'] if vacancy['salary'] else None,
            'salary_to': vacancy['salary']['to'] if vacancy['salary'] else None,
            'currency': vacancy['salary']['currency'] if vacancy['salary'] else None,
            'employer': vacancy['employer']['name'],
            'published_at': vacancy['published_at'],
        })
    return parsed_vacancies


def save_to_csv(vacancies, filename='db.csv'):
    fieldnames = ['id', 'name', 'area', 'salary_from', 'salary_to', 'currency', 'employer', 'published_at']
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(vacancies)


def main(company_name):
    vacancies, found = fetch_vacancies(company_name)
    parsed_vacancies = parse_vacancies(vacancies)
    save_to_csv(parsed_vacancies)
    return f"{len(parsed_vacancies)}/{found}"


if __name__ == "__main__":
    company_name = input("Enter company name: ")
    result = main(company_name)
    print(result)
