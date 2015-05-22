import csv
import string
import nltk
from nltk.corpus import stopwords

stops = set(stopwords.words('english'))
for w in stops:
    print w