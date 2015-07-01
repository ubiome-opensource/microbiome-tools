#Using the uBiome Tools Repository

Please add your tools here, and edit this file to keep a directory of scripts, programs, templates, or anything else you find useful for manipulating or analyzing uBiome information.


**RuBiome: simple scripts in R**

```
# returns a dataframe showing how the two samples compare
# returns the count_norm of sample2 - sample1 (i.e. positive numbers indicate more in sample2)
uBiome_compare_samples <- function(sample1,sample2,rank="species")
```
