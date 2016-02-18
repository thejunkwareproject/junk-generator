# Junk Generator

A Python script to generate random objects from a patent database.

Generate an object

    junkware # generate its definition
    junkware -p # generate the associated STL 3d model
    junkware -tads # t,a,d options allow to print title, abstract, description

Check the help with

    junkware -h

To generate the 3D models, you will need to install [OpenSCAD](http://www.openscad.org/)

    sudo apt-get install openscad


### Install

    git clone http://github.com/thejunkwareproject/junk-generator && cd junk-generator
    python setup.py

Download NLP corpora

    python -m textblob.download_corpora

Download the patent corpus in the ```/data``` folder by [clicking here]( https://raw.githubusercontent.com/thejunkwareproject/junkware/master/data/patents/Patents.sqlite3) or copy/pasting the following command in your terminal.

    wget -P data https://raw.githubusercontent.com/thejunkwareproject/junkware/master/data/patents/Patents.sqlite3


### Post on twitter

Using Twitter command-line util [t](https://github.com/sferik/t#features)

     junkware -t | xargs t update
