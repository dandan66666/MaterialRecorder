# coding=utf-8
from flask import jsonify
from functools import reduce
import types
from .errorCode import ErrorCode

def get_json_from_cursor(cursor):
    result = []
    for row in cursor:
        d = {"id": row[0], "name": row[1], "number": row[2], "record_time": row[3],
             "specifications": row[4], "price": row[5]}
        result.append(d)
    return jsonify(result)

def make_record_response(data, code=ErrorCode.Success):

    @staticmethod
    def getErrorMsg(code):
        errorMsgDict = {
            ErrorCode.RecordNotExist : 'Record Do Not Exist',
            ErrorCode.Success: 'Success',
            ErrorCode.ChangeNameForbidden: 'Change Name Forbidden',
            2: 'Server Internal Error',
            3: ''
        }
        return errorMsgDict.get(code, 'Wrong Error Code')

    error_code, error_msg = code, getErrorMsg(code)
    # 无需返回数据仅返回错误码
    if data is None:
        return jsonify({'error_code': error_code, 'error_msg': error_msg})

    records = [data] if type(data) is types.DictType else data
    total_price = reduce(lambda r1, r2: r1.price+r2.price, records)
    total_records = len(records)
    return jsonify({'error_code': error_code, 'error_msg': error_msg,
                    'total_price': total_price, 'total_records': total_records, 'records': records})

class RecordSql:
    @staticmethod
    def search_by_time_range(json_data):
        start_time = json_data['start_time']
        end_time = json_data['end_time']
        return "SELECT id, name, number, record_time, specifications, price FROM"+\
                           " material WHERE record_time >= {} AND record_time <= {}".format(start_time, end_time)

    @staticmethod
    def search_by_name(json_data):
        name = json_data['name']
        return "SELECT id, name, number, record_time, specifications, price FROM"+\
                       " material WHERE name = '{}'".format(name)

    @staticmethod
    def search_by_specifications(json_data):
        specifications_regex = "%{}%".format(json_data['specifications'])
        return "SELECT id, name, number, record_time, specifications, price FROM"+\
                           " material WHERE specifications LIKE '{}'".format(specifications_regex)

    @staticmethod
    def modify_record(json_data):
        id = json_data['id']
        name = json_data['name']
        number = json_data['number']
        record_time = json_data['record_time']
        specifications = json_data['specifications']
        price = json_data['price']
        return "UPDATE material SET name = '{}', number = {}, record_time = {}, specifications = '{}', price = {} WHERE id = {}"\
        .format(name, number, record_time, specifications, price, id)

    @staticmethod
    def delete_record(id):
        return "DELETE from material where id = {}".format(id)

    @staticmethod
    def add_record(json_data):
        name = json_data['name']
        number = json_data['number']
        record_time = json_data['record_time']
        specifications = json_data['specifications']
        price = json_data['price']
        return "INSERT INTO material (name, number, record_time, specifications, price)\
                    VALUES('{}', {}, {}, '{}', {})".format(name, number, record_time, specifications, price)

    @staticmethod
    def get_record_detail(id):
        return "SELECT id, name, number, record_time, specifications, price from material where id = {}".format(id)

    @staticmethod
    def list_record():
        return "SELECT id, name, number, record_time, specifications, price from material"