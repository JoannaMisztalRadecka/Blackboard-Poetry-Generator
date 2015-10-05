from Experts.Expert import *
import nltk

class AnaphoraExpert(Expert):
    """Making anaphoras - repeating first words of former line to generate phrase from ngram model"""

    def __init__(self, blackboard):
        super(AnaphoraExpert, self).__init__(blackboard, "Anaphora Expert")

    ''' add first word from last line to pool ngram seeds '''
    def add_anaphora(self, pool):
        if len(pool.poem)>0:
            try:
                last_line = pool.poem[-1]
                first_word = last_line[0].words[0]
                if first_word.name not in (nltk.corpus.stopwords.words('english') + ["!","?", "o", "oh"] ):
                    pool.ngram_seed.append(first_word)
            except:
                return

