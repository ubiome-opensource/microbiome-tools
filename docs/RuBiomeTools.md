#R Tools for uBiome#

These tools will help you analyze your uBiome results.

Log into your [uBiome account](http://apps.ubiome.com)

Select "Raw Taxonomy", like this:

![Raw taxonomy](./images/ScreenShot Raw Taxonomy.jpg)

you'll see a screen that looks something like this:

![JSON](./images/uBiome json screenshot.png)

From inside your browser, Save As.. to a filename ending with '.json'.

Launch R, then set the working directory to the location
where you saved the uBiome JSON file. For example:

```
setwd("/ubiome")  # enter the path for your directory here
```
(Note that everything after the '#' is a comment and doesn't need to be typed.

Now you are ready to begin using the tools. To load them, type:

```
source("uBiomeConvertToCSV.R") # or another filename, depending on which tool.

```
