from Experts.Expert import *
from Phrase import *

class PoemMakingExpert(Expert):
    """Experts generating phrases to pool"""

    def __init__(self, blackboard, name, importance = 1):
        super(PoemMakingExpert, self).__init__(blackboard, name)
        self.counter = 0
        self.importance = importance

    def add_phrase(self, pool):
        print "Adding phrase: " + self.name
        if not self.precondition:
            return
        for i in range(self.importance):
            phrase = Phrase(self.generate_phrase(pool))
            pool.phrases_dict.append((phrase, self))


    
    ''' Generate phrase according to grammar and lexical rules'''
    def generate_phrase(self, pool):
        print "Generating phrase by expert: ", self.name
  


