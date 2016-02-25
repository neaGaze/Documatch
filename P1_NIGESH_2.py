import ast
import os
import sys
import math
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer

tokens_in_all_doc = {}
tfidf = {}
#corpus_token_repo = []
TOTAL_DOCUMENTS_SCANNED = 0

list_val = []

# return the cosine similairty between a query string and a document
def querydocsim(tfidf, qstring,filename):
    processed_token = token_processor(qstring.lower())
    doc = tfidf[filename]
    tf_qstring = {}
    weighted_avg_mean = 0
    
    for token in processed_token:
        if token not in tf_qstring:
            count = processed_token.count(token)
            tf_qstring[token] = ((1.0 + float(math.log10(float(count)))) if count != 0 else 0)
            weighted_avg_mean += tf_qstring[token]**(2)

    cosine_simil = 0
    
    for tmp_key in tf_qstring:
        tf_qstring[tmp_key] = ((tf_qstring[tmp_key])) / weighted_avg_mean**(1/2)
        for tmp_key2 in doc:
            if tmp_key == tmp_key2:
                cosine_simil += tf_qstring[tmp_key] * doc[tmp_key2]

    return cosine_simil

# return the cosine similarity betwen two speeches (files)
def docdocsim(tfidf, filename1,filename2):
    doc1 = tfidf[filename1]
    doc2 = tfidf[filename2]
    cosine_sum = 0

    for key in doc1:
        for each in doc2:
            if key == each:
                cosine_sum += doc1[key] * doc2[each]

    return cosine_sum

# return the inverse document frequency of a token. If the token doesn't exist in the corpus, return 0
def getidf(token):
    total_docs = 0
    for key in tokens_in_all_doc:
        if token in tokens_in_all_doc[key]:
            total_docs += 1
    return math.log10((float(TOTAL_DOCUMENTS_SCANNED) / float(total_docs)))

# return the total number of occurrences of a token in all documents
def getcount(token):
    count = 0
    for each in tokens_in_all_doc:
        count += tokens_in_all_doc[each].count(token)
    return count

# return the document that has the highest similarity score with respect to 'qstring'
def query(qstring):
    processed_token = token_processor(qstring.lower())
    return False

def calc_tf_idf(corpus_token_repo):
    for doc in tokens_in_all_doc:
        print("Running doc ", doc, "...")
        tfidf[doc] = {}
        weighted_avg_mean = 0

        for token in tokens_in_all_doc[doc]:
            if token not in tfidf[doc]:
                count = tokens_in_all_doc[doc].count(token)
                tfidf[doc][token] = ((1.0 + float(math.log10(float(count)))) if count != 0 else 0) * getidf(token)
                weighted_avg_mean += (tfidf[doc][token] * tfidf[doc][token])

        for tmp_key in tfidf[doc]:
            tfidf[doc][tmp_key] = ((tfidf[doc][tmp_key])) / weighted_avg_mean**(1/2)

    return tfidf


def token_processor(doc):
    onlyApha = re.sub(r'[^a-zA-Z]+', " ", doc)
    tokens = onlyApha.split()

    common_words = stopwords.words('english')
    tokens = [each for each in tokens if each not in common_words]

    stemmer = PorterStemmer()
    tokens = [stemmer.stem(each) for each in tokens]
    
    #print tokens
    return tokens

def read_file_tokenize():
    corpus_root = './presidential_debates' # './test_cases' 
    global TOTAL_DOCUMENTS_SCANNED
    corpus_token_repo = []

    for filename in os.listdir(corpus_root):
        file = open(os.path.join(corpus_root, filename), "r")
        doc = file.read()
        file.close() 
        doc = doc.lower()

        # now get the tokens
        tokens_in_all_doc[filename] = token_processor(doc)
        TOTAL_DOCUMENTS_SCANNED += 1
        
        # get all the corpus of tokens
        # corpus_token_repo += [each for each in tokens_in_all_doc[filename] if each not in corpus_token_repo] 

    return corpus_token_repo

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
#temp_list = [compute_tf_idf(each) for each in tokens_in_all_doc['2012-10-22.txt'][0:25]]

