# coding: utf-8

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from nltk import Tree
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget
import matplotlib

matplotlib.use('Agg')


def drawrst(strtree, fname):
    """ Draw RST tree into a file
    """
    if not fname.endswith(".ps"):
        fname += ".ps"
    t = Tree.fromstring(strtree)
    cf = CanvasFrame()
    tc = TreeWidget(cf.canvas(), t)
    cf.add_widget(tc, 10, 10)  # (10,10) offsets
    cf.print_to_file(fname)
    cf.destroy()


with open("./data/pic_result.txt", "r") as f:
    i = 0
    for line in f.read().split("\n"):
        if line.strip() != "":
            print(line)
            i += 1
            fname = "./pic_result_" + str(i) + ".ps"
            drawrst(line, fname)

# 图片结果对比着相应的*.merge_text(原始文本)看
