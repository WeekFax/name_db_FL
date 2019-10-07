import json
import pymysql
import requests
import random
from contextlib import closing


# w_name = [name[:-1] for name in open('baseWomenName.txt', 'r')]
# w_fam = [name[:-1] for name in open('baseWomenFam.txt', 'r')]
# w_otec = [name[:-1] for name in open('baseWomenOtec.txt', 'r')]
#
#
# people = []
# while len(people) < 100000:
#     person = [
#         w_name[random.randint(0, len(w_name) - 1)],
#         w_fam[random.randint(0, len(w_fam) - 1)],
#         w_otec[random.randint(0, len(w_otec) - 1)],
#         0,
#         0,
#         0
#     ]
#     if person not in people:
#         people.append(person)

with closing(pymysql.connect(host='localhost', user='root', db='name_db', charset='utf8mb4')) as conn:
    with conn.cursor() as cursor:
        query = """select * from names where surname like '%(%'"""
        cursor.execute(query)
        persons = [[per[1].split(' ')[0],per[0]] for per in list(cursor)]
    for pers in persons:
        with conn.cursor() as cursor:
            query = 'update names set surname = %s where id = %s'
            cursor.execute(query, pers)
            conn.commit()

