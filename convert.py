# Copyright 2018 CVTE . All Rights Reserved.
# coding: utf-8

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from os import listdir
from os.path import join
from preprocess.xmlreader import reader, writer, combine


def extract(fxml):
    sentlist, constlist = reader(fxml)
    sentlist = combine(sentlist, constlist)
    fconll = fxml.replace(".xml", ".conll")
    writer(sentlist, fconll)


def main(rpath):
    files = [join(rpath, fname) for fname in listdir(rpath) if fname.endswith(".xml")]
    print(files)
    for fxml in files:
        print('Processing file: {}'.format(fxml))
        extract(fxml)


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2:
        main(rpath=sys.argv[1])
    else:
        print("python convert.py data_path")
