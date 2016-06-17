Using the Ubiome Python Library
-------------------------------

`uBiome <http://ubiome.com>`__ is a citizen science company that
collects and analyzes samples of the human microbiome. Send a sample
and have it processed using the information contained in the
16S ribosomal subunit of the bacterial genome.

Advanced users have access to the raw data, including the original FASTQ
files from uBiome's Illumina NextSeq500 machine as well as a
JSON-encapsulated summary of the results.

This library will help you analyze and process the JSON summary.

Main Functions
--------------

Until we have complete documentation, please see the
`ubiome-example <microbiome-tools/ubiome_example.py>`__ to see how this
works.

Get Started Quickly
-------------------

If you already have your uBiome results downloaded and you know how to
use a command line interface on your computer (either Terminal on a Mac
or Powershell on Windows), type

::

    $ pip install ubiome

to download the uBiome Python library from the Python Package Index.

If you already have two uBiome JSON files available in your current
directory, like this:

::

    $ ls

    sample1.json  sample2.json  x.csv

Run the following series of commands in your Python 2+ or 3+ console:

::

    $ python

    >>> from ubiome import *
    >>> x1 = UbiomeSample("sample1.json")
    >>> x2 = UbiomeSample("sample2.json")
    >>> x = UbiomeMultiSample(x1)
    >>> x.merge(x2)
    >>> x.write("x.csv")

Now your directory will have a new file ``x.csv`` with both samples
merged.

Class uBiomeSample
~~~~~~~~~~~~~~~~~~

::

    class UbiomeSample
         |  class representation of a well-formed uBiome sample
         |
         |  Methods defined here:
         |
         |  __init__(self, fname='', name='', date=datetime.date(2000, 1, 1), site='gut')
         |      initialize with a string representing the path to a uBiome-formatted JSON file
         |      If no name, just instantiate an object; you can read the contents later using self.load()
         |      :param fname : filename
         |      :param name: name for the sample
         |      :type name: str
         |      :type fname: str
         |      :type date: datetime.date
         |
         |  __repr__(self)
         |
         |  __str__(self)
         |
         |  addCountsToList(self, taxonList)
         |      given a list of taxa, return another list, of dicts, that contain the same taxa and their corresponding count_norm
         |      :param taxonList: list # contains taxnames
         |      :return:
         |
         |  compareWith(self, sample2)
         |      compare the current sample with sample2 and return a uBiomeDiffSample object of the differences
         |
         |      :param sample2: UbiomeSample
         |      :type sample2: UbiomeSample
         |      :return: UBiomeDiffSample
         |      :rtype: UbiomeDiffSample
         |
         |  countNormOf(self, taxName)
         |      returns the count_norm of a given taxName for a sample
         |      :param taxName: string representation of a uBiome tax_name
         |      :return:
         |
         |  diversity(self, rank='family')
         |      uses Simpson index: http://codegolf.stackexchange.com/questions/53455/simpson-diversity-index
         |
         |      :param rank: specify the rank that will be used for the calculations. uBiome generally measures at the Family level.
         |      :return float representing the inverse simpson diversity found in the sample.
         |      :rtype float
         |
         |  load(self, fname, ftype='JSON')
         |      read a JSON file of the uBiome taxonomy (the one you get from downloading from the uBiome web site)
         |      :type fname: str
         |      :param fname: the string filename containing JSON data
         |      :param ftype: currently unused, but provided for future compatibility
         |      :type ftype: str
         |      :return:
         |      :rtype None
         |
         |  prettyPrint(self)
         |      print a nice ascii table of the sample if you have the PIP module 'prettytable' available.
         |      :return: prettytable
         |
         |  set_taxaList_JSON(self, sourceJson)
         |      :param  sourceJson: a dict representation of a well-formed uBiome dictionary
         |      :type sourceJson: dict
         |      :return:
         |
         |  sort(self, sortBy='tax_name')
         |      sort the sample (mutably) by sortBy (which can be any of the taxonomy file keys)
         |      :param  sortBy: str:  any of the valid taxonomy file keys
         |      :return: bool
         |
         |  taxaField(self, taxName, field)
         |      look up taxName in _taxaList and return its attribute corresponding to 'field'
         |      :param taxName:
         |      :return:
         |
         |  taxnames(self)
         |      returns a list of all organisms in this sample
         |      :return: list
         |
         |  taxonOf(self, taxName)
         |
         |  unique(self, sample2)
         |      returns all organisms that are unique to sample 1
         |      :type sample2: UbiomeSample
         |      :param sample2:
         |      :return: UBiomeDiffSample
         |
         |  write(self, filename, ftype='csv')
         |      write contents of the current sample to a CSV file.  If filename=sys.stdout, just display it
         |
         |      :param filename: name of file to write to.  Include extension in the string name.
         |      :type filename: str
         |      :param ftype: str: default is 'csv' for now, but may add other file types in the future.
         |      :return:
         |
