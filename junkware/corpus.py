# -*- coding: utf-8 -*-

import os
from random import choice, randint
import sqlite3
import codecs
import pickle

# some characters to avoid
stopwords = ["(", ")", "/"]


class PatentCorpus(object):

    """ Patent corpus """

    def __init__(self, patent_db):
        conn_patents = sqlite3.connect(patent_db)
        self.patents = conn_patents.cursor()

    def get_column_names(self):
        ''' Rows should be : Patent, Title, Abstract '''
        cols=[]
        for c in self.patents.execute("PRAGMA table_info('Patents');"): cols.append(c[1])
        return cols

    def get_records(self, _count, random=False):

        """
            Get a number of patents
            return :
            patents in full text
        """

        abtracts=[]
        titles=[]

        max_id = [max[0] for max in self.patents.execute("SELECT MAX(Id) FROM Patents;")][0]
        order = " ORDER BY id ASC "

        if (random == True):
            ids = ""
            rands = [randint(1, max_id) for x in range(0, _count)]
            for i, _id in enumerate(rands):
                ids += "" + str(_id) + ""
                if i != _count - 1:
                    ids += ","

            order = " AND id IN (" + ids + ")"

        query = "SELECT * FROM Patents WHERE (Description!='')" + \
            order + " LIMIT " + str(_count)
        # print query

        for row in self.patents.execute(query):
            # print row[3]
            # remove numbers and some unwantable characters
            text = ''.join(
                [i for i in row[2] if not i.isdigit() and i not in stopwords])

            abtracts.append(str(text))
            titles.append(str(row[3]))

        return {
            "ids" : ids,
            "abstracts" : abtracts,
            "titles" : titles
        }

    def get_records_by_ids(self, _ids):

        abtracts=[]
        titles=[]

        my_ids=str(_ids).split(",")

        ids = ""
        for i, _id in enumerate(my_ids):
            ids += "" + str(_id) + ""
            if i != len(my_ids) - 1:
                ids += ","

        order = " AND id IN (" + ids + ")"

        query = "SELECT * FROM Patents WHERE (Description!='')" + \
            order + " LIMIT " + str(len(my_ids))

        for row in self.patents.execute(query):
            text = ''.join(
                [i for i in row[2] if not i.isdigit() and i not in stopwords])

            abtracts.append(str(text))
            titles.append(str(row[3]))


        return {
            "ids" : _ids,
            "abstracts" : abtracts,
            "titles" : titles
        }
