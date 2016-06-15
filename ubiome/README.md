Using the Ubiome Python Library
---

uBiome is a citizen science company that collects and analyzes samples of the human microbiome. Send them your sample and they will process it using the information contained in the 16S subregion of the bacterial genome and send you the results.

Advanced users have access to the raw data, including the original FASTQ files from uBiome's Illumina NextSeq500 machine as well as a JSON-encapsulated summary of the results.

This library will help you look at the JSON summary.

Main Functions
---

Until more documentation is available, please see the [ubiome-example](microbiome-tools/ubiome_example.py) to see how this works.

# Super Short Intro

If you already have your uBiome results downloaded and you know how to use a command line interface on your computer (either Terminal on a Mac or Powershell on Windows), type

    $ pip ubiome

  to download the uBiome Python library from the Python Package Index.

  Let's assume you already have two uBiome JSON files available in your current directory, like this:

    $ ls
    sample1.json  sample2.json  x.csv
    $ python
    >>> from ubiome import *
    >>> x1 = UbiomeSample("sample1.json")
    >>> x2 = UbiomeSample("sample2.json")
    >>> x = UbiomeMultiSample(x1)
    >>> x.merge(x2)
    >>> x.write("x.csv")
    
Your directory will now contain the file ```x.csv``` that has all your uBiome results 