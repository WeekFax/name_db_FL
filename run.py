import pymysql
from contextlib import closing
import transliterate
import random

def read_config_db():
    ans = {}
    for line in open('config_db.ini').readlines():
        field, value = line.split('=')
        field = field[:-1]
        value = value.rstrip()[2:-1]
        ans[field] = value
    return ans


def get_convert_types():
    counter = 0
    converts = []
    for line in open('config.ini', 'r').readlines():
        convert_type, percent = line.split('=')
        convert_type = convert_type[:-1]
        percent = float(percent[1:].lstrip())
        if convert_type == 'Ленин Владимир Ильич':
            converts.append([0, counter])
        elif convert_type == 'Ленин Владимир':
            converts.append([1, counter])
        elif convert_type == 'Владимир':
            converts.append([2, counter])
        elif convert_type == 'Lenin Vladimir':
            converts.append([3, counter])
        elif convert_type == 'Владимир Ленин':
            converts.append([4, counter])
        elif convert_type == 'ленин владимир':
            converts.append([5, counter])
        elif convert_type == 'владимир':
            converts.append([6, counter])
        elif convert_type == 'LENIN VLADIMIR':
            converts.append([7, counter])
        elif convert_type == 'Владимир Л.':
            converts.append([8, counter])
        elif convert_type == 'Владимир Л':
            converts.append([9, counter])
        elif convert_type == 'Vladimir':
            converts.append([10, counter])
        elif convert_type == 'ЛЕНИН ВЛАДИМИР':
            converts.append([11, counter])
        elif convert_type == 'Ленин ВЛАДИМИР':
            converts.append([12, counter])
        counter += percent
    for i in range(len(converts)):
        converts[i][1] = converts[i][1]/counter

    return converts


def convert(surname, name, patron, choosen_convert=-1):
    if choosen_convert == -1:
        converts = get_convert_types()
        rnd = random.random()
        for c in converts[::-1]:
            if rnd > c[1]:
                choosen_convert = c[0]
                break
    if choosen_convert == 0:
        return '{} {} {}'.format(surname, name, patron)
    elif choosen_convert == 1:
        return '{} {}'.format(surname, name)
    elif choosen_convert == 2:
        return '{}'.format(name)
    elif choosen_convert == 3:
        return transliterate.translit('{} {}'.format(surname, name), reversed=True)
    elif choosen_convert == 4:
        return '{} {}'.format(name, surname)
    elif choosen_convert == 5:
        return '{} {}'.format(name, surname).lower()
    elif choosen_convert == 6:
        return '{}'.format(name).lower()
    elif choosen_convert == 7:
        return transliterate.translit('{} {}'.format(surname, name), reversed=True).upper()
    elif choosen_convert == 8:
        return '{} {}.'.format(name, surname[0])
    elif choosen_convert == 9:
        return '{} {}'.format(name, surname[0])
    elif choosen_convert == 10:
        return transliterate.translit('{}'.format(name), reversed=True)
    elif choosen_convert == 11:
        return '{} {}'.format(surname, name).upper()
    elif choosen_convert == 12:
        return '{} {}'.format(surname, name.upper())


if __name__ == '__main__':
    config_db = read_config_db()

    sex = None
    while sex != 'M' and sex != 'W':
        sex = input('Выберите пол (M или W): ')
    if sex == 'M':
        gender = 1
    elif sex == 'W':
        gender = 0

    with closing(pymysql.connect(host=config_db['DB_HOST'], user=config_db['DB_USER'], db=config_db['DB_NAME'], password = config_db['DB_PASSWORD'], charset='utf8mb4')) as conn:
        repeat = True
        while repeat:
            with conn.cursor() as cursor:
                query = """SELECT * FROM names WHERE is_used = 0 and is_refused = 0 and gender = %s ORDER BY RAND() LIMIT 1"""
                cursor.execute(query, gender)
                persons = list(cursor)
                if len(persons) == 0:
                    print("Нет необработанных имен данного пола")
                    exit()
                else:
                    person = persons[0]
            choose = 'r'
            while choose == 'r':
                current = convert(person[1], person[2], person[3])
                choose = input("{} ('y'-согласиться, 'r'-перегенерировать, 'n'-отказаться): ".format(current))
                while choose != 'y' and choose != 'n' and choose != 'r':
                    choose = input("{} ('y'-согласиться, 'r'-перегенерировать, 'n'-отказаться) :".format(current))
            if choose == 'y':
                query = 'UPDATE names SET is_used = 1 WHERE id = %s'
                repeat = False
            elif choose == 'n':
                query = 'UPDATE names SET is_refused = 1 WHERE id = %s'
            with conn.cursor() as cursor:
                cursor.execute(query, person[0])
                conn.commit()

