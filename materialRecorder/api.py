#coding: utf-8
from flask import request, jsonify, g, Blueprint, current_app, abort
from .utils import getErrorMsg, make_record_response
from .errorCode import ErrorCode
from . import db

mod = Blueprint('utils', __name__, url_prefix='/')

@mod.before_app_request
def get_db():
    db.get_db()

@mod.after_app_request
def close_db(res):
    db.close_db()
    return res

@mod.route('/construction/list')
def get_construction():
    sqlStr = "SELECT construction, COUNT(construction) from material GROUP BY construction"
    result = []
    cursor = g.db.cursor()
    try:
        cursor.execute(sqlStr)
        for row in cursor:
            result.append(row[0])
        current_app.logger.info("Get Construction Success")
        error_code, error_msg = ErrorCode.Success.value, getErrorMsg(ErrorCode.Success)
        return jsonify({'error_code': error_code, 'error_msg': error_msg,
                'constructions': result})
    except Exception as e:
        current_app.logger.error("Get Construction Error %s", e)
        return make_record_response(None, ErrorCode.GetConstructionError)
    finally:
        cursor.close()
