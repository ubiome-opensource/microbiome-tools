Using the Ubiome Python Library
---

uBiome is a citizen science company that collects and analyzes samples of the human microbiome. Send them your sample and they will process it using the information contained in the 16S subregion of the bacterial genome and send you the results.

Advanced users have access to the raw data, including the original FASTQ files from uBiome's Illumina NextSeq500 machine as well as a JSON-encapsulated summary of the results.

This library will help you look at the JSON summary.

Until more documentation is available, please see the [ubiome-example](microbiome-tools/ubiome_example.py) to see how this works.

## Super Short Intro

If you already have your uBiome results downloaded and you know how to use a command line interface on your computer (either Terminal on a Mac or Powershell on Windows), type


    $ pip install ubiome

  to download the uBiome Python library from the Python Package Index.

  Let's assume you already have two uBiome JSON files available in your current directory, like this:

    $ ls
    sample1.json  sample2.json
    $ python
    >>> from ubiome import *
    >>> x1 = UbiomeSample("sample1.json")
    >>> x2 = UbiomeSample("sample2.json")
    >>> x = UbiomeMultiSample(x1)
    >>> x.merge(x2)
    >>> x.write("x.csv")
    
Your directory will now contain the file ```x.csv``` that has all your uBiome results laid out in a spreadsheet form like this:

| tax_name                           | tax_rank     | sample1.json | sample2.json | 
|------------------------------------|--------------|--------------|--------------| 
| Bacteria                           | superkingdom | 1000000      | 1000000      | 
| Firmicutes                         | phylum       | 622877       | 463379       | 
| Dialister                          | genus        | 6039         | 0            | 
| Desulfovibrio                      | genus        | 799          | 0            | 
| environmental samples              | no_rank      | 799          | 0            | 
| Desulfovibrio sp. oral clone BB161 | species      | 780          | 0            | 
| Ruminococcus faecis                | species      | 772          | 0            | 
| ...                                |              |              |              | 

You should know what to do at this point. Filter by tax_rank, sort by column, etc.  If you want to convert everything to percentages, divide the integers by 10,000.