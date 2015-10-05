from Experts.Expert import *
import random

class DiversityExpert(Expert):
    """expert choosing the least common phrase"""
       
    def __init__(self, blackboard):
        super(DiversityExpert, self).__init__(blackboard, "Diversity Expert")

    """Selecting phrase from list of least common expert"""
    def select_phrase(self, pairs):
        min_fit = min([p[1].counter for p in pairs])
        winners = [w for w in pairs if w[1].counter == min_fit]
        winner = random.choice(winners)
        winner[1].counter += 1
        return winner
        

