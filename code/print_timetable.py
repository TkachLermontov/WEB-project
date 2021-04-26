import argparse
import csv
import requests
import sys


def find_organization(address):
    geocoder_request = f'http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=' \
                       f'{address}&format=json'
    response = requests.get(geocoder_request)

    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_coodrinates = toponym_coodrinates.split(' ')
        toponym_coodrinates = ','.join(toponym_coodrinates)
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    search_params = {
        "apikey": api_key,
        "text": "парикмахерская",
        "lang": "ru_RU",
        "ll": toponym_coodrinates,
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)

    if response:
        json_response = response.json()
        organization = json_response["features"][0]
        org_address = organization["properties"]["CompanyMetaData"]["address"]
        return org_address
    else:
        print("Ошибка выполнения запроса!")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)


def execute_from_database(file_name, ids=True, names=True, numbers=True, dates=True):
    # Импорт библиотеки
    import sqlite3

    # Подключение к БД
    con = sqlite3.connect("db/timetable.db")

    # Создание курсора
    cur = con.cursor()

    # Выполнение запроса и получение всех результатов
    result = cur.execute("""SELECT * FROM clients""").fetchall()

    lst = list()

    # Делаем массив со словарями с данными из базы данных
    for cor in result:
        dic = dict()
        for i in range(len(cor)):
            if i == 0 and ids:
                dic['id'] = cor[i]
            if i == 1 and names:
                dic['name'] = cor[i]
            if i == 2 and numbers:
                dic['number'] = cor[i]
            if i == 3 and dates:
                dic['data'] = cor[i]
        lst.append(dic)
    return file_name[0], lst


# Используем консоль для получения аргументов
parser = argparse.ArgumentParser()
parser.add_argument('file_name', type=str, nargs=1,
                    help='name for css file, which will be generated in \'generated\' fold. '
                         '!!! Should be written without file extension !!!')
parser.add_argument('--no-id', action='store_const', const=False, default=True, dest='id',
                    help='data\'ll be taken from database without clients\' id')
parser.add_argument('--no-name', action='store_const', const=False, default=True, dest='name',
                    help='data\'ll be taken from database without clients\' names')
parser.add_argument('--no-number', action='store_const', const=False, default=True, dest='number',
                    help='data\'ll be taken from database without clients\' numbers')
parser.add_argument('--no-date', action='store_const', const=False, default=True, dest='date',
                    help='data\'ll be taken from database without clients\' haircut dates')
parser.add_argument('--address', type=str, nargs='+', default=False,
                    help='data\'ll be taken from database without clients\' id')
args = parser.parse_args()

if args.address:
    address_stroke = find_organization('""'.join(args.address))
    with open('generated\\address.txt', 'w') as fi:
        fi.write(address_stroke)


file, data = execute_from_database(args.file_name, args.id, args.name, args.number, args.date)
file = 'generated\\' + file + '.csv'
with open(file, 'w', newline='') as f:
    writer = csv.DictWriter(
        f, fieldnames=list(data[0].keys()),
        delimiter='-')
    writer.writeheader()
    for d in data:
        writer.writerow(d)
