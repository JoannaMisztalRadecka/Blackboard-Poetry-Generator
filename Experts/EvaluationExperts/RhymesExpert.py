from ControlExpert  import*
import PhoneticsUtils
from Word import *
from Phrase import *
import copy

class RhymesExpert(ControlExpert):
    """Expert evaluating rhymes in lines"""

    def __init__(self, blackboard):
        super(RhymesExpert, self).__init__(blackboard, "Rhymes Expert")

    '''check the quality of rhyme (how many phonemes are the same)'''
    def rhyme_quality(self,word1,word2 ):
        """ Determine a numerical quality of the rhyme between two pronunciation lists. 
    
            >>> rhyme_quality( ["A", "B", "C"], ["A", "B"] )
            0
            >>> rhyme_quality( ["A", "B", "C"], ["B", "C"] )
            2
            >>> rhyme_quality( ["A", "B"], ["A", "B"] )
            0
            >>> rhyme_quality( ["B", "B", "C", "D"], ["A", "B", "C", "D"] )
            3
        """
        
        p1 = PhoneticsUtils.check_phonetics(word1.name)
        p2 = PhoneticsUtils.check_phonetics(word2.name)

        if len(p1) == 0 or len(p2) == 0:
            return 0

        p1 = copy.deepcopy(p1)[0]
        p2 = copy.deepcopy(p2)[0]
    

        p1.reverse()
        p2.reverse()
        if p1 == p2:
            # G-Spot rocks the G-Spot
            return 0
        quality = 0
        for i, p_chunk in enumerate(p1):
            try:
                if p_chunk == p2[i]:
                    quality += 1
               # if p_chunk != p2[i]:
                #    break
            except IndexError:
                break
        return quality

    def phrases_rhyme_quality(self,p1, p2):
        if p1.words[-1].name not in ["!","?"]:
            w1 = p1.words[-1]
        else:
            w1 = p1.words[-2]
        if p2.words[-1].name not in ["!","?"]:
            w2 = p2.words[-1]
        else:
            w2 = p2.words[-2]
        return self.rhyme_quality(w1, w2)

    def cross_line_rhyme_evaluation(self, phrase, line_nr):
        try:
            if line_nr<=2:
                return 0
            else:
                cross_line = self.blackboard.pool.poem[-2][0]
                return self.phrases_rhyme_quality(phrase, cross_line)
        except:
            return 0


    def any_rhyme_evaluation(self, phrase, line_nr):
        try:
            if line_nr<2:
                return 0
            else:
                max_r = 0
                for l in self.blackboard.pool.poem:
                    if len(l)>0:
                        r = self.phrases_rhyme_quality(phrase, l[0])
                        if r>max_r:
                            max_r = r
                return (-1)*max_r
        except:
            return 0

    def evaluate_lines(self, line_nr):
        phrases_eval = {i:self.any_rhyme_evaluation(self.blackboard.pool.phrases_dict[i][0], line_nr) 
                        for i in range(len(self.blackboard.pool.phrases_dict))}
        return phrases_eval
        





