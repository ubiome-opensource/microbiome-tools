# Compare two uBiome samples (Python)

Download the script ubiomeCompare.py to the same folder where you have two uBiome taxonomy files you want to compare. 

On the Macintosh, open the ```Terminal``` application and at the prompt type:

```
> python ubiomeCompare.py -h
```

You should see the following:

```

usage: ubiomeCompare.py [-h] [-c COMPARE] [-u UNIQUE] [-d DEBUG] sample2

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
> python ubiomeCompare.py -c sample1.json sample2.json

```

You will see several lines of comma-separated values indicating the difference in `count_norm` values between the two samples.

You can also type the following to save the results to the file "compare12.csv"

```
> python ubiomeCompare.py -c sample1.json sample2.json > compare12.csv

```

Similarly, to see the unique organisms in one sample compared to the other, type:

```
> python ubiomeCompare.py -u sample1.json sample2.json > unique12.csv

```









