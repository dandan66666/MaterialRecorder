#coding: utf-8
from flask import jsonify
from functools import reduce
import types
from .errorCode import ErrorCode

def get_valid_integer(arg):
    if arg is None or type(arg) == int:
        return arg
    return int(arg)


def get_valid_float(arg):
    if arg is None or type(arg) == float:
        return arg
    return float(arg)

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
            ErrorCode.RecordNotExist : '暂无数据',
            ErrorCode.Success: '成功',
            ErrorCode.ChangeNameForbidden: '材料名称不可修改',
            ErrorCode.ServerInternalError: '服务器错误',
            ErrorCode.MultiRecords: '存在多条记录',
            ErrorCode.WrongInput: '错误输入',
            ErrorCode.SearchTypeNotExist: '搜索的类型不存在'
        }
        return errorMsgDict.get(code, 'Wrong Error Code')

    error_code, error_msg = code.value, code.name
    # 无需返回数据仅返回错误码
    if data is None:
        return jsonify({'error_code': error_code, 'error_msg': error_msg})

    records = [data] if type(data) == dict else data
    total_price = 0
    for record in records:
        total_price += record['price']*record['number']
    # if len(records) >= 2:
    #     total_price = reduce(lambda r1, r2: r1.price+r2.price, records)
    total_records = len(records)
    result =  jsonify({'error_code': error_code, 'error_msg': error_msg,
                    'total_price': total_price, 'total_records': total_records, 'records': records})
    return result

class RecordSql:
    @staticmethod
    def list_by_time_range(json_data):
        start_time = get_valid_integer(json_data.get('start_time'))
        end_time = get_valid_integer(json_data.get('end_time'))
        if start_time is None or end_time is None:
            return None
        return "SELECT id, name, number, record_time, specifications, price FROM"+\
                           " material WHERE record_time >= {} AND record_time <= {}".format(start_time, end_time)

    @staticmethod
    def list_by_name(json_data):
        name = json_data.get('name')
        if name is None:
            return None
        return "SELECT id, name, number, record_time, specifications, price FROM"+\
                       " material WHERE name = '{}'".format(name)

    @staticmethod
    def list_by_specifications(json_data):
        if json_data.get('specifications') is None:
            return None
        specifications_regex = "%{}%".format(json_data['specifications'])
        return "SELECT id, name, number, record_time, specifications, price FROM"+\
                           " material WHERE specifications LIKE '{}'".format(specifications_regex)

    @staticmethod
    def modify(json_data):
        id = get_valid_integer(json_data['id'])
        name = json_data.get('name', None)
        number = get_valid_integer(json_data.get('number', None))
        record_time = get_valid_integer(json_data.get('record_time', None))
        specifications = json_data.get('specifications', None)
        price = get_valid_float(json_data.get('price', None))
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
        name = json_data.get('name', None)
        number = get_valid_integer(json_data.get('number', None))
        record_time = get_valid_integer(json_data.get('record_time', None))
        specifications = json_data.get('specifications', None)
        price = get_valid_float(json_data.get('price', None))
        print('Add Record:', name, number, record_time, specifications, price)
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

    @staticmethod
    def list(json_data):
        sql = "SELECT id, name, number, record_time, specifications, price from material"
        name = json_data.get('name', None)
        number = get_valid_integer(json_data.get('number', None))
        start_time = get_valid_integer(json_data.get('start_time', None))
        end_time = get_valid_integer(json_data.get('end_time', None))
        specifications = json_data.get('specifications', None)
        price = get_valid_float(json_data.get('price', None))
        sqllist = []
        if name is not None:
            sqllist.append(" name='{}'".format(name))
        if number is not None:
            sqllist.append(" number={}".format(number))
        if price is not None:
            sqllist.append(" price={}".format(price))
        if specifications is not None:
            sqllist.append(" specifications LIKE '%{}%'".format(specifications))
        if start_time is not None:
            sqllist.append(" record_time >={}".format(start_time))
        if end_time is not None:
            sqllist.append(" record_time <={}".format(end_time))
        if len(sqllist) == 0:
            return sql
        sql += " WHERE" + sqllist[0]
        for i in range(1, len(sqllist)):
            sql += " AND" + sqllist[i]
        return sql

