#!/usr/bin/python
# ### ubiomeFastqCombine.py
# use this command to combine the individual sequences for each run into a single file:

#	% python ubiomeFastqCombine.py -c ssr_15759__R1__L004.fastq ssr_15759__R2__L004.fastq
#	% gzip ssr_15759ssr_15759.fastq 

#This script simply tapes together the sequences and associated error information  across the two runs.
#Then gzip the resulting file so it's faster to upload. Compressing it will save 10x on bandwidth.


__author__ = 'sprague'


import __future__
from argparse import ArgumentParser

def ubiomeCombineRuns(fname1,fname2):
    """
    return a single file with appended version of the seq found in each run
    :param fname1: string filename for run 1 of a given lane
    :param fname2: string filename for run 2 of the same lane.
    :return: list of all sequences found.  You can check the length of the list as a check on whether it worked or not.
    """
    f1=open(fname1,'r')
    f2=open(fname2,'r')
    output = open(fname1[:9]+fname2[:9]+".fastq",'w')
    seqs = []
    quals = []
    while True:
        header1 = f1.readline()
        header2 = f2.readline()
        seq1 = f1.readline().strip()
        seq2 = f2.readline().strip()
        if len(seq1)==0:
            break
        plus1 = f1.readline()  # skip
        plus2 = f2.readline()  # skip
        qual1 = f1.readline().strip()
        qual2 = f2.readline().strip()
        output.write(header1)
        output.write(seq1+seq2+"\n")
        output.write(plus1)
        output.write(qual1+qual2+"\n")
        seqs+=[seq1+seq2]
    f1.close()
    f2.close()
    output.close()
    return seqs


if __name__=="__main__":
    parser = ArgumentParser()
    parser.add_argument("-c","--combine",help="Combine seq1 with seq1")
    #parser.add_argument("-u","--unique",help="Find items in sample1 not in sample2")
    #parser.add_argument("-d","--debug",help="turn on debug mode to run tests")
    parser.add_argument("seq2",help="another sequence")
    args = parser.parse_args()

    if not(args):
        print("type ubiomecompare -h for help")
        quit()
    if args.combine:
        a=args.combine
        b=args.seq2
#    if args.unique:
        #print("Unique Sample 1",args.unique,args.sample2)
#       a=args.unique
    z = ubiomeCombineRuns(a,b)
    print("Length=%d",len(z))
