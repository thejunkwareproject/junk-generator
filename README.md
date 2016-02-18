# Junk Generator

A Python script to generate random objects from a patent database.

Generate title

    junkware -t

Generate description

    junkware -d

Generate fictional objects

    junkware --STL # get a STL file


### Install

    git clone http://thejunkwareproject/junk-generator && cd junk-generator
    python setup.py develop

Download NLP corpora

    python -m textblob.download_corpora

Download the patent corpus in the ```/data``` folder by [clicking here]( https://raw.githubusercontent.com/thejunkwareproject/junkware/master/data/patents/Patents.sqlite3) or copy/pasting the following command in your terminal.

    wget -P data https://raw.githubusercontent.com/thejunkwareproject/junkware/master/data/patents/Patents.sqlite3


### Post on twitter

Using Twitter command-line util [t](https://github.com/sferik/t#features)

     junkware -t | xargs t update
