from Word import *
from AbstractionLevel import *
import nltk
from PoolOfIdeas import *
from Properties import *
from random import randint, choice


class Blackboard(object):
    """Public blackboard with current state of poem and partial solutions"""
    def __init__(self, text_file, syllables):
        self.text = open(text_file).read()
        self.poem = []
        self.syllables = syllables
        self.keyphrases = []
        self.pool_of_ideas = {}
        self._pool = None
        self.pool = property(self.get_pool, self.set_pool)
        self.tense = choice(["past", "present"])
        self.person = randint(1,3)
        print "Tense: ", self.tense, " Person: ", self.person
        self.sentences = []

        self.poem = []
        #self.phrases = [self.parse_phrase(keyphrase)]
        self.phrases_dict = []
        self.ngram_seed = []
        self.next_line = []
        
        ###triggered experts ###
        self._bb_ready_experts = []
        self._bb_keywords_generated_experts = []
        self._bb_words_generated_experts = []
        self._bb_phrases_generated_experts = []
        self._bb_line_added_experts = []
  

    ### triggers ###

    def get_pool(self):
        return self._pool

    def set_pool(self, value):
        self._pool = value
        print "set pool"
        #for callback in self._observers:
        #    print 'anouncing change'
        #    callback(self._global_wealth)

    def set_bb_ready(self):
        pass

    def set_bb_keywords_generated(self):
        pass

    def set_bb_words_generated(self):
        pass

    def set_bb_pool_selected(self):
        pass

    def set_bb_phrases_generated(self):
        pass

    def set_bb_line_added(self):
        pass

    def set_bb_poem_finished(self):
        pass



    def __str__(self):
        s = "\n Poem: \n"
        for l in self.poem:
            for w in l:
                s+= w.__str__()
                s+=" "
            s+= "\n"
        return s

    def __repr__(self):
        s = "Poem: \n"
        for l in self.poem:
            for w in l:
                s+= w.__str__()
            s+= "\n"
        return s
   
