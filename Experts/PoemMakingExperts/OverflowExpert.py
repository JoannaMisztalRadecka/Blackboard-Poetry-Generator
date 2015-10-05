from Experts.PoemMakingExperts.PoemMakingExpert import *
from Phrase import *

class OverflowExpert(PoemMakingExpert):
    """Making overflow from phrase - breaking it to next line"""
    
    def __init__(self, blackboard):
        super(OverflowExpert, self).__init__(blackboard, "Overflow Expert")

    '''select phrases longer than goal for the line and break them'''
    def generate_phrase(self, pool):
        if len(pool.poem)<len(self.blackboard.syllables)-1:
            goal_syls = self.blackboard.syllables[len(pool.poem)] 
            next_goal_syls = self.blackboard.syllables[len(pool.poem)+1] 
            #Count syls in phrase
            def count_syls(phrase):
                return sum([w.syllables for w in phrase])
            for phrase in pool.phrases:
                if phrase.count_syllables() >= goal_syls + next_goal_syls:
                    pool.next_line.append(Phrase(phrase.words[int(goal_syls/2):]))
                    new_phrase = phrase.words[:int(goal_syls/2)]
                    return new_phrase
                    