from random import choice
from Experts.Expert import *
from itertools import *

class SyllablesExpert(Expert):
    """Expert selecting words in poem from candidates"""

    def __init__(self, blackboard):
        super(SyllablesExpert, self).__init__(blackboard, "Syllables Expert")

    def heuristics(self, target_syls, line, candidate):
        av_nr_of_syls = 1
        words_in_line = [w for w in line if w.name is not None]
        estimated_syls_line_nr = sum([w.syllables for w in words_in_line]) + av_nr_of_syls * (len(line) - len(words_in_line) - 1) + candidate.syllables
        counts = [l.count(candidate) for l in self.blackboard.poem]
        cand_count = sum(counts)
        return abs(target_syls - estimated_syls_line_nr)+cand_count
            
    def select_candidate(self, target_syls, line, candidates):
        fitness = {}
        for c in candidates:
            fitness[c] = self.heuristics(target_syls, line,c)
        min_fit = 0
        min_fit = min(fitness.values())

        winners = [w for w in fitness if fitness[w] is min_fit]
        return choice(winners)


    """Selecting best phrase from pool (number of syls evaluation)"""
    def select_phrases(self, pool, line_nr):
        target_syls = self.blackboard.syllables[line_nr]

        #Count syls in phrase
        def count_syls(phrase):
            return sum([w.syllables for w in phrase])

        # given an iterable of pairs return the key corresponding to the greatest value
        def argmin(pairs):
            min_fit = min(pairs.values())
            winners = [w for w in pairs if pairs[w] is min_fit]
            return winners

        #count dif of phrases syls and target syls for line
        def evaluate_syls(phrase, target_syls):
            return abs(target_syls-count_syls(phrase))

        phrases_eval = {i:evaluate_syls(pool.phrases_dict[i][0].words, self.blackboard.syllables[line_nr]) for i in range(len(pool.phrases_dict))}
        pool.phrases_dict = [pool.phrases_dict[i] for i in argmin(phrases_eval)]
