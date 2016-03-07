# Documatch
A python driven program to analyze the relevance of text documents to the given dataset of documents using TF-IDF vector 

Dataset

We use a corpus of all the general election presidential debates from 1960 to 2012. We processed the corpus and provided you a .zip file, which includes 30 .txt files. Each of the 30 files contains the transcript of a debate and is named by the date of the debate. 

Programming Language

-> Python 3.5.1
-> NLTK library (http://www.nltk.org/index.html)

Test Cases

query(qstring): return the document that has the highest similarity score with respect to 'qstring'.
getcount(token): return the total number of occurrences of a token in all documents.
getidf(token): return the inverse document frequency of a token. If the token doesn't exist in the corpus, return 0.
docdocsim(filename1,filename2): return the cosine similarity betwen two speeches (files).
querydocsim(qstring,filename): return the cosine similairty between a query string and a document.
