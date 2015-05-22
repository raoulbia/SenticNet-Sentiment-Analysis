import sys
sys.path.append('C:\\Python27\\python_projects\\nodebox')
import en
import string
import nltk

import inflect # https://pypi.python.org/pypi/inflect
p = inflect.engine()

# Custom Stopword List
stopwords = """about,above,an,are,as,because,been,being,below,but,by,did,does,doing,during,had,
    has,having,he,her,hers,herself,him,himself,his,i,into,is,it,its,itself,me,more,my,myself,nor,or,
    our,ours,ourselves,s,she,should,such,than,their,theirs,them,themselves,these,they,those,was,were,
    which,who,whom,why,you,your,yours,yourselves"""

class HelperNLP:

    def __init__(doc):
      doc = doc
            
    def removePunctuationSentence(self, row):            
        row = str(row)
        row = row.translate(string.maketrans("",""), string.punctuation)
        return row
      
    def removeStopwords(self,row):
        row_tokenized = nltk.word_tokenize(str(row))
        filtered_word_list = [] #make a copy of the row
        for word in row_tokenized:
            if word not in stopwords: 
                filtered_word_list.append(word) 
        return ' '.join(filtered_word_list)
    
    def normalizeTense(self, word):
        word = word.lower()
        pos = en.sentence.tag(word)
        if pos[0][1] in ('VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'JJ'): #normalise also JJ annoying >> annoy
            try:
                word = en.verb.present(word)
                pos = en.sentence.tag(word)
            except:
                word = word    
        return word

    def normalizePlural(self, word):
        pos = en.sentence.tag(word)
        if pos[0][1] in ('NNS', 'NNPS'):        
            word_sing = p.singular_noun(word)
            if word_sing != False:
                word = word_sing
            else:
                word = word
        return word

