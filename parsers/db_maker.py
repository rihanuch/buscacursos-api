import pymongo
import json

client = pymongo.MongoClient('mongodb://localhost:27017/')
database = client['buscacursos']
collection_teachers = database['teachers']
collection_given = database['given']
collection_courses = database['courses']

with open('data/ramos.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    collection_courses.insert_many(data)

with open('data/profesores.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    collection_teachers.insert_many(data)

with open('data/given.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    collection_given.insert_many(data)