import nltk
import itertools
import sys
sys.path.append('C:\\Python27\\python_projects\\nodebox')
import en

from HelperNLP import HelperNLP
hnlp = HelperNLP()
from HelperRdfLib import HelperRdfLib
hrdf = HelperRdfLib()
from HelperNegation import HelperNegation
hn = HelperNegation()

f = open('C:\\Users\\raoulb\\Documents\\_DIT\\_THESIS\\EXPERIMENT\\raw\\threshold STDEV\\blablatest.xls','a')
#with open('C:\\Users\\raoulb\\Documents\\_DIT\\_THESIS\\DATASETS\\BASELINE\\baseline_test.csv') as doc:
with open('C:\\Users\\raoulb\\Documents\\_DIT\\_THESIS\\DATASETS\\ISEAR\\dataset_anger.csv') as doc:  

    doc_scores = []
    row_id = 0
    for row in doc:
        row_id += 1
        row = row.rstrip('\n')
        print 'row:', row
        row_sentences = row.split('.')
        print 'row_sentences:', row_sentences 
        sentence_id = 0
        for sentence in row_sentences:
            sentence_id += 1
            print 'sentence:', sentence, '\n'
            sentence_clauses_scores_sw = []
            sentence_clauses_scores_mw = []
            clauses = sentence.split(',')
            print '  clauses:', clauses
            clause_id = 0
            for i in range(len(clauses)):
                clause_id += 1    
                single_clause_scores_sw = []
                single_clause_scores_mw = []
                
                try:
                    neg_flag = hn.negControl(clauses[i])
                    clause = hnlp.removePunctuationSentence(clauses[i])
                    clause = clause.lower()
                    print '  row_id', row_id, 'sentence_id', sentence_id, 'clause_id', clause_id, ':', clause
                    terms = hnlp.removeStopwords(clause)
                    #print 'terms:', terms
                    concepts = []
                    for term in terms.split(' '):
                        #print term
                        term = hnlp.normalizeTense(term)
                        
                        term = hnlp.normalizePlural(term)
                        concepts.append(term)
                    print '  concepts', concepts
                    clause_scores = []
                    for term in concepts:                       
                        word_score = hrdf.getPolarity(term)
                        #if word_score <> None:
                        #if word_score <> None and (word_score < -0.289 or word_score > 0.289):
                        if word_score <> None and (word_score < -0.577 or word_score > 0.577):                        
                            print '  ', term, word_score
                            single_clause_scores_sw.append(word_score)
                    print '  single_clause_scores_sw', single_clause_scores_sw, '\n'
                    
                    if single_clause_scores_sw:        
                        perms = itertools.combinations(concepts, r = 2)
                        for perm in perms:
                            mw = perm[0] + '_' + perm[1]
                            #print '   mw:', mw
                            word_score = hrdf.getPolarity(mw)
                            #if word_score <> None:
                            #if word_score <> None and (word_score < -0.257 or word_score > 0.257):
                            if word_score <> None and (word_score < -0.514 or word_score > 0.514):
                                print '  ', mw, word_score
                                single_clause_scores_mw.append(word_score)
                    print '  multi_clause_scores_mw', single_clause_scores_mw, '\n'
                                      
                    if single_clause_scores_sw:       
                        try:
                            final_clause_score_sw = round(sum(single_clause_scores_sw)/len(single_clause_scores_sw),3)
                        except:
                            final_clause_score_sw = 0    
                        if neg_flag == 1:
                            print 'invert score\n'
                            final_clause_score_sw = -final_clause_score_sw
                    else:
                        continue
                    print '  final_clause_score_sw', final_clause_score_sw
                    sentence_clauses_scores_sw.append(final_clause_score_sw)
                    
                    if single_clause_scores_mw:       
                        try:
                            final_clause_score_mw = round(sum(single_clause_scores_mw)/len(single_clause_scores_mw),3)
                        except:
                            final_clause_score_mw = 0    
                        if neg_flag == 1:
                            print 'invert score'
                            final_clause_score_mw = -final_clause_score_mw
                    else:
                        continue
                    print '  final_clause_score_mw', final_clause_score_mw
                    sentence_clauses_scores_mw.append(final_clause_score_mw)
                                      
                except:
                    continue        
                
            print '\nsentence_clauses_scores_sw', sentence_clauses_scores_sw
            try:
                final_sentence_score_sw = round(sum(sentence_clauses_scores_sw)/len(sentence_clauses_scores_sw),3)
            except:
                final_sentence_score_sw = 0
            
            if not final_sentence_score_sw:
                final_sentence_score_sw = 0
            print 'sentence_id', sentence_id, '- final_sentence_score_sw: ', final_sentence_score_sw
          
            
            print '\nsentence_clauses_scores_mw', sentence_clauses_scores_mw
            try:
                final_sentence_score_mw = round(sum(sentence_clauses_scores_mw)/len(sentence_clauses_scores_mw),3)
            except:
                final_sentence_score_mw = 0
            
            if not final_sentence_score_mw:
                final_sentence_score_mw = 0
            print 'sentence_id', sentence_id, '- final_sentence_score_mw', final_sentence_score_mw           
        
            if final_sentence_score_sw <> 0 and final_sentence_score_mw <> 0:
                print >> f, 'STDEV2', 'nrg', 'movie', row_id, sentence_id, final_sentence_score_sw, final_sentence_score_mw
                
    f.flush()
    f.close()