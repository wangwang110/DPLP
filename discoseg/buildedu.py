## buildedu.py
## Author: Yangfeng Ji
## Date: 05-03-2015
## Time-stamp: <yangfeng 09/25/2015 15:35:08>

from os import listdir
from os.path import join, basename
from discoseg.model.classifier import Classifier
from discoseg.model.docreader import DocReader
from discoseg.model.sample import SampleGenerator
from pickle import load
import gzip


def main(fmodel, fvocab, rpath, wpath):
    clf = Classifier()
    print("clf")
    vocab = load(gzip.open(fvocab))
    print("clf")
    dr = DocReader()
    clf.loadmodel(fmodel)
    print("clf")
    flist = [join(rpath, fname) for fname in listdir(rpath) if fname.endswith('conll')]

    for (fidx, fname) in enumerate(flist):
        print("Processing file: {}".format(fname))
        doc = dr.read(fname, withboundary=False)
        sg = SampleGenerator(vocab)
        sg.build(doc)
        M, _ = sg.getmat()
        predlabels = clf.predict(M)
        doc = postprocess(doc, predlabels)
        writedoc(doc, fname, wpath)


def postprocess(doc, predlabels):
    """ Assign predlabels into doc
    """
    tokendict = doc.tokendict
    for gidx in tokendict:
        if predlabels[gidx] == 1:
            tokendict[gidx].boundary = True
        else:
            tokendict[gidx].boundary = False
        if tokendict[gidx].send:
            tokendict[gidx].boundary = True
    return doc


# def writedoc(doc, fname, wpath):
#     """ Write doc into a file with the CoNLL-like format
#     """
#     tokendict = doc.tokendict
#     N = len(tokendict)
#     fname = basename(fname) + '.edu'
#     fname = join(wpath, fname)
#     eduidx = 0
#     with open(fname, 'w') as fout:
#         for gidx in range(N):
#             fout.write(str(eduidx) + '\n')
#             if tokendict[gidx].boundary:
#                 eduidx += 1
#             if tokendict[gidx].send:
#                 fout.write('\n')
#     print 'Write segmentation: {}'.format(fname)


def writedoc(doc, fname, wpath):
    """ Write file
    """
    tokendict = doc.tokendict
    N = len(tokendict)
    fname = basename(fname).replace(".conll", ".merge")
    fname = join(wpath, fname)
    eduidx = 1
    eduidx2text = {}
    with open(fname, 'w') as fout:
        for gidx in range(N):
            tok = tokendict[gidx]
            line = str(tok.sidx) + "\t" + str(tok.tidx) + "\t"
            line += tok.word + "\t" + tok.lemma + "\t"
            line += tok.pos + "\t" + tok.deplabel + "\t"
            line += str(tok.hidx) + "\t" + tok.ner + "\t"
            line += tok.partialparse + "\t" + str(eduidx) + "\n"
            fout.write(line)
            if eduidx not in eduidx2text:
                eduidx2text[eduidx] = tok.word + " "
            else:
                eduidx2text[eduidx] += tok.word + " "

            # Boundary
            if tok.boundary:
                eduidx += 1
            if tok.send:
                fout.write("\n")

    # print(eduidx2text)
    with open(fname + "_text", 'w') as ff:
        for item in eduidx2text.items():
            ff.write(str(item[0]) + "\t" + str(item[1]) + "\n")
