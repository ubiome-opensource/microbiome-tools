# ubiome_sweep.py : runs through a directory, loading all ubiome taxonomy files

# The directory contains a series of subdirectories like this:
# ub-data-<name>
#      README.md # first line is name, etc.  rest of text is free-flow description of the person
#      <name>-<site>-<date>.json
#


import os
import sys

def ubiome_tax_filenames (walk_dir,site="gut"):
    """
    Returns a list of all files in walk_dir that are type JSON and have 'gut' in their filename
    :param walk_dir:
    :param site:
    :return:
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
            if file_extension == ".json" and "gut" in fname:
                # print('\t- file %s (extension: %s)' % (filename, file_extension))
                # print("file:",file_path)
                tax_filenames.append(file_path)
    return tax_filenames

print(ubiome_tax_filenames(os.getcwd()))

import errno


def make_dirs_from_people_list(fname):
    """
    read the text file fname and create new directories based on the names therein, in the current working directory
    :param str: fname
    :return:
    """
    with open(fname,'r') as people_file:
        x=people_file.read().splitlines()


    for n in x:
        #print("ub-data-",n.replace(" ","_"),sep="")
        newdir="ub_data-"+n.replace(" ","_")
        print(newdir)
        try:
            os.makedirs(newdir)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise


# run the following line only once:
#make_dirs_from_people_list("/Users/sprague/OneDrive/Projects/microbiome-tools/ubiome_people.txt")

import csv
import json

def ubiome_convert_csv_json(fname):
    """
    This doesn't work (yet)!
    read a well-formed CSV file and convert it to properly-formed ubiome JSON
    :param fname: str the file you want to convert
    :return:
    """
    with open(fname) as ubiome_csv_file:
        reader = csv.DictReader(ubiome_csv_file)
        json_out=[]
        for row in reader:
            rowkeys = row.keys()
            rowvals = row.values()
            rownext = [rowkey for rowkey in rowkeys if rowkey in ['count', 'count_norm', 'parent', 'tax_name', 'tax_rank', 'tax_color', 'avg', 'taxon']]
            json_out = json_out+[rownext]

    return json_out





