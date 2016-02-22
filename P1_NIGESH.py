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

# return the cosine similairty between a query string and a document
def querydocsim(qstring,filename):
    return False

# return the cosine similarity betwen two speeches (files)
def docdocsim(filename1,filename2):
    return False

# return the inverse document frequency of a token. If the token doesn't exist in the corpus, return 0
def getidf(token):
    if token not in words_not_common[token]:
        return 0
    else:
        return 1

# return the total number of occurrences of a token in all documents
def getcount(token):
    return False

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

def calculate_tdidf(vec):
    tfidf_vec = {}
    return tfidf_vec

# function to separate words from sentences
def word_separator(row):
    onlyApha = re.sub(r'[^a-zA-Z]+', " ", row)
    tokens = onlyApha.split()
    return tokens

# NOT USED. function to tokenize the words
def tokenize(row):
    sentences = []
    tokenizer_plan = nltk.data.load('tokenizers/punkt/english.pickle')
    sentencesTokenize = tokenizer_plan.tokenize(row.decode('utf8').strip())

    for x in sentencesTokenize:
        if len(sentencesTokenize) > 0:
            sentences.append(word_separator(x))
                
    return sentences

# read files 
corpus_root = './presidential_debates'
for filename in os.listdir(corpus_root):
    file = open(os.path.join(corpus_root, filename), "r")
    doc = file.read()
    file.close() 
    doc = doc.lower()
    raw_data.append(doc)

count = 0
for entry in raw_data:
   # tokenizer = RegexpTokenizer(r'[^a-zA-Z]')
    if count <= 10: #count != 11 and count != 13 and count != 14 and count < 15:
        print "searching document #",count+1," ......."
        tokenized_data.append(word_separator(entry))
        count_datafiles += 1
    count += 1

# stemming process
stemmer = PorterStemmer()
for innerList in tokenized_data:
    tmp_list = []
    for each in innerList:
        if len(each) > 0:
            # print each
            tmp_list.append(stemmer.stem(each))
    stemmed_data.append(tmp_list)

# removing the stopwords
stepword = stopwords.words('english')
words_not_common = []
tfidf_vec_list = []
for a in stemmed_data:
    words_not_common.append([each for each in a if each not in stepword])
    print words_not_common
    #tfidf_vec_list.append(calculate_tdidf(words_not_common[a]))  

# calculate the tdidf vector
idf = {}
tf_list = []
for list_terms in words_not_common:
    tf = {} 
    for term in list_terms:
        flag = True

        if term in tf:
            tf[term] += 1
        else:
            tf[term] = 1

 #   for term in list_terms:
        if term in idf and flag:
            idf[term] += 1
            #break
            flag = False
        else:
            idf[term] = 1

    tf_list.append(tf)

cnt = 0
for list_terms in words_not_common:
    tfidf = {}
    for term in list_terms:
        first_part = 1 + math.log10(tf_list[cnt][term])
        second_part = math.log10(float(len(words_not_common)) / float(idf[term]))
        tfidf[term] = first_part * second_part
    tfidf_vec_list.append(tfidf)
    cnt += 1



