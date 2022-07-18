"""
 base response
 Created by janeho at 11/04/2022.
"""
from flask import jsonify


class BaseResponse:
    """
    base response
    """
    def __init__(self):
        """
        init response code
        """
        self.result_code_success = 200
        self.result_code_fail = 201

    def success(self, msg="success", data=None):
        """
        success response
        :param msg: message
        :param data: data
        :return: json
        """
        if data is None:
            data = {}
        result = {
            "code": self.result_code_success,
            "message": msg,
            "data": data
        }
        return jsonify(result)

    def fail(self, msg="fail", data=None):
        """
        fail response
        :param msg: message
        :param data: data
        :return: json
        """
        if data is None:
            data = {}
        result = {
            "code": self.result_code_fail,
            "message": msg,
            "data": data
        }
        return jsonify(result)
