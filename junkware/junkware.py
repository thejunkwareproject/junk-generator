#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from optparse import OptionParser

import random

from corpus import PatentCorpus
from markov import TitleGenerator
from object import ObjectGenerator
from scad import get_template_scad
from nlp import NLP

import json

import logging
logger = logging.getLogger('junkware')

nb_patent = 10 # number of patents loaded
TMP_DIR = "/tmp"

# init patents db
corpus_path='data/Patents.sqlite3'
corpus_path_ok = os.path.join(os.getcwd(),corpus_path)
logger.info("Init Patent Corpus with %s"%corpus_path_ok)

# tmp text corpus
tmp_corpus_path = os.path.join(TMP_DIR, 'corpus_abstract')
logger.info("TMP abstract corpus: %s"%tmp_corpus_path)

# init templates
make_path = os.path.join(os.getcwd(),"make")
scad_file = os.path.join(make_path,"STLconverter.scad")

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

def create_scad_file(shape, scad_file_path):
    scad_shape = get_template_scad(shape)
    logger.info("Saved SCAD supershape in %s"%scad_file_path)

    # save file
    with open(scad_file_path, "w") as f:
        f.write(scad_shape)
    print "SCAD supershape saved %s"%scad_file_path

def create_STL_file(stl_file_path, scad_file_path):
    # create STL file
    cmd = "/usr/bin/openscad -o " + " " + stl_file_path + " " +scad_file_path
    logger.info("STL : Executing subprocess %s"%cmd)

    # no block, it start a sub process.
    p = subprocess.Popen(cmd , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # and you can block util the cmd execute finish
    p.wait()

    print "STL file saved at %s"%stl_file_path


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

    #
    p.add_option('-v', '--verbose', action="store_true", dest="verbose", help="don't print status messages to stdout", default=False)
    p.add_option('-t', '--title', action="store_true", dest="title", help="print the Junk object title to stout", default=False)
    p.add_option('-a', '--abstract', action="store_true", dest="abstract", help="print the Junk object abstract to stout", default=False)
    p.add_option('-d', '--description', action="store_true", dest="description", help="print the Junk object description to stout", default=False)
    p.add_option('-s', '--shape', action="store_true", dest="shape", help="print the Junk object shape to stout", default=False)

    # generate STL 3D model
    p.add_option('-p', '--printSTL', action="store_true", dest="printSTL", help="Generate STL 3D model", default=False)

    # export
    p.add_option("-o", "--output",
          action="store", # optional because action defaults to "store"
          dest="output_dir",
          default="junk",
          help="Name of the folder that will contains the object")

    return p

def main():

    # load parser
    parser = get_cli_args_parser()

    # get cli args
    (options, args) = parser.parse_args()

    try :
        dest_foldername = args[0]
    except IndexError:
        dest_foldername = None

    if options.verbose :
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG) # show logs

    dest_folder = os.path.join(os.getcwd(),options.output_dir)
    junk = generate_junk()

    # save the whole thing
    if not os.path.isdir(dest_folder):
        logger.info("Saving data in %s"%dest_folder)
        os.makedirs(dest_folder)
        with open(os.path.join(dest_folder,'%s.json'%options.output_dir), 'w') as outfile:
            json.dump(junk, outfile, sort_keys = True, indent = 4)

        print "Junk saved at %s"%dest_folder
    else :
        print "Can not write. Junk %s already exists at %s"%(options.output_dir, dest_folder)
        return

    # create 3D printing files
    if options.printSTL :
        # create SCAD file
        scad_file_path = os.path.join(dest_folder,"%s.scad"%options.output_dir)
        create_scad_file(junk["shape"], scad_file_path)

        # convert to STL
        stl_file_path = os.path.join(dest_folder,"%s.stl"%options.output_dir)
        create_STL_file(stl_file_path, scad_file_path)


    # display options
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
