from Experts.PoemMakingExperts.PoemMakingExpert import *
from random import choice

class RepetitionExpert(PoemMakingExpert):
    """Repeating words to emphasise them"""

    def __init__(self, blackboard):
        super(RepetitionExpert, self).__init__(blackboard, "Repetition Expert")

    def generate_phrase(self, pool):
        if len(pool.poem)>1:
            phrase = choice(pool.poem)
            return phrase[0].words

