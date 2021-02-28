#coding: utf-8
from flask import request, jsonify, g, Blueprint, current_app, abort
from .utils import make_record_response, get_json_from_cursor, RecordSql, get_valid_float, get_valid_integer
from .errorCode import ErrorCode
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

    cursor = g.db.cursor()
    executeStr = RecordSql.add(json_data)
    print(executeStr)
    if executeStr is None:
        make_record_response(None, ErrorCode.WrongInput)
    try:
        cursor.execute(executeStr)
        g.db.commit()
        current_app.logger.info("Add Record {%s} Successfully.", executeStr)
        return make_record_response(None)
    except Exception as e:
        current_app.logger.error("Add Record {%s} Error %s.", executeStr, e)
        return make_record_response(None, ErrorCode.ServerInternalError)
    finally:
        cursor.close()

@mod.route('/list', methods=['POST'])
def list_record():
    json_data = request.form
    page_num = get_valid_integer(json_data['page_num'])
    limit = page_size = get_valid_integer(json_data['page_size'])
    offset = (page_num-1)*page_size
    cursor = g.db.cursor()
    sqlStr = RecordSql.list(json_data)
    if sqlStr is None:
        return make_record_response(None, ErrorCode.WrongInput)
    sqlStr += " LIMIT {} OFFSET {}".format(limit, offset)
    print(sqlStr)
    try:
        cursor.execute(sqlStr)
        result = make_record_response(get_json_from_cursor(cursor))
        current_app.logger.info("List Record {%s} Successfully", sqlStr)
        return result
    except Exception as e:
        current_app.logger.error("List Record {%s} Error %s", sqlStr, e)
        return make_record_response(None, ErrorCode.ServerInternalError)
    finally:
        cursor.close()

# @mod.route('/list')
# def list_record():
#     cursor = g.db.cursor()
#     try:
#         cursor.execute(RecordSql.list_record())
#         current_app.logger.info("List Record Successfully.")
#         return make_record_response(get_json_from_cursor(cursor))
#     except Exception as e:
#         current_app.logger.error("List Record Error %s.", e)
#         return make_record_response(None, ErrorCode.ServerInternalError)
#     finally:
#         cursor.close()


@mod.route('/detail/<int:id>')
def get_record_detail(id):
    cursor = g.db.cursor()
    executeSql = RecordSql.get_detail(id)
    if executeSql is None:
        current_app.logger.error("Get Record {%d} Detail Wrong Input", id)
        return make_record_response(None, ErrorCode.WrongInput)
    try:
        cursor.execute(executeSql)
        result = get_json_from_cursor(cursor)
        if len(result) == 0:
            return make_record_response(result, ErrorCode.RecordNotExist)
        elif len(result) > 1:
            return make_record_response(None, ErrorCode.MultiRecords)
        current_app.logger.info("Get Record {%d} Detail Successfully.", id)
        return make_record_response(result)
    except Exception as e:
        current_app.logger.error("Get Record {%d} Detail Error %s", id, e)
        return make_record_response([], 2)
    finally:
        cursor.close()

@mod.route('/delete/<int:id>', methods=['DELETE'])
def delete_record(id):
    cursor = g.db.cursor()
    executeSql = RecordSql.delete(id)
    if executeSql is None:
        current_app.logger.error("Delete Record {} Wrong Input", id)
        return make_record_response(None, ErrorCode.WrongInput)
    try:
        cursor.execute(executeSql)
        g.db.commit()
        if cursor.rowcount == 0:
            return make_record_response(None, ErrorCode.RecordNotExist)
        current_app.logger.info("Delete Record {%d} Successfully.", id)
        return make_record_response(None)
    except Exception as e:
        current_app.logger.error("Get Record {%d} Detail Error %s", id, e)
        return make_record_response(None, ErrorCode.ServerInternalError)
    finally:
        cursor.close()

@mod.route('/modify', methods=['POST'])
def modify_record():
    json_data = request.form
    id = json_data['id']
    try:
        cursor = g.db.cursor()
        if get_valid_integer(id) is None:
            return make_record_response(None, ErrorCode.WrongInput)
        # 修改前先判断该记录存在且没有改名字，否则返回错误码
        cursor.execute(RecordSql.get_detail(id))
        record = cursor.fetchall()
        if len(record) == 0:
            return make_record_response(None, ErrorCode.RecordNotExist)
        elif record[0]['name'] != json_data['name']:
            return make_record_response(None, ErrorCode.ChangeNameForbidden)
        executeSql = RecordSql.modify(json_data)
        if executeSql is None:
            return make_record_response(None, ErrorCode.WrongInput)
        cursor.execute(executeSql)
        g.db.commit()
        current_app.logger.info("Update Record {%d} Successfully.", id)
        return make_record_response(None)
    except Exception as e:
        current_app.logger.error("Update Record {%d} Detail Error %s", id, e)
        return make_record_response(None, ErrorCode.ServerInternalError)
    finally:
        cursor.close()

