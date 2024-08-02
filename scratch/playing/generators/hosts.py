# hosts.py
#
# Find unique host IP addresses

from apachelog import apache_log
from linesdir import lines_from_dir

lines = lines_from_dir("access-log*","www")
log = apache_log(lines)

hosts = set(r["host"] for r in log)
for h in hosts:
    print(h)
