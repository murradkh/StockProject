#!/bin/sh

exitcode=0

cd $(dirname "$0")
for testfile in myapp/tests/test_*.py; do
	# Running tests separately beacuse web tests can't run together...
	echo "Running test $testfile"
	python3 -m unittest $testfile
	exitcode=$(expr  $? \| "$exitcode")
done

exit $exitcode
