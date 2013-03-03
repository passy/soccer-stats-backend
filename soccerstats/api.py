"""
Blueprint implementing the API wrapper.

:author: 2013, Pascal Hartig <phartig@weluse.de>
:license: BSD
"""

from flask import Blueprint, request
from .utils import JSONError


api = Blueprint('api', __name__, url_prefix='/v1')
