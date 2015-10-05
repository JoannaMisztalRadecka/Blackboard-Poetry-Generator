from Experts.Expert import *

class ControlExpert(Expert):
    """Evaluating expert"""

    def select_phrases(self, pool, line_nr):
        pass

    def evaluate_lines(self):
        pass

    

    
    """Selecting best phrase from pool """
    def select_phrases(self, pool, line_nr):
        '''given an iterable of pairs return the key corresponding to the greatest value'''
        def argmin(pairs):
            min_fit = min(pairs.values())
            winners = [w for w in pairs if pairs[w] is min_fit]
            return winners
        phrases_eval = self.evaluate_lines(line_nr)
        pool.phrases_dict =  [pool.phrases_dict[i] for i in argmin(phrases_eval)]
