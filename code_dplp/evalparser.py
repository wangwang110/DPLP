## evalparser.py
## Author: Yangfeng Ji
## Date: 11-05-2014
## Time-stamp: <yangfeng 09/25/2015 16:32:42>

from code_dplp.model import ParsingModel
from code_dplp.tree import RSTTree
from code_dplp.docreader import DocReader
from code_dplp.evaluation import Metrics
from os import listdir
from os.path import join as joinpath
from code_dplp.util import drawrst
from nltk import Tree
import pickle


def parse(pm, doc):
    """ Parse one document using the given parsing model

    :type pm: ParsingModel
    :param pm: an well-trained parsing model

    :type fedus: string
    :param fedus: file name of an document (with segmented EDUs) 
    """
    pred_rst = pm.sr_parse(doc)
    return pred_rst


def writebrackets(fname, brackets):
    """ Write the bracketing results into file
    """
    print('Writing parsing results into file: {}'.format(fname))
    with open(fname, 'w') as fout:
        for item in brackets:
            fout.write(str(item) + '\n')


def evalparser(path='./examples', report=False,
               bcvocab=None, draw=True,
               withdp=False, fdpvocab=None, fprojmat=None):
    """ Test the parsing performance

    :type path: string
    :param path: path to the evaluation data

    :type report: boolean
    :param report: whether to report (calculate) the f1 score
    """
    # ----------------------------------------
    # Load the parsing model
    print('Load parsing model ...')
    pm = ParsingModel(withdp=withdp, fdpvocab=fdpvocab, fprojmat=fprojmat)
    pm.loadmodel("model/parsing-model.pickle.gz")
    # ----------------------------------------
    # Evaluation
    met = Metrics(levels=['span', 'nuclearity', 'relation'])
    # ----------------------------------------
    # Read all files from the given path
    doclist = [joinpath(path, fname) for fname in listdir(path) if fname.endswith('.merge')]
    doc_li = []
    fname_out = "./data/pic_result.txt"
    print('Writing all parsing Tree result into file: {}'.format(fname_out))
    with open(fname_out, "w") as ff:
        sort_doclist = sorted(doclist, key=lambda s: int(s.split(".")[1][-1]), reverse=False)
        for fmerge in sort_doclist:
            print(fmerge)
            # ----------------------------------------
            # Read *.merge file
            dr = DocReader()
            doc = dr.read(fmerge)
            # ----------------------------------------
            # Parsing
            pred_rst = pm.sr_parse(doc, bcvocab)
            ff.write(pred_rst.parse() + "\n\n")

            doc_li.append(Tree.fromstring(pred_rst.parse()))
            if draw:
                strtree = pred_rst.parse()
                # print(type(strtree))
                drawrst(strtree, fmerge.replace(".merge", ".ps"))
                print("==========")
            # Get brackets from parsing results
            pred_brackets = pred_rst.bracketing()
            fbrackets = fmerge.replace('.merge', '.brackets')
            # Write brackets into file
            writebrackets(fbrackets, pred_brackets)
            # ----------------------------------------
            # Evaluate with gold RST tree
            if report:
                fdis = fmerge.replace('.merge', '.dis')
                gold_rst = RSTTree(fdis, fmerge)
                gold_rst.build()
                gold_brackets = gold_rst.bracketing()
                met.eval(gold_rst, pred_rst)
    if report:
        met.report()

    # pickle.dumps(doc_li, open("pic_rst_tree.bin", "wb"))
