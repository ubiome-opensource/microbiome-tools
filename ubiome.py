#!/usr/bin/env python
# ### uBiomeCompare.py
### lets you analyze your uBiome sample
###
### works from the command line in either Python 2.7+ or Python 3+
### %python ubiome

__author__ = 'sprague'

import json
import csv
import sys
import __future__
from argparse import ArgumentParser



class Taxon():
    """
    An abstract representation of a uBiome taxon
    """





class UbiomeSample():
    """ class representation of a well-formed uBiome sample

    """

    def __init__(self,fname=[],name=[]):
        """ initialize with a string representing the path to a uBiome-formatted JSON file
        """
        if fname:
            self.readJSONfile(fname)
        else:
            self.sampleList = []
        self.taxnamelist = []
        if not name:
            self.name = fname
        else:
            self.name = name

    def readJSONfile(self,fname):
        jsonFile = open(fname)
        sourceJson = json.load(jsonFile)
        self.sampleList = sourceJson["ubiome_bacteriacounts"] # a list of dicts

    def readCSVfile(self,fname):
        csvFile = open(fname)
        sourceCSV = csv.DictReader(csvFile)
        header = sourceCSV.fieldnames
        for row in sourceCSV:
            self.sampleList+=[row]


    def prettyPrint(self):
        try:
            __import__("prettytable")
        except ImportError:
            #print("no prettyprint available")
            return
        else:
            import prettytable
            uniqueTable = prettytable.PrettyTable(["Tax_Name","Tax_Rank","Count_Norm"])
            for i in self.sampleList:
                uniqueTable.add_row([i["tax_name"],i["tax_rank"],i["count_norm"]])
            #print(uniqueTable)
            return uniqueTable


    def sort(self,sortBy="tax_name"):
        self.sampleList = sorted(self.sampleList,key=lambda k:k[sortBy],reverse=True)
        return True





    def showContents(self):
        l = len(self.sampleList)
        print("length=",l)
        i=0
        while l>10&i<10:
            print(self.sampleList[i])
            l=l-1
            i+=1



    def taxnames(self):
        """ returns a list of all organisms in this sample
        :return: list
        """
        if self.taxnamelist: # already computed, so don't recompute
            return self.taxnamelist
        for taxon in self.sampleList:
            self.taxnamelist = self.taxnamelist + [[taxon["tax_name"],taxon["tax_rank"]]]
        return self.taxnamelist


    def countNormOf(self, taxName):
        """
        returns the count_norm of a given taxName for a sample
        :param taxName: string representation of a uBiome tax_name
        :return:
        """
        for taxon in self.sampleList:
            if taxon["tax_name"]==taxName:
                assert isinstance(taxon, dict)
                return int(taxon["count_norm"])

    def taxonOf(self, taxName):
            """
            returns an entire taxon dict of a given taxName for a sample
            :param taxName: string representation of a uBiome tax_name
            :return: dict
            """
            for taxon in self.sampleList:
                if taxon["tax_name"]==taxName:
                    assert isinstance(taxon, dict)
                    return taxon
            return None


    def unique(self,sample2):
        """
        returns all organisms that are unique to sample 1
        :type sample2: UbiomeSample
        :param sample2:
        :return: UBiomeDiffSample
        """
        uniqueList = []
        for taxon1 in self.sampleList:
            t=sample2.taxonOf(taxon1["tax_name"])
            if not t: # not found sample2, so add to the return list
                uniqueList = [{"tax_name":taxon1["tax_name"],"count_norm":taxon1["count_norm"],"tax_rank":taxon1["tax_rank"]}] + uniqueList
        return UbiomeDiffSample(uniqueList)
        #
        #
        # uniqueSet = set(self.taxranklist()) - set(sample2.taxranklist())  # all unique taxons
        # listWithCounts = self.addCountsToList(list(uniqueSet))
        # returnSample=UbiomeDiffSample(listWithCounts)
        # return returnSample

    def addCountsToList(self,taxonList):
        """
        :param taxonList: list # contains taxnames
        :return:
        """
        if not taxonList:
            return []
        else:
            return [{"tax_name":taxonList[0],"count_norm":self.countNormOf(taxonList[0])}] +\
                   self.addCountsToList(taxonList[1:])



    def compareWith(self,sample2):
        """

        :param sample2: UbiomeSample
        :return: UBiomeDiffSample
        """

        taxList = []
        for taxon1 in self.sampleList:
            t = t=sample2.taxonOf(taxon1["tax_name"])
            if t: #found this taxon in sample2
                countDiff = int(taxon1["count_norm"]) - int(t["count_norm"])
                taxList = [{"tax_name":taxon1["tax_name"],"count_norm":str(countDiff),"tax_rank":taxon1["tax_rank"]}] + taxList



     #   allOrganisms = set(self.taxranklist()) & set(sample2.taxranklist())
     #   allOrganismsWithCounts = self.addCountsToList(list(allOrganisms))
        diffSample = UbiomeDiffSample(taxList)
        return diffSample

    def writeCSV(self,filename):
        if filename==sys.stdout:
            ubiomeWriter = csv.DictWriter(sys.stdout,dialect='excel',fieldnames=self.sampleList[0].keys())
            #print('writing to csv')
            ubiomeWriter.writeheader()
            for organism in self.sampleList:
                ubiomeWriter.writerow(organism)
        else:
            with open(filename,'w') as csvFile:
                #print('writing to csv')
                ubiomeWriter = csv.DictWriter(csvFile,dialect='excel',fieldnames=self.sampleList[0].keys())
                ubiomeWriter.writeheader()
                for organism in self.sampleList:
                    ubiomeWriter.writerow(organism)


class UbiomeDiffSample(UbiomeSample):
    """ same as regular uBiome sampleList, except count_norm is a delta, not an absolute number.

    """
    def __init__(self,sampleList):
        self.sampleList = sampleList
        self.taxnameList = []

class UbiomeMultiSample():
    """
    merge a bunch of samples into a single data frame
    [ fullTaxList, sample1Quantities, sample2Quantities, ... ]

    fullTaxList is a list containing strings of tax_name; fullTaxList[0] = "tax_name"
    sampleQuantities is a list where sampleQuantities[0] = "July"  and [1..n] correspond to Quants for fullTaxList[1..n]

    usage: (assuming sample1 and sample2 are of class UbiomeSample)

    x = UbiomeMultiSample()  # initializing
    x.merge(sample1) #


    """
    def __init__(self,newSample = []):
        self.fullTaxList = [["tax_name","tax_rank"]]
        self.samples = []
        if newSample:
            self.fullTaxList +=newSample.taxnames()
            self.samples+=[[newSample.name]+[sample["count_norm"] for sample in newSample.sampleList]]


    def showContents(self):
        print("length of fullTaxList=",len(self.fullTaxList))
        print([self.fullTaxList[i] for i in range(10)])
        print("length of samples=",len(self.samples))
        for sample in self.samples:
            print(sample[0],"--->",len(sample))
        print("latest sample:",[self.samples[len(self.samples)-1][i] for i in range(10)])


    def merge(self,sample2):
        """ merge the current multiSample with sample2.  This operation is mutable
        so you permanently modify the current UbiomeMultiSample when you do this.

        :param sample2: UbiomeSample
        :return:
        """

        # find the taxNames missing from fullTaxList
        newTaxNamesL = []
        sampleTaxNames = sample2.taxnames()

        Sample2ZippedList = sample2.taxnames()
        justSample2TaxNames, justSample2TaxRanks = zip(*Sample2ZippedList)
        justFullTaxNames, justFullTaxRanks = zip(*self.fullTaxList)

        newTaxRanksL = []
        for i,taxName in enumerate(sampleTaxNames):
            if taxName not in self.fullTaxList:
                newTaxNamesL+=[taxName]
                newTaxRanksL+=[justFullTaxRanks[i]]

        self.fullTaxList+=newTaxNamesL
        newTaxons = [sample2.taxonOf(taxa[0])for taxa in newTaxNamesL]

        #[sample["count_norm"] for sample in sample2.sampleList]
        oldSamplesList = self.samples[len(self.samples)-1]
        #newCounts =  oldSamplesList[0][1:] + [taxon["count_norm"] for taxon in newTaxons]
        # problem: newCounts contains the sample counts from the previous sample, not the current one.
        # need to generate a list of counts that correspond to the organisms in fullTaxList
        # if I have the UbiomeSample object for the previous sample, this is easy to compute:
        # [oldSample.taxonOf(self.fullTaxList[i]) for taxon in oldSample]
        newSampleCountsForPreviousTaxa = []
        for i in range(len(oldSamplesList)-1):
            taxonForTaxName = sample2.taxonOf(self.fullTaxList[i+1][0])
            if taxonForTaxName:
                taxCount = taxonForTaxName["count_norm"]
            else: taxCount = 0
            newSampleCountsForPreviousTaxa+=[taxCount]
        newCounts =  newSampleCountsForPreviousTaxa + [taxon["count_norm"] for taxon in newTaxons]




        self.samples += [[sample2.name] + newCounts]

        # new length of a sample is len(newTaxons)+ len(oldSamplesList)
        # fill previous samples with count_norm = 0
        for i, sample in enumerate(self.samples):
            if len(self.samples[i])<(len(newCounts)+1):
                self.samples[i]=self.samples[i] + [0 for k in range(len(newTaxons))]



    def writeCSV(self,filename):
        if filename==sys.stdout:
            ubiomeWriter = csv.DictWriter(sys.stdout,dialect='excel',fieldnames=["tax_name"]+ ["tax_rank"] + [sample[0] for sample in self.samples])
            #print('writing to csv')
            ubiomeWriter.writeheader()
            for i,taxa in enumerate(self.fullTaxList):
                taxName, taxRank = taxa
                rowDict = ["tax_name",taxName]
                rankDict = ["tax_rank",taxRank]
                sampleDict = [[sample[0],sample[i]] for sample in self.samples]
                ubiomeWriter.writerow(dict([rowDict]+[rankDict] +sampleDict))
        else:
            with open(filename,'w') as csvFile:
                #print('writing to csv')
                ubiomeWriter = csv.DictWriter(csvFile,dialect='excel',fieldnames=["tax_name"]+ ["tax_rank"] + [sample[0] for sample in self.samples])
                #print('writing to csv')
                ubiomeWriter.writeheader()
                for i,taxa in enumerate(self.fullTaxList):
                    taxName, taxRank = taxa
                    rowDict = ["tax_name",taxName]
                    rankDict = ["tax_rank",taxRank]
                    sampleDict = [[sample[0],sample[i]] for sample in self.samples]
                    ubiomeWriter.writerow(dict([rowDict]+[rankDict] +sampleDict))


## Python sets:
## a - b
## a | b
## a & b
## a ^ b  # in a or b but not both

class ubiomeApp():
    def __init__(self,fname1,fname2):
        self.sample1 = UbiomeSample(fname1)
        self.sample2 = UbiomeSample(fname2)



    def testUnique(self):
        unique=self.sample1.unique(self.sample2)
        print(len(unique.sampleList))
        #print("len esample.unique",len(unique.sampleList))
        unique.writeCSV("sample1Unique.csv")

    def runUnique(self):
        unique=self.sample1.unique(self.sample2)
        #print("len esample.unique",len(unique.sampleList))
        unique.writeCSV(sys.stdout)

    def testCompare(self):
        compare=self.sample1.compareWith(self.sample2)
        compare.writeCSV("sample1Compare.csv")
        return compare

    def runCompare(self):
        compare=self.sample1.compareWith(self.sample2)
        compare.writeCSV(sys.stdout)
        compare.prettyPrint()
        return compare



if __name__=="__main__":
    #print("run uBiomeCompare.py")
    #import doctest


    parser = ArgumentParser()
    parser.add_argument("-c","--compare",help="Compare sample1 with with sample2")
    parser.add_argument("-u","--unique",help="Find items in sample1 not in sample2")
    #parser.add_argument("-d","--debug",help="turn on debug mode to run tests")
    parser.add_argument("sample2",help="sample you are comparing to")
    args = parser.parse_args()

    if not(args):
        print("type ubiomecompare -h for help")
        quit()
    if args.compare:
        #print("Compare Sample 1 Args=",args.compare,args.sample2)
        a=args.compare
        b=args.sample2
    if args.unique:
        #print("Unique Sample 1",args.unique,args.sample2)
        a=args.unique
        b=args.sample2

   # a = "../Data/sprague data/Sprague-ubiomeMay2014.json"
   # b = "../Data/sprague data/Sprague-uBiomeJun2014.json"
    myApp = ubiomeApp(a,b)
    if args.unique:
        myApp.runUnique()
    if args.compare:
        myApp.runCompare()


else:
    print("uBiomeCompare loaded as a module")

