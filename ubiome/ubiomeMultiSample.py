
import sys
import csv

class UbiomeMultiSample(object):
    """
    merge a bunch of samples into a single data frame called 'samples'
    [ fullTaxList, sample1Quantities, sample2Quantities, ... ]

    fullTaxList is a list containing strings of tax_name; fullTaxList[0] = "tax_name"
    sampleQuantities is a list where sampleQuantities[0] = "July"  and [1..n] correspond to Quants for fullTaxList[1..n]

    usage: (assuming sample1 and sample2 are of class UbiomeSample)

    x = UbiomeMultiSample()  # initializing
    x.merge(sample1)
    x.merge(sample2)

    """
    def __init__(self,newSample = None):
        """
        Initialize with an existing sample. If you don't specify a sample, the first call to self.merge will add one.
        :type newSample: UbiomeSample.UbiomeSample
        :rtype: UbiomeMultiSample
        :ivar self.fullTaxList: list of all taxa found in any of the samples.

        """
        self.fullTaxList = [["tax_name","tax_rank"]]
        self.originalSampleObjects = []

        self.samples = []
        if newSample:
            self.fullTaxList +=newSample.taxnames()
#            self.samples+=[[newSample.name]+[sample["count_norm"] for sample in newSample.sampleList]]
            self.samples+=[[newSample.name]+[sample.count_norm for sample in newSample.taxaList]]
            self.originalSampleObjects.append(newSample)


    def alltaxa(self):
        ''' returns just the taxa in this multisample

        :return: list of all taxa in this sample
        :rtype: list
        '''
        alltaxa = []
        for sample in self.fullTaxList:
            taxa = sample[0]
            alltaxa += [taxa]
        return alltaxa


    def showContents(self):
        """
        Prints a short representation of the UbiomeMultiSample. Useful for debugging
        :return:
        :rtype: None
        """
        print("length of fullTaxList=",len(self.fullTaxList))
        print([self.fullTaxList[i] for i in range(10)])
        print("length of samples=",len(self.samples))
        for sample in self.samples:
            print(sample[0],"--->",len(sample))
        print("latest sample:",[self.samples[len(self.samples)-1][i] for i in range(10)])

    def __str__(self):
        return "UbiomeMultiSample: len=" + str(len(self.fullTaxList)) + "\n" + "latest sample:"+str([self.samples[len(self.samples)-1][i] for i in range(10)])


    def merge(self,sample2):
        """ merge the current multiSample with sample2.  This operation is mutable
        so you permanently modify the current UbiomeMultiSample when you do this.

        :type sample2: UbiomeSample
        :return:
        """

        if len(self.fullTaxList)==1: #special case when there are no existing samples
            self.fullTaxList +=sample2.taxnames()
            self.samples+=[[sample2.name]+[sample.count_norm for sample in sample2.taxaList]]
            return True

        # find the taxNames missing from fullTaxList
        newTaxNamesL = []
        sampleTaxNames = sample2.taxnames()


        for i,taxName in enumerate(sampleTaxNames):
            if taxName not in self.fullTaxList:
                newTaxNamesL+=[taxName]


        self.fullTaxList+=newTaxNamesL
        newTaxons = [sample2.taxonOf(taxa[0])for taxa in newTaxNamesL]

        oldSamplesList = self.samples[len(self.samples)-1]
        newSampleCountsForPreviousTaxa = []
        for i in range(len(oldSamplesList)-1):
            taxonForTaxName = sample2.taxonOf(self.fullTaxList[i+1][0])
            if taxonForTaxName:
                taxCount = taxonForTaxName["count_norm"]
            else: taxCount = 0
            newSampleCountsForPreviousTaxa+=[taxCount]
        newCounts =  newSampleCountsForPreviousTaxa + [taxon["count_norm"] for taxon in newTaxons]

        self.samples += [[sample2.name] + newCounts]
        self.originalSampleObjects.append(sample2)

        # new length of a sample is len(newTaxons)+ len(oldSamplesList)
        # fill previous samples with count_norm = 0
        for i, sample in enumerate(self.samples):
            if len(self.samples[i])<(len(newCounts)+1):
                self.samples[i]=self.samples[i] + [0 for k in range(len(newTaxons))]

    def write(self, filename, ftype="csv"):
        """ write the merged bunch of sample to a single CSV file (or sys.stdout)

        :type filename: str
        :param filename: name of file to write to. Include extension
        :return:
        """
        if filename==sys.stdout:
            ubiomeWriter = csv.DictWriter(sys.stdout,dialect='excel',fieldnames=["tax_name"]+ ["tax_rank"] + [sample[0] for sample in self.samples])
            #ubiomeWriter.writeheader()
            for i,taxa in enumerate(self.fullTaxList):
                taxName, taxRank = taxa
                rowDict = ["tax_name",taxName]
                rankDict = ["tax_rank",taxRank]
                sampleDict = [[sample[0],sample[i]] for sample in self.samples]
                ubiomeWriter.writerow(dict([rowDict]+[rankDict] +sampleDict))
        else:
            with open(filename,'w') as csvFile:
                ubiomeWriter = csv.DictWriter(csvFile, dialect='excel',fieldnames=["tax_name"]+ ["tax_rank"] + [sample[0] for sample in self.samples])
                #print('writing to csv')
                #ubiomeWriter.writeheader()
                for i,taxa in enumerate(self.fullTaxList):
                    taxName, taxRank = taxa
                    rowDict = ["tax_name",taxName]
                    rankDict = ["tax_rank",taxRank]
                    sampleDict = [[sample[0],sample[i]] for sample in self.samples]
                    ubiomeWriter.writerow(dict([rowDict]+[rankDict] +sampleDict))

