from application.salary import calculate_salary
from application.db import people
from datetime import datetime


def get_date():
    date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    return date


if __name__ == '__main__':
    print(get_date())
    calculate_salary()
    people.get_employees()
