from Experts.Expert import *

class EpiphoraExpert(Expert):
    """Making epiphoras - repeating last words of former line """
        
    def __init__(self, blackboard):
        super(EpiphoraExpert, self).__init__(blackboard, "Epiphora Expert")

    ''' add last word from last line to pool ngram seeds '''
    def add_epiphora(self, pool):
        if len(pool.poem)>0:
            try:
                last_line = pool.poem[-1]
                last_word = last_line[0].words[-1]
                if first_word.name not in (nltk.corpus.stopwords.words('english') + ["!","?"]):
                    pool.ngram_seed.append(first_word)
            except:
                return