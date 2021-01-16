import Cutter
import Match
import sys
import warnings

warnings.filterwarnings("ignore")


def main(bookName):
    Cutter.main(bookName)
    Match.Main(bookName)


if __name__ == "__main__":
    main(sys.argv[1])
