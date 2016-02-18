#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
from textblob import TextBlob
from nltk.corpus import stopwords
import re
from time import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')

stopwords = stopwords.words('english')
lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()


# Taken from Su Nam Kim Paper...
grammar = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns

    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
"""
chunker = nltk.RegexpParser(grammar)


class NLP(object):

    '''
    NLP tools
    required :
    corpus_path

    '''

    def __init__(self, _text, *args, **kwargs):
        # print "init NLP"

        # try:
        #     _text.decode("utf-8")
        # except UnicodeDecodeError :
        #     print "ok"
        #     pass


        self.text = _text
        self.blob = TextBlob(_text)
        self.sentences = self.blob.sentences

    def words(self):
        return self.blob.words

    def count_words(self):
        return dict(self.blob.word_counts)

    def get_language(self):
        return self.blob.detect_language()

    def keywords(self):

        t0 = time()

        # Used when tokenizing words
        sentence_re = r'''(?x)      # set flag to allow verbose regexps
              ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
            | \w+(-\w+)*            # words with optional internal hyphens
            | \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
            | \.\.\.                # ellipsis
            | [][.,;"'?():-_`]      # these are separate tokens
        '''

        toks = nltk.regexp_tokenize(self.text, sentence_re)

        postoks = nltk.tag.pos_tag(toks)
        # postoks = self.blob.pos_tags

        tree = chunker.parse(postoks)
        # print tree

        def leaves(tree):
            """Finds NP (nounphrase) leaf nodes of a chunk tree."""
            for subtree in tree.subtrees(filter=lambda t: t.node == 'NP'):
                yield subtree.leaves()

        def normalise(word):
            """Normalises words to lowercase and stems and lemmatizes it."""
            word = word.lower()
            word = stemmer.stem_word(word)
            word = lemmatizer.lemmatize(word)
            return word

        def acceptable_word(word):
            """Checks conditions for acceptable word: length, stopword."""
            accepted = bool(2 <= len(word) <= 40
                            and word.lower() not in stopwords)
            return accepted

        def get_terms(tree):
            for leaf in leaves(tree):
                # print leaf
                term = [normalise(w) for w, t in leaf if acceptable_word(w)]
                yield term

        terms = get_terms(tree)

        words = []
        for term in terms:
            for word in term:
                words.append(word)

        print "Done in %fs" % (time() - t0)
        return words

    def analyze_sentiment(self):
        sentiments = []
        for sentence in self.sentences:
            sentiments.append({
                "polarity": sentence.sentiment.polarity,
                "subjectivity": sentence.sentiment.subjectivity
            })
        return sentiments

    def get_adjectives(self):
        adj = []
        for word, POStag in sorted(set(self.blob.tags)):
            if POStag == "JJ":
                adj.append(str(word))
        return adj

    # https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html

    def start_with_number(self, s):
        data = [c for c in s if c in '0123456789Xx']
        if len(data) != 0:
            return True
        else:
            return False

    def filter_out_nastyness(self):
        '''Filter out proper nouns (NNP & NNPS), numbers (CD) and symbols (SYM)'''

        to_filter_out = ["ed.", '"']

        # for word, tag in self.blob.tags:
        #     if tag == "NNP"         \
        #         or tag == "NNPS"        \
        #         or tag == "CD"           \
        #         or tag == "SYM"         \
        #         or word[0:4] == "doi:" or word[0:4] == "isbn" or word[0:4] == "ISBN" \
        #             or self.start_with_number(word) == True  \
        #             or any(x.isupper() for x in word[2:]) == True \
        #             or tag == "FW":
        #         to_filter_out.append(word)
        # print to_filter_out
        regex = re.compile('\\b(%s)\\W'%('|'.join(map(re.escape,to_filter_out))),re.UNICODE)
        clean = regex.sub(" ", self.text)
        clean.decode("utf-8")
        clean_ok = ''.join([i for i in clean if i not in '()#'])
        clean_ok = clean_ok.replace("R.sub","")
        # clean_ok.decode("utf-8")
        return clean_ok

    def get_clean_text(self):
        txt=self.filter_out_nastyness()
        return txt

    def get_verbs(self):
        verbs = []
        for word, POStag in sorted(set(self.blob.tags)):
            if POStag == "VB":
                verbs.append(str(word))
        return verbs

    def get_nouns(self):
        nouns = []
        for word, POStag in sorted(set(self.blob.tags)):
            if POStag == "NN":
                nouns.append(str(word))
        return nouns

    def get_noun_phrases(self):
        nouns = []
        for word in self.blob.noun_phrases:
            nouns.append(str(word))
        return nouns

    def translate_to(self, _language):
        return self.blob.translate(to=_language)
