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
def querydocsim(qstring,filename):
    return False

# return the cosine similarity betwen two speeches (files)
def docdocsim(filename1,filename2):
    doc1 = tfidf[filename1]
    doc2 = tfidf[filename2]
    cosine_sim = []

    for key in doc1:
        cosine_sim += [doc2[each]*doc1[key] for each in doc2 if key in doc2]

    cosine_sum = sum(cosine_sim)
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

def cosine_similarity(v1,v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)

def calc_tf_idf(corpus_token_repo):
    for doc in tokens_in_all_doc:
        print("Running doc ", doc, "...")
        tfidf[doc] = {}
        weighted_avg_mean = 0

        for token in tokens_in_all_doc[doc]:
            if token not in tfidf[doc]:
                count = tokens_in_all_doc[doc].count(token)
                tfidf[doc][token] = (1.0 + float(math.log10(float(count)))) if count != 0 else 0
                weighted_avg_mean += (tfidf[doc][token] * tfidf[doc][token])

        for tmp_key in tfidf[doc]:
            tfidf[doc][tmp_key] = ((tfidf[doc][tmp_key]) * getidf(token)) / weighted_avg_mean**(1/2)

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
    corpus_root = './test_cases' # './presidential_debates'
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
        corpus_token_repo += [each for each in tokens_in_all_doc[filename] if each not in corpus_token_repo] 

    return corpus_token_repo

''' write the data to the disk '''
def write_output_file(var):
    file_name = input('Enter the file name to save as:')
    with open(os.path.join('./gen', file_name),'w') as data:
        data.write('{0}'.format(var))

''' Read saved data from disk '''
def read_saved_data(filename):
    str_data = ''
    with open(filename) as da:
        str_data += da.read()

    return ast.literal_eval(str_data)

tbl = read_file_tokenize()
#temp_list = [compute_tf_idf(each) for each in tokens_in_all_doc['2012-10-22.txt'][0:25]]

