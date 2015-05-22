# http://nbviewer.ipython.org/gist/slarson/6818123
# http://docs.openlinksw.com/virtuoso/rdfsparql.html
#import rdflib
import sys
sys.path.append('C:\\Python27\\python_projects\\nodebox')

import rdflib.graph as g
import networkx as nx
import time, en
start_time = time.clock()

import nltk
from nltk import *
from nltk.tag import stanford
from nltk.tag.stanford import POSTagger
st = POSTagger('C:\\Python27\\stanford-postagger\\models\\english-bidirectional-distsim.tagger',
                    'C:\\Python27\\stanford-postagger\\stanford-postagger.jar')


def getPolarity(concept):   
   #print concept
   pola = G.query( 
    """
    prefix concept: <http://sentic.net/api/en/concept/>
    prefix api: <http://sentic.net/api>
    SELECT ?polarity
        WHERE {           
           concept:%s  api:polarity ?polarity
        }"""%concept)    
   #return pola # pola = SPARQLResult object
   for r in pola:
       return str(r[0])
   
   
G = nx.read_gpickle('C:\\Users\\raoulb\\Documents\\_DIT\\_THESIS\\senticnet\\resources\\senticnet-3.0\\senticnet3.pickle')

f = open('C:\\Users\\raoulb\\Documents\\_DIT\\_THESIS\\EXPERIMENT\\SenticNet Analysis\\20150215_SenticNet_3_taggedConcepts_stanford.xls','a')


id = 0 #max id is 13742
nodes = []
for node in G:
    concept = node[0].split('concept/')[1]
    concept = concept.replace('\'','')
    if concept in nodes:
        print 'found\n'
        continue
    else:
        id += 1 
        nodes.append(concept)
        #print id, concept, '\n'
        
        pos = st.tag(concept.split('_'))
        #print concept, pos
        
        tok = []
        for i in pos:
            tok.append(i[1])
        pos = '_'.join(tok)
        pola = getPolarity(concept)
        print concept, pos, pola
        
        print >> f, concept,  pos, pola
        
f.flush()
f.close()
   
print time.clock() - start_time, "seconds"


