#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse

import random
from corpus import PatentCorpus
from markov import TitleGenerator
from object import ObjectGenerator

from nlp import NLP

import logging
logger = logging.getLogger('junkware')
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG) # show logs

corpus_path='data/Patents.sqlite3'
nb_patent = 10 # number of patents loaded
TMP_DIR = "/tmp"

# init patents db
corpus_path_ok = os.path.join(os.getcwd(),corpus_path)
logger.info("Init Patent Corpus with %s"%corpus_path_ok)

if os.path.isfile(corpus_path_ok):
    patents=PatentCorpus(corpus_path_ok)
else :
    raise ValueError("No database file.")

def get_random_patents():
    logger.info("Getting %s patents."%nb_patent)
    return patents.get_records(nb_patent, random=True)

def generate_description(patents, paragraphs=1):

    # abstract
    abstract_corpus_path = os.path.join(TMP_DIR, 'corpus_abstract')
    logger.info("TMP abstract corpus: %s"%abstract_corpus_path)
    abstract_generator = ObjectGenerator(abstract_corpus_path)

    # add patents to corpus
    for abstract in patents["abstracts"]:
        abs_nlp = NLP(abstract)
        clean_abstract=abs_nlp.filter_out_nastyness()
        abstract_generator.add_to_corpus(clean_abstract)

    description = []
    for i  in range(0,paragraphs):
        description.append(abstract_generator.generate_definition(1,random.randint(30,150)))

    logger.info("Description: %s"%description)
    return description

def generate_title(patents):
    # title
    titles=""
    for t in patents["titles"]:
        titles += " "+t

    title= TitleGenerator(titles).generate_text(size=random.randint(4,7)).title()
    logger.info("Title: %s"%title)
    return title

def generate_junk():
    patents = get_random_patents()
    generate_title(patents)
    generate_description(patents) # random.randint(10,25) for more paragraphs

def parse_args():
    # parse command line arguments
    p = argparse.ArgumentParser()

def main():

    # load parser
    parser = parse_args()

    # get cli args
    # args = parser.parse_args(sys.argv[1:])

    generate_junk()



if __name__ == "__main__":
    main()
