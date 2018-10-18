#!/bin/sh
source venv/bin/activate

exec gunicorn -b :5001 -w $(( 2 * `cat /proc/cpuinfo | grep 'core id' | wc -l` + 1 )) --access-logfile - --error-logfile - seed:application