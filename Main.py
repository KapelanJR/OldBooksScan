import warnings

warnings.simplefilter(action = "ignore", category = FutureWarning)

import sys
import Match
import Cutter

def main(bookPath, bookName):
    Cutter.main(bookPath, bookName)
    Match.Main(bookPath)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])