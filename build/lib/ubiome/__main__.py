import sys
from argparse import ArgumentParser

from .ubiome import UbiomeSample
from .ubiomeMultiSample import UbiomeMultiSample


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    if not len(sys.argv) > 1:
        print("A processor for uBiome taxonomy files. Type ubiome -h for help")
        quit()
    parser = ArgumentParser(description="A processor for uBiome taxonomy files")
    parser.add_argument("-c", "--compare", help="Compare sample1 with sample2", nargs=2, metavar=('sample1.json','sample2.json'))
    parser.add_argument("-u", "--unique", help="Find items in sample1 not in sample2", nargs=2, metavar=('sample1.json','sample2.json'))
    #parser.add_argument("sample2", help="sample you are comparing to")
    parser.add_argument("-m", "--multi",help="Combine multiple samples",type=str, nargs="+", metavar=('sample1.json','sample2.json'))
    args = parser.parse_args()

    if args.compare:
        # print("Compare Sample 1 Args=",args.compare,args.sample2)
        s1 = UbiomeSample(args.compare[0])
        s2 = UbiomeSample(args.compare[1])
        s  = s1.compareWith(s2)
        s.write(sys.stdout)

    if args.unique:
        # print("Unique Sample 1",args.unique,args.sample2)
        s1 = UbiomeSample(args.unique[0])
        s2 = UbiomeSample(args.unique[1])
        s = s1.unique(s2)
        s.write(sys.stdout)

    if args.multi:
        m = UbiomeMultiSample(UbiomeSample(args.multi[0]))
        for sample in args.multi[1:]:
            m.merge(UbiomeSample(sample))
        m.write(filename=sys.stdout)

if __name__ == "__main__":
    main()