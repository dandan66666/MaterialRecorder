
from flask import jsonify

def get_json_from_cursor(cursor):
    result = []
    for row in cursor:
        d = {"id": row[0], "name": row[1], "number": row[2], "record_time": row[3],
             "specifications": row[4], "price": row[5]}
        result.append(d)
    return jsonify(result)