#!/usr/bin/env bash
#
# Runs Stanford CoreNLP.
# Simple uses for xml and plain text output to files are:
#    ./corenlp.sh -file filename
#    ./corenlp.sh -file filename -outputFormat text 

scriptdir=/data_local/DPLP-master/stanford-corenlp-4.2.2/

# echo java -mx3g -cp \"$scriptdir/*\" edu.stanford.nlp.pipeline.StanfordCoreNLP $*

# $1 - path
PATH=$1
for FNAME in $PATH/*
do
     echo $FNAME.xml
     echo $(/usr/bin/basename $FNAME.xml)
     echo $scriptdir
    /home/Java/jdk1.8.0/bin/java  -mx2g -cp "$scriptdir/*" edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse -ssplit.eolonly \
    -tokenize.whitespace true -file $FNAME -outputFormat xml
    /bin/mv $(/usr/bin/basename $FNAME.xml) $PATH/
done
