import os
import math
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer

tokens_in_all_doc = {}
TOTAL_DOCUMENTS_SCANNED = 0

# return the cosine similairty between a query string and a document
def querydocsim(qstring,filename):
    return False

# return the cosine similarity betwen two speeches (files)
def docdocsim(filename1,filename2):
    return False

# return the inverse document frequency of a token. If the token doesn't exist in the corpus, return 0
def getidf(token):
    total_docs = 0
    for key in tokens_in_all_doc:
        if token in tokens_in_all_doc[key]:
            total_docs += 1
    return math.log10((float(total_docs) / float(TOTAL_DOCUMENTS_SCANNED)))

# return the total number of occurrences of a token in all documents
def getcount(token):
    count = 0
    for each in tokens_in_all_doc:
        count += tokens_in_all_doc[each].count(token)
    return count

# return the document that has the highest similarity score with respect to 'qstring'
def query(qstring):
    return False

def cosine_similarity(v1,v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)

def compute_tf_idf(token):
    val = getcount(token) * getidf(token)
    return val

def find_tf_idf_vector():
    tf_idf = {}
    for key in tokens_in_all_doc:
        for each in tokens_in_all_doc[key][0:10]:
            if each not in tf_idf:
                tf_idf[each] = compute_tf_idf(each)
        # tf_idf[] += [compute_tf_idf(each) for each in tokens_in_all_doc[key] if each not in tf_idf]
    return tf_idf

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
    corpus_root = './presidential_debates'
    global TOTAL_DOCUMENTS_SCANNED
    for filename in os.listdir(corpus_root):
        file = open(os.path.join(corpus_root, filename), "r")
        doc = file.read()
        file.close() 
        doc = doc.lower()

        # now get the tokens
        tokens_in_all_doc[filename] = token_processor(doc)
        TOTAL_DOCUMENTS_SCANNED += 1
    return True

read_file_tokenize()
#temp_list = [compute_tf_idf(each) for each in tokens_in_all_doc['2012-10-22.txt'][0:25]]
