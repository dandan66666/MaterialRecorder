from flask import request, jsonify, g, Blueprint, current_app, abort
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

@mod.route('/add', methods=["POST"])
def add_record():
    json_data = request.form
    name = json_data['name']
    number = json_data['number']
    record_time = json_data['record_time']
    specifications = json_data['specifications']
    price = json_data['price']
    cursor = g.db.cursor()
    executeStr = "INSERT INTO material (name, number, record_time, specifications, price)\
                VALUES('{}', {}, {}, '{}', {})".format(name, number, record_time, specifications, price)
    try:
        cursor.execute(executeStr)
        g.db.commit()
        current_app.logger.info("Add Record (%s) Successfully.", executeStr)
        return "Ok", 200
    except Exception as e:
        current_app.logger.error("Add Record (%s) Error %s.", executeStr, e)
        return "Error", 500

@mod.route('/list')
def list_record():
    cursor = g.db.cursor()
    try:
        cursor.execute("SELECT id, name, number, record_time, specifications, price from material")
        current_app.logger.info("List Record Successfully.")
        return get_json_from_cursor(cursor)
    except Exception as e:
        current_app.logger.error("List Record Error %s.", e)
        return "Error", 500


@mod.route('/detail/<int:id>')
def get_record_detail(id):
    cursor = g.db.cursor()
    cursor.execute("SELECT id, name, number, record_time, specifications, price from material where id = {}".format(id))
    try:
        for row in cursor:
            d = {"id": row[0], "name": row[1], "number": row[2], "record_time": row[3],
                 " specifications": row[4], "price": row[5]}
            current_app.logger.info("Get Record (%d) Detail Successfully.", id)
            return jsonify(d)
    except Exception as e:
        current_app.logger.error("Get Record (%d) Detail Error %s", id, e)
        return {}, 404

@mod.route('/delete/<int:id>', methods=['DELETE'])
def delete_record(id):
    cursor = g.db.cursor()
    try:
        cursor.execute("DELETE from material where id = {}".format(id))
        g.db.commit()
        current_app.logger.info("Delete Record (%d) Successfully.", id)
        return "Ok", 200
    except Exception as e:
        current_app.logger.error("Get Record (%d) Detail Error %s", id, e)
        return "Error", 500

@mod.route('/modify', methods=['POST'])
def modify_record():
    json_data = request.form
    id = json_data['id']
    name = json_data['name']
    number = json_data['number']
    record_time = json_data['record_time']
    specifications = json_data['specifications']
    price = json_data['price']
    try:
        cursor = g.db.cursor()
        cursor.execute("UPDATE material SET name = '{}', number = {}, record_time = {}, specifications = '{}', price = {} WHERE id = {}"
                       .format(name, number, record_time, specifications, price, id))
        g.db.commit()
        current_app.logger.info("Update Record (%d) Successfully.", id)
        return "Ok", 200
    except Exception as e:
        current_app.logger.error("Update Record (%d) Detail Error %s", id, e)
        return "Error", 500

@mod.route('/search/timeRange', methods=['POST'])
def search_record_by_time_range():
    json_data = request.form
    start_time = json_data['start_time']
    end_time = json_data['end_time']
    cursor = g.db.cursor()
    try:
        cursor.execute("SELECT id, name, number, record_time, specifications, price FROM"
                       " material WHERE record_time >= {} AND record_time <= {}".format(start_time, end_time))
        result = get_json_from_cursor(cursor)
        current_app.logger.info("Search Record By TimeRange (%d) Detail Successfully", id)
        return result
    except Exception as e:
        current_app.logger.error("Search Record By TimeRange (%d) Detail Error %s", id, e)
        return "Error", 500

@mod.route('/search/name', methods=['POST'])
def search_record_by_name():
    json_data = request.form
    name = json_data['name']
    cursor = g.db.cursor()
    cursor.execute("SELECT id, name, number, record_time, specifications, price FROM"
                   " material WHERE name = '{}'".format(name))
    try:
        result = get_json_from_cursor(cursor)
        current_app.logger.info("Search Record By TimeRange (%d) Detail Successfully", id)
        return result
    except Exception as e:
        current_app.logger.error("Search Record By TimeRange (%d) Detail Error %s", id, e)
        return "Error", 500

@mod.route('/search/specifications', methods=['POST'])
def search_record_by_specifications():
    json_data = request.form
    specifications_regex = "%{}%".format(json_data['specifications'])
    cursor = g.db.cursor()
    try:
        cursor.execute("SELECT id, name, number, record_time, specifications, price FROM"
                       " material WHERE specifications LIKE '{}'".format(specifications_regex))
        result = get_json_from_cursor(cursor)
        current_app.logger.info("Search Record By TimeRange (%d) Detail Successfully", id)
        return result
    except Exception as e:
        current_app.logger.error("Search Record By TimeRange (%d) Detail Error %s", id, e)
        return "Error", 500