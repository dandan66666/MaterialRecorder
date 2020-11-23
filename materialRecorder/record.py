from flask import request, jsonify, g, Blueprint
from materialRecorder.utils import get_json_from_cursor
from . import db

mod = Blueprint('record', __name__, url_prefix='/record')

@mod.before_app_request
def get_db():
    db.get_db()

@mod.after_app_request
def close_db(res):
    db.close_db()
    return res


@mod.route('/')
def hello_world():
    return 'Hello, World!'

@mod.route('/add')
def add_record():
    json_data = request.get_json()
    name = json_data['name']
    number = json_data['number']
    record_time = json_data['record_time']
    specifications = json_data['specifications']
    price = json_data['price']
    cursor = g.db.cursor()
    cursor.execute("INSERT INTO material (name, number, record_time, specifications, price)\
                VALUES('{}', {}, {}, '{}', {})".format(name, number, record_time, specifications, price))
    g.db.commit()

@mod.route('/list')
def list_record():
    cursor = g.db.cursor()
    cursor.execute("SELECT id, name, number, record_time, specifications, price from material")
    return get_json_from_cursor(cursor)

@mod.route('/detail/<int:id>')
def get_record_detail(id):
    cursor = g.db.cursor()
    cursor.execute("SELECT id, name, number, record_time, specifications, price from material where id = {}".format(id))
    for row in cursor:
        d = {"id": row[0], "name": row[1], "number": row[2], "record_time": row[3],
             " specifications": row[4], "price": row[5]}
        return jsonify(d)

@mod.route('/delete/<int:id>')
def delete_record(id):
    cursor = g.db.cursor()
    cursor.execute("DELETE from material where id = {}".format(id))
    g.db.commit()

@mod.route('/modify')
def modify_record(id):
    json_data = request.get_json()
    id = json_data['id']
    name = json_data['name']
    number = json_data['number']
    record_time = json_data['record_time']
    specifications = json_data['specifications']
    price = json_data['price']
    cursor = g.db.cursor()
    cursor.execute("UPDATE material SET name = '{}' number = {} record_time = {} specifications = '{}' price = {} WHERE id = {}"
                   .format(name, number, record_time, specifications, price, id))
    g.db.commit()

@mod.route('/search/timeRange')
def search_record_by_time_range():
    json_data = request.get_json()
    start_time = json_data['start_time']
    end_time = json_data['end_time']
    cursor = g.db.cursor()
    cursor.execute("SELECT id, name, number, record_time, specifications, price FROM"
                   " material WHERE record_time >= {} AND record_time <= {}".format(start_time, end_time))
    return get_json_from_cursor(cursor)

@mod.route('/search/name')
def search_record_by_name():
    json_data = request.get_json()
    name = json_data['name']
    cursor = g.db.cursor()
    cursor.execute("SELECT id, name, number, record_time, specifications, price FROM"
                   " material WHERE name = '{}'".format(name))
    return get_json_from_cursor(cursor)

@mod.route('/search/specifications')
def search_record_by_specifications():
    json_data = request.get_json()
    specifications_regex = "%{}%".format(json_data['specifications'])
    cursor = g.db.cursor()
    cursor.execute("SELECT id, name, number, record_time, specifications, price FROM"
                   " material WHERE specifications LIKE '{}'".format(specifications_regex))
    return get_json_from_cursor(cursor)