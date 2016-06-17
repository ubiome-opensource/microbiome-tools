import sys
from argparse import ArgumentParser

from .ubiome import ubiomeApp


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    parser = ArgumentParser()
    parser.add_argument("-c", "--compare", help="Compare sample1 with sample2")
    parser.add_argument("-u", "--unique", help="Find items in sample1 not in sample2")
    parser.add_argument("-d", "--debug", help="turn on debug mode to run tests")
    parser.add_argument("sample2", help="sample you are comparing to")
    args = parser.parse_args()

    if not (args):
        print("type ubiomecompare -h for help")
        quit()
    if args.compare:
        # print("Compare Sample 1 Args=",args.compare,args.sample2)
        a = args.compare
        b = args.sample2
    if args.unique:
        # print("Unique Sample 1",args.unique,args.sample2)
        a = args.unique
        b = args.sample2
    if args.debug:
        a = "./testdata/Sprague-ubiomeMay2014.json"
        b = "./testdata/Sprague-uBiomeJun2014.json"

    myApp = ubiomeApp(a, b)
    if args.unique:
        myApp.runUnique()
    if args.compare:
        myApp.runCompare()

if __name__ == "__main__":
    main()