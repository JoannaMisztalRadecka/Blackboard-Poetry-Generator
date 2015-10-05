from random import choice
from Word import *
from Experts.PoemMakingExperts.PoemMakingExpert import *

class ApostropheExpert(PoemMakingExpert):
    """Making apostrophes of given noun "Oh ... !" - adding hypernym """

    def __init__(self, blackboard):
        super(ApostropheExpert, self).__init__(blackboard, "Apostrophe Expert",2)
        self.apostrophes = [Word("O"), Word("Oh")]

    def generate_phrase(self, pool):
        noun = choice(list(pool.nouns))
        apostrophe = choice(self.apostrophes)
        try:
            hypernyms = pool.hypernyms[noun]
            hypernym = choice(hypernyms)
            epithets = list(pool.epithets[noun])
            epithet = choice(epithets)
        except:
            return
        verse = [apostrophe, noun, Word("the"), epithet, hypernym]
        return verse


