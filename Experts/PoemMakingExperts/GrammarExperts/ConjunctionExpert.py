import en
from random import choice, randrange
from Experts.PoemMakingExperts.PoemMakingExpert import *

class ConjunctionExpert(PoemMakingExpert):
    """Expert making enumerating words"""

    """ min and max number of words """
    def __init__(self, blackboard, min = 2, max = 3):
        super(ConjunctionExpert, self).__init__(blackboard, "Conjunction Expert")
        self.blackboard = blackboard
        self.min_words = min
        self.max_words = max

    """make ennumeration from random nouns from list"""
    def generate_phrase(self, pool):
        random_length = randrange(self.min_words,self.max_words+1)
        #filtered_words = [w for w in words if en.is_noun(w)] #filter nouns
        selection = []
        for i in range(random_length):
            word = choice(pool.nouns)
            selection.append(word)
        return en.list.conjunction(selection) #make enumeration

