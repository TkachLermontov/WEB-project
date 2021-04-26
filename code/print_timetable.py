import argparse
import csv


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
parser.add_argument('--address', type=str, nargs='+',
                    help='data\'ll be taken from database without clients\' id')
args = parser.parse_args()

""" Напиши в консоль, например: 'py print_timetable.py test_file --address город Екатеринбург, улица Сахалинская 24'
    В args.address будет храниться массив с адресом.
    При помощи ' ' '.join(args.address) ' его можно переделать в строку с адресом"""
print(' '.join(args.address))

file, data = execute_from_database(args.file_name, args.id, args.name, args.number, args.date)
file = 'generated\\' + file + '.csv'
with open(file, 'w', newline='') as f:
    writer = csv.DictWriter(
        f, fieldnames=list(data[0].keys()),
        delimiter='-')
    writer.writeheader()
    for d in data:
        writer.writerow(d)
