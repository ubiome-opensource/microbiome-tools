
"""

This section is for brief in-app doc testing.

To run, type
python ubiomeCompare -c "../Data/sprague data/Sprague-ubiomeMay2014.json" "../Data/sprague data/Sprague-uBiomeJun2014.json"

>>> myApp.testUnique()
384
>>> v=myApp.testCompare()
>>> len(v.sampleList)
139

>>> 5+5
10

"""

__author__ = 'sprague'

import ubiome
import sys

DEBUG = True

if DEBUG:
    #myApp.testUnique()
    #v = myApp.testCompare(myApp.esample,myApp.msample)
    import doctest
    myApp = ubiome.ubiomeApp( "../Data/sprague data/Sprague-ubiomeMay2014.json" , "../Data/sprague data/Sprague-uBiomeJun2014.json")
    doctest.testmod()
    print("all tests successful")

print("starting program now")

#myApp.sample1.showContents()
sample1=myApp.sample1
sample2=myApp.sample2

#sample2.unique(sample1).showContents()
#sample1.compareWith(sample2).showContents()

jul = ubiome.UbiomeSample("../Data/sprague data/Sprague-ubiomeJul2015.json")
apr = ubiome.UbiomeSample("../Data/sprague data/sprague-ubiome-150428.json")

aprJulc = apr.compareWith(jul)
aprJulu = apr.unique(jul)

aprJulu.writeCSV(sys.stdout)


