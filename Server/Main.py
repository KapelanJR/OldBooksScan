import warnings

warnings.filterwarnings("ignore")

import sys
import Match
import Cutter

def main(bookName):
    Cutter.main(bookName)
    Match.Main("test1")

if __name__ == "__main__":
    main("test1")