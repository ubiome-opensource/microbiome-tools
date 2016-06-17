__author__ = 'sprague'

import unittest
import datetime




# I recognize it's not ideal to import straight from the current directory
# eventually all tests should be moved out of the package directory, or find a better way to do this.
import ubiome

import ubiomeMultiSample

#from ..ubiome import UbiomeMultiSample

pathPrefix="./testdata/"
s1 = ubiome.UbiomeSample(pathPrefix+"sample1.json",name="sample1")
s2 = ubiome.UbiomeSample(pathPrefix+"sample2.json",name="sample2")
s3 = ubiome.UbiomeSample(pathPrefix+"sample3.json",name="sample2")
s4 = ubiome.UbiomeSample(pathPrefix+"sample4.json",name="sample2")
may14 = ubiome.UbiomeSample(pathPrefix+"Sprague-ubiomeMay2014.json",name="May 2014")
jun14 = ubiome.UbiomeSample(pathPrefix+"sprague-uBiomeJun2014.json",name="Jun 2014")
aug15 = ubiome.UbiomeSample(name="Aug 2015")
aug15.load(pathPrefix + "Sprague-ubiome-150815.csv",ftype="CSV")
aug = aug15 #ubiome.UbiomeSample(pathPrefix+"Sprague-ubiome-150815.json",name = "Aug 2015")


class MyTestCase(unittest.TestCase):

    def setUp(self):
        x = ubiomeMultiSample.UbiomeMultiSample(may14)
        x.merge(jun14)
        x.merge(aug)
        self.sampleMultiSample = x

    def test_unique(self):
        v = may14.unique(jun14)
        self.assertEqual(v.taxaList[8].percent,0.0008)
        self.assertEqual(len(v.taxaList), 384)
        
    def test_compare_with(self):
        v = may14.compareWith(jun14)
        self.assertEqual(v.taxaList[5].count_norm,-124739)
        self.assertEqual(len(v.taxaList),139)

    def test_taxList_count_norm_is_integer(self):
        v = may14._taxaList[0].count_norm
        self.assertIsInstance(v,int)

    def test_sort_keeps_length_constant(self):
        v = len(s1._taxaList)
        s1.sort("count_norm")  # remember that sort is mutable.
        self.assertEqual(len(s1._taxaList),v)

    def test_addCountsToList(self):
        v = may14.addCountsToList(["Roseburia","Akkermansia"])
        self.assertEqual(v,[{'tax_name': 'Roseburia', 'count_norm': 13554}, {'tax_name': 'Akkermansia', 'count_norm': 30960}])

    def test_CountNormOf(self):
        v = may14.countNormOf("Clostridiales")
        self.assertEqual(v,594169)

    def test_diversity(self):
        v = s1.diversity()
        self.assertEqual(v,0.5001489102477326)

    def test_diversity_rank_genus(self):
        v = s1.diversity(rank="genus")
        self.assertEqual(v,0.2064177920125012)

    def test_taxonOf(self):
        v = may14.taxonOf("Clostridiales")
        self.assertEqual(v,{'taxon': '186802', 'count': 150137, 'tax_rank': 'order', 'avg': None, 'tax_color': None, 'tax_name': 'Clostridiales', 'parent': '186801', 'count_norm': 594169})

    def test_sampleFullTaxListLength(self):
        self.assertEqual(len(self.sampleMultiSample.fullTaxList), 795)
    def test_sampleTaxList(self):
        firstTenVals = [['tax_name', 'tax_rank'], ['Bacteria', 'superkingdom'], ['Firmicutes', 'phylum'], ['Clostridia', 'class'], ['Clostridiales', 'order'], ['Bacteroidetes/Chlorobi group', 'superphylum'], ['Bacteroidetes', 'phylum'], ['Bacteroidia', 'class'], ['Bacteroidales', 'order'], ['Ruminococcaceae', 'family']]
        self.assertEqual(firstTenVals,[self.sampleMultiSample.fullTaxList[i] for i in range(10)])

    def test_latestSample(self):
        latestSample = ['Aug 2015', 1000000, 642701, 622361, 622244, 184516, 184508, 184204, 184136, 307556]
        self.assertEqual(latestSample,[self.sampleMultiSample.samples[len(self.sampleMultiSample.samples)-1][i] for i in range(10)])

    def test_sort(self):
        self.assertEqual(jun14.taxaList[-1].tax_name,'Anaerostipes hadrus')
        jun14.sort("tax_name")
        v = jun14.taxaList[-1].tax_name
        self.assertEqual(v,'Achromobacter')

    def test_multisample_init(self):
        v = ubiomeMultiSample.UbiomeMultiSample(may14)
        self.assertEqual(len(v.fullTaxList),len(may14.taxaList)+1)
        self.assertEqual(v.fullTaxList[57][0],may14.taxaList[56].tax_name) # +1 because fullTaxList[0]="tax_rank"

    def test_alltaxa_isList(self):
        self.assertEqual(len(self.sampleMultiSample.alltaxa()),795)

    def test_found_metadata(self):
        self.assertEqual(s3.datetime, datetime.datetime(2016,1,11,0,0))
        self.assertEqual(s3.site,"mouth")
        self.assertEqual(s2.site,"gut")
        self.assertEqual(s1.datetime,datetime.datetime(2000,1,1,0,0))
        self.assertEqual(s1.date, datetime.date(2000, 1, 1))
        self.assertEqual(s4.date, datetime.date(2015, 8, 22))
        self.assertEqual(s4.datetime,datetime.datetime(2015,8,22,3,0))

    def tearDown(self):
        pass



if __name__ == '__main__':
    unittest.main()
