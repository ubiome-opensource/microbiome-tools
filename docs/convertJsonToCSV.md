#Convert JSON files to CSV#

This is a useful utility for quickly converting a whole directory of
uBiome JSON files into CSV.

From R, set the working directory to the location where you saved the uBiome file.

Then type this in R:
```
> source('uBiomeConvertToCSV.R')

```
Set your working directory to the location of the data files you
want to convert to CSV. For example:
```
>setwd("/data")
```
```
convert_json_files_to_csv()
```
Now every .json file in that directory will be converted to .csv

Try opening in Excel: they'll be _much_ easier to read.
