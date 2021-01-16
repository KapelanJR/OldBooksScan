import warnings

warnings.filterwarnings("ignore")

import sys
import Match
import Cutter

def main(bookName):
    Cutter.main(bookName)
    Match.Main(bookName)

if __name__ == "__main__":
    main(sys.argv[1])