# Compare two uBiome samples (Python)

Download the script [ubiome.py](../ubiome.py) to the same folder where you have two uBiome taxonomy files you want to compare. 

## Command line version (easiest)

On the Macintosh, open the ```Terminal``` application and at the prompt type:

```
> python ubiome.py -h
```

You should see the following:

```

usage: ubiome.py [-h] [-c COMPARE] [-u UNIQUE] [-d DEBUG] sample2

positional arguments:
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
> python ubiome.py -c sample1.json sample2.json

```

You will see several lines of comma-separated values indicating the difference in `count_norm` values between the two samples.

You can also type the following to save the results to the file "compare12.csv"

```
> python ubiome.py -c sample1.json sample2.json > compare12.csv

```

Similarly, to see the unique organisms in one sample compared to the other, type:

```
> python ubiome.py -u sample1.json sample2.json > unique12.csv

```

## Module version (requires knowledge of Python)

Write your own Python script. Here's an example using JSON files from the current directory:

	import ubiome
	# create a new instance of class UbiomeSample, initialized to a json file
	jul = ubiome.UbiomeSample("Sprague-ubiomeJul2015.json")
	apr = ubiome.UbiomeSample("sprague-ubiome-150428.json")

	# these variables hold instances of class UbiomeDiffSample
	aprJulc = apr.compareWith(jul)
	aprJulu = apr.unique(jul)

	# sort them, pretty-print them
	aprJulu.sort("count_norm")
	aprJuluPretty = aprJulu.prettyPrint() 
	aprJulu.writeCSV("AprJulUnique.csv")  # or write to a CSV file on disk


You can also merge several sample files together to make a big CSV file where the first row is all the taxons ever found in your samples, and the other columns are your different samples, with rows containing the `count_norm` for every taxon.  

Example, given two samples (JSON files read from current directory)

	aprB = ubiome.UbiomeSample("sprague-ubiome-150428.json",name = "Apr28")
    jul = ubiome.UbiomeSample("Sprague-ubiomeJul2015.json",name = "Jun 2015")
    x = ubiome.UbiomeMultiSample(aprB)
    x.merge(jul)
    x.writeCSV("combinedResults.csv")
    
This will leave you the file "combinedResults.csv" with the combined `count_norm`s for your two samples






