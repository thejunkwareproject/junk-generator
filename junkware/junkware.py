#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from optparse import OptionParser

import random
from corpus import PatentCorpus
from markov import TitleGenerator
from object import ObjectGenerator

from nlp import NLP

import logging
logger = logging.getLogger('junkware')

corpus_path='data/Patents.sqlite3'
nb_patent = 10 # number of patents loaded
TMP_DIR = "/tmp"

# init patents db
corpus_path_ok = os.path.join(os.getcwd(),corpus_path)
logger.info("Init Patent Corpus with %s"%corpus_path_ok)

# tmp text corpus
tmp_corpus_path = os.path.join(TMP_DIR, 'corpus_abstract')
logger.info("TMP abstract corpus: %s"%tmp_corpus_path)

if os.path.isfile(corpus_path_ok):
    patents=PatentCorpus(corpus_path_ok)
else :
    raise ValueError("No database file.")

def get_random_patents():
    logger.info("Getting %s patents."%nb_patent)
    return patents.get_records(nb_patent, random=True)

def generate_shape():
    shape = {}
    shape["m1"]  = random.randint(0,20)
    shape["n11"] = random.randint(0,50)
    shape["n12"] = random.randint(0,50)
    shape["n13"] = random.randint(0,50)
    shape["m2"]  = random.randint(0,20)
    shape["n21"] = random.randint(0,50)
    shape["n22"] = random.randint(0,50)
    shape["n23"] = random.randint(0,50)
    logger.info("Shape: %s"%shape)
    return shape

def generate_text(patents, paragraphs=1):

    abstract_generator = ObjectGenerator(tmp_corpus_path)

    # add patents to corpus
    for abstract in patents["abstracts"]:
        abs_nlp = NLP(abstract)
        clean_abstract=abs_nlp.filter_out_nastyness()
        abstract_generator.add_to_corpus(clean_abstract)

    description = []
    for i  in range(0,paragraphs):
        description.append(abstract_generator.generate_definition(1,random.randint(30,150)))

    logger.info("Generated %s paragraphs of text."%len(description))
    return description

def generate_description(patents):
    return generate_text(patents, random.randint(10,25))

def generate_abstract(patents):
    abstract = generate_text(patents, 1)[0]
    logger.info("Abstract: %s words."%len(abstract))
    return abstract


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
    title = generate_title(patents)
    abstract = generate_abstract(patents)
    description = generate_description(patents)
    shape = generate_shape()
    return {
        "title": title,
        "abstract" : abstract,
        "description": description,
        "shape" : shape
    }

def get_cli_args_parser():
    # parse command line arguments
    p = OptionParser()
    p.add_option('-v', '--verbose', action="store_true", dest="verbose", help="don't print status messages to stdout", default=False)
    p.add_option('-t', '--title', action="store_true", dest="title", help="print the Junk object title to stout", default=False)
    p.add_option('-a', '--abstract', action="store_true", dest="abstract", help="print the Junk object abstract to stout", default=False)
    p.add_option('-d', '--description', action="store_true", dest="description", help="print the Junk object description to stout", default=False)
    p.add_option('-s', '--shape', action="store_true", dest="shape", help="print the Junk object shape to stout", default=False)

    return p

def main():

    # load parser
    parser = get_cli_args_parser()

    # get cli args
    (options, args) = parser.parse_args()
    if options.verbose :
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG) # show logs

    junk = generate_junk()

    if options.title :
        print junk["title"]

    if options.abstract :
        print junk["abstract"]

    if options.description :
        print junk["description"]

    if options.shape :
        print junk["shape"]



if __name__ == "__main__":
    main()
