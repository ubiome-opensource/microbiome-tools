# ubiome_example: a simple Python script showing how to use the ubiome Python library
# makes a single CSV file where each column is a unique sample

from ubiome import UbiomeSample, UbiomeDiffSample, UbiomeMultiSample

my_sample = UbiomeSample()

my_sample.load("ubiome/testdata/sample1.json")

my_sample.showContents() # useful for debugging


import os
def ubiome_tax_filenames (walk_dir,site="gut"):
    """
    Returns a list of all files in walk_dir that are type JSON
    :param walk_dir: str
    :param site: str
    :return: list
    """

    tax_filenames = []

    for root, subdirs, files in os.walk(walk_dir):
        # print('--\nroot = ' + root)
        # list_file_path = os.path.join(root, 'my-directory-list.txt')
        # print('list_file_path = ' + list_file_path)

        # with open(list_file_path) as list_file:
        # for subdir in subdirs:
        #     print('\t- subdirectory ' + subdir)

        for filename in files:
            file_path = os.path.join(root, filename)
            fname, file_extension = os.path.splitext(file_path)
            if file_extension == ".json" : # and "gut" in fname:
                # print('\t- file %s (extension: %s)' % (filename, file_extension))
                # print("file:",file_path)
                tax_filenames.append(file_path)
    return tax_filenames


test_dir = "./ubiome/testdata/"

all_JSON_files = ubiome_tax_filenames(test_dir)


first_sample = UbiomeSample(name=all_JSON_files[0])
first_sample.load(all_JSON_files[0])

all_samples = UbiomeMultiSample(first_sample)

for sample_file in all_JSON_files[1:]:
    next_sample = UbiomeSample(name=sample_file)
    next_sample.load(sample_file)
    all_samples.merge(next_sample)


all_samples.write("example.csv")






