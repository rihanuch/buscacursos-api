import flask
from flask import request, jsonify
from flask import render_template
import pymongo
import json

client = pymongo.MongoClient('mongodb://localhost:27017/')
database = client['buscacursos']

collection_teachers = database['teachers']
collection_courses = database['courses']
collection_given = database['given']


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/year/<year>/<semester>', methods=['GET'])
def find_by_year(year):
    if str.isnumeric(year):
        pipeline = [
            {"$unwind": "$given"},
            {"$match": {"given.year": int(year)}},
            {"$project": {
                "_id": 0
            }}
        ]
        return jsonify(list(collection_courses.aggregate(pipeline)))
    else:
        return jsonify(list())


@app.route('/api/teacher/<teacher>', methods=['GET'])
def find_by_teacher(teacher):
    result = collection_given.find({"teachers": teacher}, {"_id": 0})
    return jsonify(list(result))


@app.route('/api/course/<course>', methods=['GET'])
def find_by_course(course):
    pipeline = [
        {"$match": {"course_id": course}},
        {"$group": {"_id": {"year": "$year", "semester": "$semester"},
                    "available": {"$sum": "$available"}, "total": {"$sum": "$total"}}},
        {"$sort": {"_id.year": 1, "_id.semester": 1}}
    ]
    result = collection_given.aggregate(pipeline)
    return jsonify(list(result))


@app.route('/course/', methods=['GET'])
def chart_course():
    legend = 'Data por semestre'
    labels = ["2018-1", "2018-2", "2019-1", "2019-2"]
    values = [10, 9, 8, 7]
    return render_template('chart.html', values=values, labels=labels, legend=legend)

app.run()
