#!/bin/sh

exitcode=0

cd $(dirname "$0")
find myapp -not -path '*tests*' -name '*.py' -not -name wsgi.py -not -name asgi.py -not -name settings.py -not -name manage.py -not -name admin.py | xargs python3 -m flake8 --ignore F405,F401,E501,F403
exitcode=$(expr  $? \| "$exitcode")


exit $exitcode
