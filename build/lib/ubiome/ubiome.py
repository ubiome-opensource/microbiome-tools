#!/usr/bin/env python
# ### ubiome.py
### lets you analyze your uBiome sample
###
### works from the command line in either Python 2.7+ or Python 3+
### %python ubiome.py

from __future__ import print_function, division

__author__ = 'sprague'

import json
import csv
import sys
import datetime


INVALID_TAXON = -1
INVALID_COLOR = -2
INVALID_RANK = -3
INVALID_AVG = -4
INVALID_COUNT = -5


class UbiomeTaxa():
    '''Abstracts the keys from the uBiome JSON file, making it easier to update if the format changes.
    Normally a SampleList looks like this:
    [dict1, dict2, dict3, dict4, ... dictN]

    where dict is something like this:
    {'parent': '2', 'count': '157391', 'count_norm': 622877, 'taxon': '1239',
        'tax_name': 'Firmicutes', 'tax_rank': 'phylum', 'tax_color': '5E6591', 'avg': None}

    a UbiomeTaxonomy object lets you do this:
    >>>a = UbiomeTaxa({'parent': '2', 'count': '157391', 'count_norm': 622877, 'taxon': '1239',\
        'tax_name': 'Firmicutes', 'tax_rank': 'phylum', 'tax_color': '5E6591', 'avg': None})

    >>>a.parent
    '2'
    >>>a.count_norm
    157391

    # but you're not allowed to set a new value for these attributes
    '''

    def __init__(self, ubiomeDict):
        assert (isinstance(ubiomeDict, dict))
        self._parent = ubiomeDict.get('parent', INVALID_TAXON)
        try:
            self._count = int(ubiomeDict.get('count'))
        except TypeError:
            self._count = INVALID_COUNT

        try:
            self._count_norm = int(ubiomeDict.get('count_norm'))
        except TypeError:
            self._count_norm = INVALID_COUNT
        self._taxon = ubiomeDict.get('taxon', INVALID_TAXON)
        self._tax_name = ubiomeDict.get('tax_name', "unknown tax_name")
        self._tax_rank = ubiomeDict.get('tax_rank', INVALID_RANK)
        self._avg = ubiomeDict.get('avg', INVALID_AVG)
        self._tax_color = ubiomeDict.get('tax_color', INVALID_COLOR)

    def __str__(self):
        return "<ubiome.UbiomeTaxa: " + self.tax_name + ">"

    @classmethod
    def nullTaxa(self):
        return UbiomeTaxa({"tax_name": "None", "taxon": INVALID_TAXON, "parent": INVALID_TAXON, \
                "count": 0, "percent":0, "count_norm": 0, "tax_rank": INVALID_RANK, "avg": INVALID_AVG,
                "tax_color": INVALID_COLOR})

    @property
    def dictForm(self):
        ''' returns taxa as a dict, for compatibility with the original JSON
        :return:dict
        :rtype: dict
        '''
        return {"tax_name": self.tax_name, "taxon": self.taxon, "parent": self.parent, \
                "count": self.count, "count_norm": self.count_norm, "tax_rank": self.tax_rank, "avg": self.avg,
                "tax_color": self.tax_color}

    @property
    def parent(self):
        return self._parent

    @property
    def count(self):
        if type(self._count) == int:
            return self._count
        try:
            self._count = int(self._count)
        except ValueError:
            assert ("bad value for count")
        return self._count

    @property
    def percent(self):
        ''' convert count_norm to percentage of sample

        :return: float
        :rtype: float
        '''
        if self.count_norm > 0:
            return round(self.count_norm / 10000, 4)
        return 0

    @property
    def taxon(self):
        return self._taxon

    @property
    def tax_color(self):
        return self._tax_color

    @property
    def avg(self):
        return self._avg

    @property
    def count_norm(self):
        return self._count_norm

    @property
    def tax_name(self):
        return self._tax_name

    @property
    def tax_rank(self):
        return self._tax_rank


class UbiomeSample():
    """ class representation of a well-formed uBiome sample

    """

    def __init__(self, fname="", name="", date=datetime.date(2000, 1, 1), site="gut"):
        """ initialize with a string representing the path to a uBiome-formatted JSON file
        If no name, just instantiate an object; you can read the contents later using self.load()
        :param fname : filename
        :param name: name for the sample
        :type name: str
        :type fname: str
        :type date: datetime.date
        """
        self.date = date
        self.site = site
        if fname:
            self.load(fname)
        else:
            self._taxaList = []
        self._taxnamelist = []

        if not name:
            self.name = fname
        else:
            self.name = name

    @property
    def taxaList(self):
        """ list of all taxa in this sample, represented as a list made of UbiomeTaxa

        :return: list
        """
        return self._taxaList

    def set_taxaList_JSON(self, sourceJson):
        """

        :param  sourceJson: a dict representation of a well-formed uBiome dictionary
        :type sourceJson: dict
        :return:
        """
        allDicts = sourceJson["ubiome_bacteriacounts"]  # a list of dicts
        newDicts = []
        for taxa_dict in allDicts:
            taxa_dict['count_norm'] = int(taxa_dict['count_norm'])
            newDicts += [taxa_dict]
        self._taxaList = [UbiomeTaxa(taxDict) for taxDict in newDicts]

    def load(self, fname, ftype="JSON"):
        """ read a JSON file of the uBiome taxonomy (the one you get from downloading from the uBiome web site)
        :type fname: str
        :param fname: the string filename containing JSON data
        :param ftype: currently unused, but provided for future compatibility
        :type ftype: str
        :return:
        :rtype None
        """
        import os
        if ftype == "CSV":
            self.__read_CSV_file(fname)
        else:
            jsonFile = open(fname)
            sourceJson = json.load(jsonFile)
            try:
                site = sourceJson['site']
                self.site = site
            except KeyError:
                pass  # keep the default site name
            try:
                date_str = sourceJson['sampling_time']
                self.datetime = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                self.date = datetime.date(self.datetime.year, self.datetime.month, self.datetime.day)
            except ValueError:
                date_str = sourceJson['sampling_time']
                self.datetime = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                self.date = datetime.date(self.datetime.year, self.datetime.month, self.datetime.day)
            except KeyError:
                try:
                    date_str = sourceJson['dateSampled']
                    if date_str:
                        self.datetime = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                        self.date = datetime.date(self.datetime.year, self.datetime.month, self.datetime.day)
                except KeyError:
                    # self.date = datetime.date(2000,1,1)
                    self.datetime = datetime.datetime(self.date.year, self.date.month, self.date.day, 0, 0)
            try:
                self.notes = sourceJson['notes']
            except KeyError:
                self.notes = ""
            try:
                self.sequencing_revision = sourceJson['sequencing_revision']
            except KeyError:
                self.sequencing_revision = "0"
            self.sequencing_revision = int(self.sequencing_revision)

            self.set_taxaList_JSON(sourceJson)

    def __read_CSV_file(self, fname):
        """
        read a CSV-formatted version of the uBiome taxonomy data.
        :param fname: filename
        :return:
        """
        csvFile = open(fname)
        sourceCSV = csv.DictReader(csvFile)
        header = sourceCSV.fieldnames
        for row in sourceCSV:
            self._taxaList += [UbiomeTaxa(row)]


        # todo make explicit return values

    def prettyPrint(self):
        """
        print a nice ascii table of the sample if you have the PIP module 'prettytable' available.
        :return: prettytable
        """
        try:
            __import__("prettytable")
        except ImportError:
            print("no prettyprint available")
            pTable = "Tax_Name\tTax_Rank\tCount_Norm\n"
            for tax in self.taxaList:
                pTable += tax.tax_name + "\t" + tax.tax_rank + "\t" + str(tax.percent) + "\n"
            return pTable
        else:
            import prettytable
            uniqueTable = prettytable.PrettyTable(["Tax_Name", "Tax_Rank", "Count_Norm"])
            # for i in self.sampleList:
            #     uniqueTable.add_row([i["tax_name"],i["tax_rank"],i["count_norm"]])
            for i in self._taxaList:
                uniqueTable.add_row([i.tax_name, i.tax_rank, i.count_norm])
            # print(uniqueTable)rs
            return uniqueTable

    def sort(self, sortBy="tax_name"):
        """
        sort the sample (mutably) by sortBy (which can be any of the taxonomy file keys)
        :param  sortBy: str:  any of the valid taxonomy file keys
        :return: bool
        """
        # self._taxaList = sorted(self._taxaList,key=lambda k:k.__getattribute__(sortBy),reverse=True)
        self._taxaList = sorted(self._taxaList, key=lambda k: getattr(k, sortBy), reverse=True)
        return True

    def __str__(self):
        l = len(self.taxaList)
        summary = "length = {}, first few objects:\n".format(l)
        i = 0
        while l> 10 & i < 10:
            summary+="{}\n".format(self._taxaList[i])
            l = l-1
            i+=1
        return summary

    def __repr__(self):
        return "<{}: name=\"{}\">".format(type(self),self.name)

    def taxnames(self):
        """ returns a list of all organisms in this sample
        :return: list
        """
        if self._taxnamelist:  # already computed, so don't recompute
            return self._taxnamelist
        for taxon in self.taxaList:
            self._taxnamelist = self._taxnamelist + [[taxon.tax_name, taxon.tax_rank]]
        return self._taxnamelist

    def diversity(self, rank="family"):
        """ uses Simpson index: http://codegolf.stackexchange.com/questions/53455/simpson-diversity-index

        :param rank: specify the rank that will be used for the calculations. uBiome generally measures at the Family level.
        :return float representing the inverse simpson diversity found in the sample.
        :rtype float
        """
        l = len(self.taxaList)
        s = [(taxa.tax_name, int(taxa.count_norm)) for taxa in self.taxaList if taxa.tax_rank == rank]
        # N = sum(n for (t,n) in s )
        eT, eN = list(zip(*s))
        d = 1 - sum([eN[i] * (eN[i] - 1) for i, j in enumerate(eN)]) / (sum(eN) * (sum(eN) - 1))
        return d  # sum(s[i%l]<>s[i/l]for i in range(l*l))/(l-1.)/l

    def taxaField(self, taxName, field):
        ''' look up taxName in _taxaList and return the field attribute.
        e.g. self.taxaField("Firmicutes","count_norm") will give the count_norm of any Firmicutes in the sample.

        :param taxName:
        :return: the value of the field attribute for this taxa; None if there isn't one.
        :rtype: bool
        '''
        for taxa in self.taxaList:
            if taxa.tax_name == taxName:
                return taxa # getattr(taxa, field, None)
        return None

    def countNormOf(self, taxName):
        """
        returns the count_norm of a given taxName for a sample
        :param taxName: string representation of a uBiome tax_name
        :return: count_norm of taxName; 0 if no such taxName in sample
        :rtype: int
        """
        t = self.taxonOf(taxName)
        if t:
            return t.count_norm
        else:
            return 0

    def taxonOf(self, taxName):
        """
        Returns the full taxon whose tax_name matches taxName, or None of no matches.


        :param taxName:
        :return:
        :rtype ubiome.UbiomeTaxa
        """
        for taxa in self.taxaList:
            if taxa.tax_name == taxName:
                return taxa  # getattr(taxa, field, None)
        return None

        # taxa = self.taxaField(taxName, 'dictForm')
        # if taxa:
        #     return taxa
        # return None

    def unique(self, sample2):
        """
        returns all organisms that are unique to sample 1
        :type sample2: UbiomeSample
        :param sample2:
        :return: UBiomeDiffSample
        """
        uniqueList = []
        for taxon1 in self.taxaList:

            t = [tax for tax in sample2.taxaList if tax.tax_name == taxon1.tax_name]
            if not t:  # not found sample2, so add to the return list
                uniqueList = [UbiomeTaxa({"tax_name": taxon1.tax_name,
                                          "count_norm": taxon1.count_norm,
                                          "tax_rank": taxon1.tax_rank,
                                          "taxon": taxon1.taxon
                                          })] + uniqueList
        return UbiomeDiffSample(uniqueList)

    def addCountsToList(self, taxonList):
        """ given a list of taxa, return another list, of dicts, that contain the same taxa and their corresponding count_norm
        :param taxonList: list # contains taxnames
        :return:
        """
        if not taxonList:
            return []
        else:
            return [{"tax_name": taxonList[0], "count_norm": self.countNormOf(taxonList[0])}] + \
                   self.addCountsToList(taxonList[1:])

    def compareWith(self, sample2):
        """ compare the current sample with sample2 and return a uBiomeDiffSample object of the differences

        :param sample2: UbiomeSample
        :type sample2: UbiomeSample
        :return: UBiomeDiffSample
        :rtype: UbiomeDiffSample
        """

        taxList = []
        for taxon1 in self.taxaList:

            if sample2.taxonOf(taxon1.tax_name):  # found this taxon in sample2
                t = [tax for tax in sample2.taxaList if tax.tax_name == taxon1.tax_name][0]
                countDiff = taxon1.count_norm - t.count_norm
                taxList = [UbiomeTaxa({"tax_name": taxon1.tax_name, \
                                       "taxon": taxon1.taxon, \
                                       "count_norm": countDiff, \
                                       "tax_rank": taxon1.tax_rank})] + taxList
        diffSample = UbiomeDiffSample(taxList)
        return diffSample

    def write(self, filename, ftype="csv"):
        """ write contents of the current sample to a CSV file.  If filename=sys.stdout, just display it

        :param filename: name of file to write to.  Include extension in the string name.
        :type filename: str
        :param ftype: str: default is 'csv' for now, but may add other file types in the future.
        :return:
        """
        if self.taxaList == []:
            return
        else:
            fields = self.taxaList[0].dictForm.keys()
        if filename == sys.stdout:
            ubiomeWriter = csv.DictWriter(sys.stdout, dialect='excel', fieldnames=fields)
            # print('writing to csv')
            ubiomeWriter.writeheader()
            for organism in self.taxaList:
                ubiomeWriter.writerow(organism.dictForm)
        else:
            with open(filename, 'w') as csvFile:
                # print('writing to csv')
                ubiomeWriter = csv.DictWriter(csvFile, dialect='excel', fieldnames=fields)
                ubiomeWriter.writeheader()
                for organism in self.taxaList:
                    ubiomeWriter.writerow(organism.dictForm)


class UbiomeDiffSample(UbiomeSample):
    """ same as regular uBiomeSample, except count_norm is a delta, not an absolute number. Also gives you a new key, percent.


    """

    def __init__(self, taxaList):
        self.name = "Diff"
        self._taxaList = [UbiomeTaxa({"tax_name": tax.tax_name, \
                           "count_norm": tax.count_norm, \
                           "percent": tax.percent, \
                           "tax_rank": tax.tax_rank, \
                           "taxon": tax.taxon
                           }) for tax in taxaList]


class ubiomeApp():
    """
    app-ified version to make testing easier.
    """

    def __init__(self, fname1, fname2):
        self.sample1 = UbiomeSample(fname1)
        self.sample2 = UbiomeSample(fname2)

    def testUnique(self):
        unique = self.sample1.unique(self.sample2)
        return len(unique.taxaList)
        # print("len esample.unique",len(unique.sampleList))
        # unique.writeCSV("sample1Unique.csv")

    def runUnique(self):
        unique = self.sample1.unique(self.sample2)
        # print("len esample.unique",len(unique.sampleList))
        unique.write(sys.stdout)

    def testCompare(self):
        compare = self.sample1.compareWith(self.sample2)
        # compare.writeCSV("sample1Compare.csv")
        return compare

    def runCompare(self):
        compare = self.sample1.compareWith(self.sample2)
        compare.write(sys.stdout)
        # compare.prettyPrint()
        return compare



# if __name__ == "__main__":
#     # print("run uBiomeCompare.py")
#     # import doctest
#     print("run as a script")
#

