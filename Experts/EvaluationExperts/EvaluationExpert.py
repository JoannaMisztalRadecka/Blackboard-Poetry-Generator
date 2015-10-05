from random import choice
from Experts.Expert import *
import logging

class EvaluationExpert(Expert):
    """ Expert selecting the best pool of ideas """

    def __init__(self, blackboard):
        super(EvaluationExpert, self).__init__(blackboard, "Evaluation Expert")
        self.pool_inspirations = {}
        logging.basicConfig(filename='poem.log',level=logging.INFO)

    """Select best pool """
    def select_pool(self):
        self.evaluate_pools()
        # given an iterable of pairs return the key corresponding to the greatest value
        def argmax(pairs):
            max_fit = max(pairs.values())
            winners = [w for w in pairs if pairs[w] is max_fit]
            return choice(winners)
        return argmax(self.pool_inspirations)

    """Evaluate blackboard pools"""
    def evaluate_pools(self):
        for pool in self.blackboard.pool_of_ideas.values():
            self.pool_inspirations[pool] = self.evaluate_inspiration(pool)

    """ Evaluate the inspiration of the pool by counting size of pool's elements """
    def evaluate_inspiration(self, pool):
        inspiration = pool.inspiration
        non_empty = 0 #nr of non empty wordsets
        pool_wordsets = (pool.nouns, pool.adjectives, pool.verbs, pool.epithets, pool.comparisons,
            pool.synonyms, pool.hypernyms, pool.antonyms, pool.emotional_adjectives, pool.emotional_nouns, 
            pool.emotional_adverbs)
        ###heuristics###
        for ws in pool_wordsets:
            if len(ws) > 0:
                non_empty += 1
        inspiration *= non_empty
        print pool.title, inspiration
        logging.info(pool.title + str(inspiration))
        return inspiration