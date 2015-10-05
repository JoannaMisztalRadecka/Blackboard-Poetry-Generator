from nltk import parse_cfg, ChartParser
import nltk
from random import choice
import en
from Word import *
from GrammarExpert import *
import random
from Phrase import *

class RhetoricalExpert(GrammarExpert):
    """Making rhetorical questions"""

    def __init__(self, blackboard, tense = "present"):
        super(RhetoricalExpert, self).__init__(blackboard, "Rhetorical Expert", tense, 3)
        self.grammar = nltk.parse_cfg("""
            S -> WHAT BE Det NP | WHY BE Det N SO JJ
            NP -> JJ N | N
            JJ -> 'adj'
            N -> 'n'
            Det -> 'the'
            BE -> 'be'
            SO -> 'so'
            WHAT -> 'what'
            WHY -> 'why'
            """)
    
    def generate_phrase(self, pool):
        noun = random.choice(list(pool.nouns))
        parser = ChartParser(self.grammar)
        gr = parser.grammar()
        phrase = self.produce(gr, gr.start())
        phrase.append("?")
       
        try:
            adj = choice(pool.epithets[noun])
        except:
            return
        replace_words = {'adj':adj, 'n': noun, 'be': self.conjugate("be")}
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
    

