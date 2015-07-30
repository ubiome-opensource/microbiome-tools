
"""

This section is for brief in-app doc testing.

To run, type
python ubiomeCompare -c "../Data/sprague data/Sprague-ubiomeMay2014.json" "../Data/sprague data/Sprague-uBiomeJun2014.json"

>>> myApp.testUnique()
384
>>> v=myApp.testCompare()
>>> len(v.sampleList)
139
>>> testRikAll()
length of fullTaxList= 939
[['tax_name', 'tax_rank'], ['Bacteria', 'superkingdom'], ['Firmicutes', 'phylum'], ['Clostridia', 'class'], ['Clostridiales', 'order'], ['Bacteroidetes/Chlorobi group', 'superphylum'], ['Bacteroidetes', 'phylum'], ['Bacteroidia', 'class'], ['Bacteroidales', 'order'], ['Ruminococcaceae', 'family']]
length of samples= 8
May 2014 ---> 939
Jun 2014 ---> 939
Oct 2014 ---> 939
Jan 2015 ---> 939
Feb 2015 ---> 939
Apr21 ---> 939
Apr28 ---> 939
Jun 2015 ---> 939
latest sample: ['Jun 2015', 1000000, 684322, 673988, 673880, 219758, 219758, 217323, 216241, 406568]


>>> 5+5
10

"""

__author__ = 'sprague'

import ubiome
import sys
import prettytable

def testRikAll():
    may14 = ubiome.UbiomeSample("../Data/sprague data/Sprague-ubiomeMay2014.json",name="May 2014")
    jun14 = ubiome.UbiomeSample("../Data/sprague data/sprague-uBiomeJun2014.json",name="Jun 2014")
    oct14 = ubiome.UbiomeSample("../Data/sprague data/Sprague-uBiomeOct2014.json",name="Oct 2014")
    jan = ubiome.UbiomeSample("../Data/sprague data/sprague-ubiomeJan2015x.json",name="Jan 2015")
    feb = ubiome.UbiomeSample("../Data/sprague data/sprague-ubiomeFeb2015.json",name="Feb 2015")

    aprA = ubiome.UbiomeSample("../Data/sprague data/sprague-ubiome-150421.json",name = "Apr21")
    aprB = ubiome.UbiomeSample("../Data/sprague data/sprague-ubiome-150428.json",name = "Apr28")
    jul = ubiome.UbiomeSample("../Data/sprague data/Sprague-ubiomeJul2015.json",name = "Jun 2015")

    aprJulc = aprB.compareWith(jul)
    aprJulu = aprB.unique(jul)

    aprJulu.sort("count_norm")
    aprJuluPretty = aprJulu.prettyPrint()

    #aprJulu.writeCSV(sys.stdout)
    #aprJulu.prettyPrint()

    x = ubiome.UbiomeMultiSample(may14)
    x.merge(jun14)
    x.merge(oct14)
    x.merge(jan)
    x.merge(feb)
    x.merge(aprA)
    x.merge(aprB)
    x.merge(jul)
    #x.writeCSV(sys.stdout)
    x.showContents()
   # x.writeCSV("spragueResults.csv")

DEBUG = True


if DEBUG:
    #myApp.testUnique()
    #v = myApp.testCompare(myApp.esample,myApp.msample)
    import doctest
    myApp = ubiome.ubiomeApp( "../Data/sprague data/Sprague-ubiomeMay2014.json" , "../Data/sprague data/Sprague-uBiomeJun2014.json")
    testRikAll()
    doctest.testmod()
    print("all tests successful")

print("starting program now")


myApp = ubiome.ubiomeApp( "../Data/sprague data/Sprague-ubiomeMay2014.json" , "../Data/sprague data/Sprague-uBiomeJun2014.json")


#myApp.sample1.showContents()
sample1=myApp.sample1
sample2=myApp.sample2

#sample2.unique(sample1).showContents()
#sample1.compareWith(sample2).showContents()




#
# uniqueTable = prettytable.PrettyTable(["Tax_Name","Tax_Rank","Count_Norm"])
# for i in aprJulu.sampleList:
#     uniqueTable.add_row([i["tax_name"],i["tax_rank"],i["count_norm"]])
#
# print(uniqueTable)



