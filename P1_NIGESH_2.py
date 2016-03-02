import ast
import os
import sys
import math
import re
import nltk
import time
from functools import reduce
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer

'''
######################################################################
    Name        Programming Assignment #1
    author      Nigesh Shakya
    Project     CSE 5331
######################################################################
'''

tokens_in_all_doc = {}
tfidf = {}
TOTAL_DOCUMENTS_SCANNED = 0
global_idf = {}

''' Return the normalized term frequency of the query '''
def get_query_tf(qstring):
    processed_token = token_processor(qstring.lower())
    tf_qstring = {}
    weighted_avg_mean = 0
    
    for token in processed_token:
        if token not in tf_qstring:
            count = processed_token.count(token)
            tf_qstring[token] = ((1.0 + float(math.log10(float(count)))) if count != 0 else 0)
            weighted_avg_mean += tf_qstring[token]**(2)

    tf_qstring.update((x, y / weighted_avg_mean**(1/2)) for x,y in tf_qstring.items())

    return tf_qstring

''' #### return the cosine similairty between a query string and a document #### '''
def querydocsim(qstring, filename):

    if filename not in tfidf:
        get_tf_idf(filename)

    doc = tfidf[filename]
    tf_qstring = get_query_tf(qstring)

    cosine_simil = 0

    for key in list(set(tf_qstring).intersection(set(doc))):
        cosine_simil += tf_qstring[key] * doc[key]

    return cosine_simil

''' return the cosine similarity betwen two speeches (files) #### '''
def docdocsim(filename1, filename2):

    if filename1 not in tfidf:
        get_tf_idf(filename1)

    if filename2 not in tfidf:
        get_tf_idf(filename2)

    doc1 = tfidf[filename1]
    doc2 = tfidf[filename2]
    cosine_sum = 0

    for key in list(set(doc1).intersection(set(doc2))):
        cosine_sum += doc1[key] * doc2[key]

    return cosine_sum

''' return the inverse document frequency of a token. If the token doesn't exist in the corpus, return 0 ### '''
def getidf(token):
    global global_idf 
    if token in global_idf:
        return global_idf[token]
    
    total_docs = 0
    for key in tokens_in_all_doc:
        if token in tokens_in_all_doc[key]:
            total_docs += 1
    global_idf[token] = math.log10((float(TOTAL_DOCUMENTS_SCANNED) / float(total_docs))) 

    return global_idf[token]

'''  return the total number of occurrences of a token in all documents #### '''
def getcount(token):
    count = 0
    stemmer = PorterStemmer()
    for each in tokens_in_all_doc:
        count += tokens_in_all_doc[each].count(stemmer.stem(token))
    return count

''' return the document that has the highest similarity score with respect to 'qstring' #### '''
def query(qstring):
    s_time = time.time() 
    find_all_tf_idf()
    tf_qstring = get_query_tf(qstring)
    greatest_val = 0.0
    matching_doc = ''
    for key in tfidf:
        sim = querydocsim(qstring, key) 
        if sim > greatest_val:
            greatest_val = sim 
            matching_doc = key
    print("\n TOTAL QUERY TIME: ", (time.time() - s_time), " secs")
    return matching_doc

''' find the tf-idf of single document '''
def get_tf_idf(doc):
    print("Running ", doc, "...")
    start_time = time.time() 
    if doc in tfidf:
        return tfidf[doc] 
    else:
        tfidf[doc] = {}

    weighted_avg_mean = 0

    for token in tokens_in_all_doc[doc]:
        if token not in tfidf[doc]:
            count = tokens_in_all_doc[doc].count(token)
            tfidf[doc][token] = ((1.0 + float(math.log10(float(count)))) if count != 0 else 0) * getidf(token)
            weighted_avg_mean += (tfidf[doc][token]**(2))

    tfidf[doc].update((x, y / weighted_avg_mean**(1/2)) for x,y in tfidf[doc].items())

    end_time = time.time()
    print("time taken: ", (end_time - start_time), " secs")
    return tfidf[doc]

''' find the tfidf vector of all the documents '''
def find_all_tf_idf():
    for doc in tokens_in_all_doc:
        get_tf_idf(doc)

    return tfidf

''' split the tokens, remove common words and stem the words '''
def token_processor(doc):
    onlyApha = re.sub(r'[^a-zA-Z]+', " ", doc)
    tokens = onlyApha.split()

    common_words = stopwords.words('english')
    tokens = [each for each in tokens if each not in common_words]

    stemmer = PorterStemmer()
    tokens = [stemmer.stem(each) for each in tokens]
    
    return tokens

''' Read the all the files inside the Presidential Debates directory '''
def read_file_tokenize():
    corpus_root = './presidential_debates' 
    global TOTAL_DOCUMENTS_SCANNED

    start_time = time.time()
    for filename in os.listdir(corpus_root):
        file = open(os.path.join(corpus_root, filename), "r")
        doc = file.read()
        file.close()
        doc = doc.lower()

        # now get the tokens
        tokens_in_all_doc[filename] = token_processor(doc)
        TOTAL_DOCUMENTS_SCANNED += 1
    
    end_time = time.time()
    print("Time taken: ", (end_time - start_time), " secs")
    return True

''' write the data to the disk '''
def write_output_file(var):
    file_name = input('Enter the file name to save as:')
    with open(os.path.join('./gen', file_name),'w') as data:
        data.write('{0}'.format(var))

''' Read saved data from disk '''
def read_saved_data(filename):
    str_data = ''
    with open(os.path.join('./gen', filename)) as da:
        str_data += da.read()

    tfidf = ast.literal_eval(str_data)
    return tfidf


tbl = read_file_tokenize()

