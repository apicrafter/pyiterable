import sys

from iterable.convert.core import convert


def run():
        convert(fromfile=sys.argv[1], tofile=sys.argv[2], silent=False, use_totals=True)
        

if __name__ == "__main__":
        run()