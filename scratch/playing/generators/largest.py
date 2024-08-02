# largest.py
#
# Find the largest file

from apachelog import apache_log
from linesdir import lines_from_dir

lines = lines_from_dir("access-log*","www")
log = apache_log(lines)

print("%d %s" % max((r["bytes"],r["request"])
                    for r in log))
