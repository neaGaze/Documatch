import os
import math
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer

raw_data = []
tokenized_data = []
stemmed_data = []
count_datafiles = 0
tokens_in_all_doc = {}

# return the cosine similairty between a query string and a document
def querydocsim(qstring,filename):
    return False

# return the cosine similarity betwen two speeches (files)
def docdocsim(filename1,filename2):
    return False

# return the inverse document frequency of a token. If the token doesn't exist in the corpus, return 0
def getidf(token):
    return 0 

# return the total number of occurrences of a token in all documents
def getcount(token):
    count = 0
    for each in tokens_in_all_doc:
        count += each.count(token)
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

def token_processor(doc):
    onlyApha = re.sub(r'[^a-zA-Z]+', " ", row)
    tokens = onlyApha.split()

    common_words = stopwords.words('english')
    tokens = [each for each in tokens if each not in common_words]

    stemmer = PorterStemmer()
    tokens = [stemmer.stem(each) for each in tokens]
    
    print tokens
    return tokens

def read_file_tokenize():
    corpus_root = './presidential_debates'
    for filename in os.listdir(corpus_root):
        file = open(os.path.join(corpus_root, filename), "r")
        doc = file.read()
        file.close() 
        doc = doc.lower()

        # now get the tokens
        tokens_in_all_doc[filename] = token_processor(doc)
    return True

read_file_tokenize()
