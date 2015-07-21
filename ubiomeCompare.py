#! /usr/bin/env python
# ### uBiomeCompare.py
### lets you analyze your uBiome sample
###
### works from the command line:
### %python uBiomeCompare
"""

this text is ignored

>>> myApp.testUnique()
44
>>> v = myApp.testCompare(myApp.esample,myApp.msample)
>>> len(v.sampleList)
195

>>> 5+5
10



"""
__author__ = 'sprague'

import json
import csv
import sys
from argparse import ArgumentParser



class Taxon():
    """
    a list of the characteristis of a single uBiome taxon.
    """





class UbiomeSample():
    """ class representation of a well-formed uBiome sample

    """

    def __init__(self,fname):
        """ initialize with a string representing the path to a uBiome-formatted JSON file
        """
        jsonFile = open(fname)
        sourceJson = json.load(jsonFile)
        self.sampleList = sourceJson["ubiome_bacteriacounts"] # a list of dicts
        self.taxRankList = []

    def showContents(self):
        print("length=",len(self.sampleList))
        print("taxlist\n",self.taxranklist())

    def taxranklist(self, rank="species"):
        """ returns a list of all organisms in this sample that are species.
        """
        if self.taxRankList: # already computed, so don't recompute
            return self.taxRankList
        for taxon in self.sampleList:
            if taxon["tax_rank"]==rank:
                self.taxRankList = self.taxRankList + [taxon["tax_name"]]
        return self.taxRankList


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


    # def addCountsToList(self,organismList):
    #     """
    #
    #     :rtype : list
    #     :param organismList: a  list of organism tax_names
    #     :param sample: a well-formed uBiome JSON-formatted sample
    #     :return: a list of dictionaries that includes the tax_name for the sample, plus its count_norm
    #     """
    #     if organismList == []:
    #         return []
    #     else:
    #         return [{"tax_name":organismList[0],"count_norm":self.countNormOf(organismList[0])}] +  self.addCountsToList(organismList[1:])

    def unique(self,sample2):
        """
        returns all organisms that are unique to sample 1
        :type sample2: UbiomeSample
        :param sample2:
        :return: UBiomeDiffSample
        """
        uniqueSet = set(self.taxranklist()) - set(sample2.taxranklist())  # all unique taxons
        listWithCounts = self.addCountsToList(list(uniqueSet))
        returnSample=UbiomeDiffSample(listWithCounts)
        return returnSample

    def addCountsToList(self,taxonList):
        """
        :param taxonList: list # contains taxnames
        :return:
        """
        if taxonList == []:
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
                taxList = taxList + [{"tax_name":taxon1["tax_name"],"count_norm":str(countDiff),"tax_rank":taxon1["tax_rank"]}]



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
        self.taxRankList = []



# def ubiomeAddCountsToList(organismList,sample):
#     """
#
#     :rtype : list
#     :param organismList: a  list of organism tax_names
#     :param sample: a well-formed uBiome JSON-formatted sample
#     :return: a list of dictionaries that includes the tax_name for the sample, plus its count_norm
#     """
#     if organismList == []:
#         return []
#     else:
#         return [{"tax_name":organismList[0],"count_norm":ubiomeCountNormOf(organismList[0],sample)}] +  ubiomeAddCountsToList(organismList[1:],sample)
#


## Python sets:
## a - b
## a | b
## a & b
## a ^ b  # in a or b but not both

class ubiomeApp():
    def __init__(self,fname1,fname2):
        self.msample = UbiomeSample(fname1)
        self.esample = UbiomeSample(fname2)



    def testUnique(self):
        unique=self.esample.unique(self.msample)
        print(len(unique.sampleList))
        #print("len esample.unique",len(unique.sampleList))
        unique.writeCSV("esample.csv")

    def runUnique(self):
        unique=self.esample.unique(self.msample)
        #print("len esample.unique",len(unique.sampleList))
        unique.writeCSV(sys.stdout)

    def testCompare(self,sample1,sample2):
        compare=sample1.compareWith(sample2)
        compare.writeCSV("ecompare.csv")
        return compare

    def runCompare(self,sample1,sample2):
        compare=sample1.compareWith(sample2)
        compare.writeCSV(sys.stdout)
        return compare



if __name__=="__main__":
    #print("run uBiomeCompare.py")
    import doctest


    parser = ArgumentParser()
    parser.add_argument("-c","--compare",help="Compare sample1 with with sample2")
    parser.add_argument("-u","--unique",help="Find items in sample1 not in sample2")
    parser.add_argument("-d","--debug",help="turn debug mode to run tests")
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
   # b = "../Data/others/elijah.json"
    myApp = ubiomeApp(a,b)
    if args.unique:
        myApp.runUnique()
    if args.compare:
        myApp.runCompare(myApp.esample,myApp.msample)

    DEBUG = False

    if DEBUG:
        #myApp.testUnique()
        #v = myApp.testCompare(myApp.esample,myApp.msample)
        doctest.testmod()
        print("all tests successful")
else:
    print("uBiomeCompare loaded as a module")

