negation = ("ain't","aren't","can't","couldn't","didn't","doesn't","don't","hasn't","isn't","mightn't",
            "mustn't","neither","never" ,"no" ,"nobody","nor","not","shan't" ,"shouldn't","wasn't","weren't",
            "won't","wouldn't")
        
class HelperNegation:
    
    def __init__(self):
       self = self
    
    def negControl(self, sent):
        
        flag = 0
        for w in sent.split(' '):
            if w in negation:
                print '  negation found', w
                flag = 1
        return flag  