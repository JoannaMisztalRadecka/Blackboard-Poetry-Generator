from random import choice
from Word import *
from Experts.PoemMakingExperts.PoemMakingExpert import *
from copy import deepcopy

class ExclamationExpert(PoemMakingExpert):
    """Adding exclamation to phrases"""

    def __init__(self, blackboard):
        super(ExclamationExpert, self).__init__(blackboard, "Exclamation Expert")
       
    def generate_phrase(self, pool):
        phrase = deepcopy(choice(pool.phrases_dict))[0].words
        if phrase[-1].name not in ["!", "?"]:
            phrase.append(Word("!"))
        return phrase

