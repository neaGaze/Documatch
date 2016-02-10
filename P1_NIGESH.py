import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer

raw_data = []
tokenized_data = []
stemmed_data = []
count_datafiles = 0

# function to separate words from sentences
def word_separator(row):
    onlyApha = re.sub(r'[^a-zA-Z]+', " ", row)
    tokens = onlyApha.split()
    return tokens

# function to tokenize the words
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
    if count != 11 and count != 13 and count != 14 and count < 15:
        tokenized_data += word_separator(entry)
        count_datafiles += 1
    count += 1

# stemming process
stemmer = PorterStemmer()
for each in tokenized_data:
    if len(each) > 0:
        print each
        stemmed_data.append(stemmer.stem(each))

stepword = stopwords.words('english')
words_not_common = [each for each in stemmed_data if each not in stepword]



