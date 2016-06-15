## Analyze uBiome samples in Python


The [ubiome Python library](../ubiome) works as either a script or a module that you can `import` into your own code. It can do the following:

* Compare two samples to find the unique organisms in each.
* Compare two samples and show the differences in counts for each.
* Merge more than one sample into a single large spreadsheet.

If you are already familiar with the basics of Python programming, see the script [ubiome_example.py](ubiome_example.py) for a complete example.


## Compare two samples


### Command line version (easiest)

Download the folder [ubiome](../ubiome) to the same folder where you have two uBiome taxonomy files you want to compare.

On the Macintosh, open the ```Terminal``` application and in the directory where you downloaded the files, type:

```
> python ubiome -h
```
You should see the following:

```
usage: ubiome.py [-h] [-c COMPARE] [-u UNIQUE] [-d DEBUG] sample1 sample2

positional arguments:
  sample1               filename for a valid uBiome JSON taxonomy file
  sample2               sample you are comparing to

optional arguments:
  -h, --help            show this help message and exit
  -c COMPARE, --compare COMPARE
                        Compare sample1 with with sample2
  -u UNIQUE, --unique UNIQUE
                        Find items in sample1 not in sample2
  -d DEBUG, --debug DEBUG
                        turn debug mode to run tests

```                      

To compare two samples, type:

```

> python ubiome -c sample1.json sample2.json
```

You will see several lines of comma-separated values indicating the difference in `count_norm` values between the two samples.

You can also type the following to save the results to the file "compare12.csv"

```
> python ubiome -c sample1.json sample2.json > compare12.csv
```

Similarly, to see the unique organisms in one sample compared to the other, type:

```
> python ubiome -u sample1.json sample2.json

```

## Module version (requires knowledge of Python)

Download the enclosed 'ubiome' directory to make the ```ubiome``` module available on your computer (either Python 2 or 3).

A simpler way, if you have the PIP command available on your system:

    $ pip ubiome

to download the uBiome Python library from the Python Package Index.

The following example assumes you downloaded two uBiome JSON files into your current directory, like this:

    $ ls

    sample1.json  sample2.json  x.csv

Run the following series of commands in your Python 2+ or 3+ console:

    $ python

    >>> from ubiome import *
    >>> x1 = UbiomeSample("sample1.json")
    >>> x2 = UbiomeSample("sample2.json")
    >>> x = UbiomeMultiSample(x1)
    >>> x.merge(x2)
    >>> x.write("x.csv")

Now your directory will have a new file ```x.csv``` with both samples merged. The first row is all the taxons ever found in your samples, and the other columns are your different samples, with rows containing the `count_norm` for every taxon.





