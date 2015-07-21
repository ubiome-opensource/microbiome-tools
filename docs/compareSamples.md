#Compare uBiome Samples (R version)#

To use this tool, type this in R:
```
> source('uBiomeCompare.R')

```
If you have two uBiome CSV files, (for example, named ```may``` and ```jun```)
try this:

```
> uBiome_compare_samples(may,jun,"phylum")
tax_name count_change
1   Acidobacteria         1650
2  Actinobacteria        -2650
3   Bacteroidetes        43539
4      Firmicutes      -159498
5  Proteobacteria       126488
6     Tenericutes        -3870
7 Verrucomicrobia       -11697
>
```
Instead of "phylum", you could also any uBiome ```tax_rank``, including
 "species", "genus", "superkingdom", or others as shown here:
 ```
 > levels(may$tax_rank)
 [1] "class"         "family"        "genus"         "no_rank"       "order"         "phylum"
 [7] "species"       "species_group" "subclass"      "suborder"      "subphylum"     "superkingdom"
 [13] "superphylum"
 ```
