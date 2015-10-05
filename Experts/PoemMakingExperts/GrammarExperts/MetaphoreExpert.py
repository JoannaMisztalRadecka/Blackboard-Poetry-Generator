from nltk import parse_cfg, ChartParser
import nltk
from random import choice
import en
from Word import *
from GrammarExpert import *
import random

class MetaphoreExpert(GrammarExpert):
    """Generating metaphores"""

    def __init__(self, blackboard, tense = "present", person = 3 ):
        super(MetaphoreExpert, self).__init__(blackboard, "Metaphore Expert",tense = tense, person = person, importance = 2)
        self.grammar = nltk.parse_cfg("""
            S -> Person BE LIKE NP 
            NP -> Det JJ N | Det N
            Person -> 'person'
            JJ -> 'adj'
            N -> 'n'
            Det -> 'the'
            BE -> 'be'
            LIKE -> 'like'
            """)
       
    def generate_phrase(self, pool):
        parser = ChartParser(self.grammar)
        gr = parser.grammar()
        phrase = self.produce(gr, gr.start())
        noun = random.choice(list(pool.nouns))
        adj = choice(pool.epithets[noun])
        replace_words = {'adj':adj, 'n': noun, 'be': self.conjugate("be",self.person), 'person' : self.persons[self.person][0]}
        for pos in replace_words:
            while pos in phrase:
                try:
                    phrase = self.replace_pos(pos,replace_words[pos],phrase)
                except:
                    return
        for w in phrase:
            if not isinstance(w, Word):
                phrase[phrase.index(w)] = Word(w)
        return phrase
    

