# coding=utf-8
from flask import jsonify
from functools import reduce
import types
from .errorCode import ErrorCode

def get_valid_integer(arg):
    if type(arg) == int:
        return arg
    if type(arg) == str and arg.isdigit():
        return int(arg)
    return None

def get_valid_float(arg):
    if type(arg) == float:
        return arg
    if type(arg) == str and arg.isdigit():
        return float(arg)
    return None

def get_json_from_cursor(cursor):
    result = []
    for row in cursor:
        d = {"id": row[0], "name": row[1], "number": row[2], "record_time": row[3],
             "specifications": row[4], "price": row[5]}
        result.append(d)
    return result

def make_record_response(data, code=ErrorCode.Success):

    def getErrorMsg(code):
        errorMsgDict = {
            ErrorCode.RecordNotExist : 'Record Do Not Exist',
            ErrorCode.Success: 'Success',
            ErrorCode.ChangeNameForbidden: 'Change Name Forbidden',
            ErrorCode.ServerInternalError: 'Server Internal Error',
            ErrorCode.MultiRecords: 'MultiRecord',
            ErrorCode.WrongInput: 'WrongInput',
            ErrorCode.SearchTypeNotExist: 'Search Type Not Exist'
        }
        return errorMsgDict.get(code, 'Wrong Error Code')

    error_code, error_msg = code.value, code.name
    # 无需返回数据仅返回错误码
    if data is None:
        return jsonify({'error_code': error_code, 'error_msg': error_msg})

    records = [data] if type(data) == dict else data
    total_price = 0
    for record in records:
        total_price += record['price']
    # if len(records) >= 2:
    #     total_price = reduce(lambda r1, r2: r1.price+r2.price, records)
    total_records = len(records)
    result =  jsonify({'error_code': error_code, 'error_msg': error_msg,
                    'total_price': total_price, 'total_records': total_records, 'records': records})
    return result

class RecordSql:
    @staticmethod
    def list_by_time_range(json_data):
        start_time = get_valid_integer(json_data['start_time'])
        end_time = get_valid_integer(json_data['end_time'])
        if start_time is None or end_time is None:
            return None
        return "SELECT id, name, number, record_time, specifications, price FROM"+\
                           " material WHERE record_time >= {} AND record_time <= {}".format(start_time, end_time)

    @staticmethod
    def list_by_name(json_data):
        name = json_data['name']
        if name is None:
            return None
        return "SELECT id, name, number, record_time, specifications, price FROM"+\
                       " material WHERE name = '{}'".format(name)

    @staticmethod
    def list_by_specifications(json_data):
        if json_data['specifications'] is None:
            return None
        specifications_regex = "%{}%".format(json_data['specifications'])
        return "SELECT id, name, number, record_time, specifications, price FROM"+\
                           " material WHERE specifications LIKE '{}'".format(specifications_regex)

    @staticmethod
    def modify(json_data):
        id = get_valid_integer(json_data['id'])
        name = json_data['name']
        number = get_valid_integer(json_data['number'])
        record_time = get_valid_integer(json_data['record_time'])
        specifications = json_data['specifications']
        price = get_valid_float(json_data['price'])
        if id is None or name is None or number is None or record_time is None \
            or specifications is None or price is None:
            return None
        return "UPDATE material SET name = '{}', number = {}, record_time = {}, specifications = '{}', price = {} WHERE id = {}"\
        .format(name, number, record_time, specifications, price, id)

    @staticmethod
    def delete(id):
        return "DELETE from material where id = {}".format(id)

    @staticmethod
    def add(json_data):
        name = json_data['name']
        number = get_valid_integer(json_data['number'])
        record_time = get_valid_integer(json_data['record_time'])
        specifications = json_data['specifications']
        price = get_valid_float(json_data['price'])
        if name is None or number is None or record_time is None \
            or specifications is None or price is None:
            return None

        return "INSERT INTO material (name, number, record_time, specifications, price)\
                    VALUES('{}', {}, {}, '{}', {})".format(name, number, record_time, specifications, price)

    @staticmethod
    def get_detail(id):
        return "SELECT id, name, number, record_time, specifications, price from material where id = {}".format(id)

    @staticmethod
    def list():
        return "SELECT id, name, number, record_time, specifications, price from material"