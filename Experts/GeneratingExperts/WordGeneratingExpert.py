from Experts.Expert import *

class WordGeneratingExpert(Expert):
    """Expert adding words to pool"""

    def __init__(self, blackboard, name):
        super(WordGeneratingExpert, self).__init__(blackboard, name)

    """Return size of generated words """
    def generate_words(self, pool):
        print "Generating words ", self.name


    """ Return how many ideas can produce for pool """
    def estimate_ideas_size(self, pool):
        print "Estimating ideas... ", self.name
        size = self.generate_words(pool)
        pool.inspiration += size
        #print "Ideas size: ", size
        return size


