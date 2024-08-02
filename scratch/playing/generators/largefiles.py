# largefiles.py
#
# Find all transfers over a megabyte

from apachelog import apache_log
from linesdir import lines_from_dir

lines = lines_from_dir("access-log*","www")
log = apache_log(lines)

large = (r for r in log
         if r["bytes"] > 1000000)

for r in large:
    print(r["request"],r["bytes"])


