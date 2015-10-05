from random import choice
from Word import *
from Experts.Expert import *
from Experts.PoemMakingExperts.PoemMakingExpert import *

class OxymoronExpert(PoemMakingExpert):
    """Making oxymoron (words with opposite meaning, antonyms) by enumarating antonyms or adding antonym epithet"""

    def __init__(self, blackboard):
        super(OxymoronExpert, self).__init__(blackboard, "Oxymoron Expert", 2)

    def generate_phrase(self, pool):
        try:
            word = choice(list(pool.antonyms))
            antonym = choice(list(pool.antonyms[word]))
            phrase = []
            phrase.append(word)
            phrase.append(Word(choice(["and", "or", "but"])))
            phrase.append(antonym)
            return phrase
        except:
            return
