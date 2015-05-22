import networkx as nx
NetworkX_pickled_graph = nx.read_gpickle('C:\\Users\\raoulb\\Documents\\_DIT\\_THESIS\\senticnet\\resources\\senticnet-3.0\\senticnet3.pickle')

class HelperRdfLib:

    def __init__(self):
      self = self
           
    def getPolarity(self, concept):   
        
       sparql_query_result = NetworkX_pickled_graph.query(
        """
        prefix concept: <http://sentic.net/api/en/concept/>
        prefix api: <http://sentic.net/api>
        SELECT ?polarity
            WHERE {           
               concept:%s  api:polarity ?polarity
            }"""%concept)    
       
       #for r in qres2.result: #accessing result is DEPRECATED
       for r in sparql_query_result:
           #print r
           return float(r[0])