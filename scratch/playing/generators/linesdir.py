# linesdir.py
#
# Generate a sequence of lines from files in a directory

from pathlib import Path

from gencat import gen_cat
from genopen import gen_open


def lines_from_dir(filepat, dirname):
    names = Path(dirname).rglob(filepat)
    files = gen_open(names)
    return gen_cat(files)

# Example use

if __name__ == "__main__":
    loglines = lines_from_dir("access-log*","www")
    for line in loglines:
        print(line, end="")
