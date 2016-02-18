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

# mysterious bug from stack overflow http://newbebweb.blogspot.fr/2012/02/python-head-ioerror-errno-32-broken.html
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

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
    title = generate_title(patents)
    description = generate_description(patents) # random.randint(10,25) for more paragraphs
    return {
        "title": title,
        "description": description[0]
    }


def get_cli_args_parser():
    # parse command line arguments
    p = OptionParser()
    p.add_option('-v', '--verbose', action="store_true", dest="verbose", help="don't print status messages to stdout", default=False)
    p.add_option('-t', '--title', action="store_true", dest="title", help="print the Junk object title to stout", default=False)
    p.add_option('-d', '--description', action="store_true", dest="description", help="print the Junk object description to stout", default=False)

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

    if options.description :
        print junk["description"]



if __name__ == "__main__":
    main()
