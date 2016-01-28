# ubiome_example: a simple Python script showing how to use the ubiome Python library

from ubiome import UbiomeSample, UbiomeDiffSample, UbiomeMultiSample

my_sample = UbiomeSample()

my_sample.readJSONfile("ubiome/testdata/sample1.json")

my_sample.showContents() # useful for debugging

MD1 = UbiomeSample(name="MD1")

MD1.read_CSV_file("/Users/sprague/OneDrive/Projects/uBiome/Data/Others/MarkDittman1510.csv")
MD2 = UbiomeSample("/Users/sprague/OneDrive/Projects/uBiome/Data/Others/MarkDittman1512.json",name="MD2")

MDAll = UbiomeMultiSample(MD1)

MDAll.merge(MD2)

MDAll.writeCSV("MDSamplesAll.csv")




