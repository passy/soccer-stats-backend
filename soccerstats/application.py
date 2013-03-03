"""
Soccer Stats API Flask application.

:author: 2013, Pascal Hartig <phartig@weluse.de>
:license: BSD
"""

from __future__ import absolute_import

import flask
from flask import Flask, jsonify


class JSONFlask(Flask):
    """Creates a JSON repsonse if the returned object contains a ``to_json``
    method.
    """

    def make_response(self, rv):
        if hasattr(rv, 'to_json'):
            return jsonify(rv.to_json())

        if isinstance(rv, tuple):
            if len(rv) == 2 and hasattr(rv[0], 'to_json'):
                return Flask.make_response(self, (jsonify(rv[0].to_json()),
                                                  rv[1]))

        return Flask.make_response(self, rv)


def create_app(config=None):
    from .api import api
    from . import settings

    app = JSONFlask('soccerstats')
    app.config.from_object(settings)

    if config is not None:
        app.config.update(config)

    @app.before_request
    def intercept_cors_preflight():
        if not app.config['CORS_ENABLED']:
            return

        if flask.request.method == 'OPTIONS' and \
           'Origin' in flask.request.headers:
            return flask.make_response()

    @app.after_request
    def cors_response(response):
        if not app.config['CORS_ENABLED'] or \
           'Origin' not in flask.request.headers:
            return response

        headers = {
            'Access-Control-Allow-Origin': app.config['CORS_ORIGIN'],
            # We only need GET at the moment.
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': ('origin, x-requested-with, '
                                             ' content-type, accept')
        }

        for key, value in headers.items():
            response.headers.add_header(key, value)

        return response

    app.register_blueprint(api)
    return app
