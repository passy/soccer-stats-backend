#!/usr/bin/env python
"""
Management script for the soccerstats Flask project.

:author: 2013, Pascal Hartig <phartig@weluse.de>
:license: BSD
"""

import sys
import os
from flask.ext.script import Manager, Server


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))


from soccerstats.application import create_app


manager = Manager(create_app({'DEBUG': True}))
manager.add_command("runserver", Server(host="0.0.0.0", port=5000,
                                        threaded=True, use_debugger=True))


@manager.command
def test():
    os.system("python -m pytest")


if __name__ == "__main__":
    manager.run()
