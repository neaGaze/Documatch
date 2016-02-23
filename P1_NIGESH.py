import os
import sys
import math
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer

class hawa:
    def __init__(self):
        self.weighted = False
        self.documents = []
        self.corpus_dict = {}

    def addDocument(self, doc_name, list_of_words):
        # building a dictionary
        doc_dict = {}
        for w in list_of_words:
            doc_dict[w] = doc_dict.get(w, 0.) + 1.0
            self.corpus_dict[w] = self.corpus_dict.get(w, 0.0) + 1.0

        # normalizing the dictionary
        length = float(len(list_of_words))
        for k in doc_dict:
            doc_dict[k] = doc_dict[k] / length

        # add the normalized document to the corpus
        self.documents.append([doc_name, doc_dict])
    
    def similarities(self, list_of_words):
        """Returns a list of all the [docname, similarity_score] pairs relative to a list of words."""

        # building the query dictionary
        query_dict = {}
        for w in list_of_words:
            query_dict[w] = query_dict.get(w, 0.0) + 1.0

        # normalizing the query
        length = float(len(list_of_words))
        for k in query_dict:
            query_dict[k] = query_dict[k] / length

        # computing the list of similarities
        sims = []
        for doc in self.documents:
            score = 0.0
            doc_dict = doc[1]
        
            for k in query_dict:
                if doc_dict.has_key(k):
                    score += ((query_dict[k] / self.corpus_dict[k]) + (doc_dict[k] / self.corpus_dict[k]))
            sims.append([doc[0], score])

        return sims

tokens_in_all_doc = {}
tfidf = {}
TOTAL_DOCUMENTS_SCANNED = 0

list_val = []

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
    return math.log10((float(TOTAL_DOCUMENTS_SCANNED) / float(total_docs)))

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

def calc_tf_idf():
    for key in tokens_in_all_doc:
        print "Running key ", key, "..."
        tfidf[key] = {}
        minimum, maximum = 5000, -5000
        for token in tokens_in_all_doc[key]:
            if token not in tfidf[key]:
                tfidf[key][token] = (1.0 + float(math.log10(float(tokens_in_all_doc[key].count(token))))) * getidf(token)

                if tfidf[key][token] < minimum:
                    minimum = tfidf[key][token]

                if tfidf[key][token] > maximum:
                    maximum = tfidf[key][token]

        for tmp_key in tfidf[key]:
            tfidf[key][tmp_key] = (tfidf[key][tmp_key] - minimum) / (maximum - minimum)

    return tfidf

def find_tf_idf_vector():
    tf_idf = {}
    list_val = []
    minimum, maximum = 5000, -5000
    for key in tokens_in_all_doc:
        for each in tokens_in_all_doc[key]:
            if each not in tf_idf:
                tf_idf[each] = compute_tf_idf(each)
                list_val.append(tf_idf[each])
                
                if tf_idf[each] < minimum:
                    minimum = tf_idf[each]

                if tf_idf[each] > maximum:
                    maximum = tf_idf[each]
        # tf_idf[] += [compute_tf_idf(each) for each in tokens_in_all_doc[key][0:10] if each not in tf_idf]

   # summ = reduce(lambda x, y: x + y, list_val) 
   # new_list = [((x - minimum) / (maximum - minimum)) for x in list_val]
    #print new_list

    for key in tf_idf:
        tf_idf[key] = (tf_idf[key] - minimum) / (maximum - minimum)

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


tbl = read_file_tokenize()
#temp_list = [compute_tf_idf(each) for each in tokens_in_all_doc['2012-10-22.txt'][0:25]]


