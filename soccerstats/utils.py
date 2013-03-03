"""
Utils for the service.

:author: 2012, Pascal Hartig <phartig@weluse.de>
:license: BSD
"""

import re
from flask import make_response, jsonify, current_app


class JSONError(object):

    def __init__(self, type=None, code=None, message=None):
        self.type = type or "INTERNAL_ERROR"
        self.code = code or "UNKNOWN"
        self.message = message

    @classmethod
    def from_exception(cls, exception, **kwargs):
        okwargs = {
            'code': camel_to_upper(exception.__class__.__name__),
            'message': exception.message
        }

        okwargs.update(kwargs)
        return cls(**okwargs)

    def to_json(self):
        result = {
            "type": self.type,
            "code": self.code,
        }

        if self.message is not None:
            result['message'] = self.message

        return result

    def to_error(self, error_code=400):
        data = jsonify(error=self.to_json())
        return make_response(data, error_code)


def camel_to_upper(value):
    """
    >>> camel_to_upper("HelloWorld")
    "HELLO_WORLD"
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).upper()
