import en, nltk, copy
from Word import *

class PoolOfIdeas(object):
    """Set of phrases derived from given keyword"""

    def __init__(self, keyphrase, syllables, sentences = []):
        self.title = keyphrase
        self.sentences = sentences
        self.poem = []
        #self.phrases = [self.parse_phrase(keyphrase)]
        self.phrases_dict = []
        self.emotion = ""

        ### pool words ###
        self.nouns = set()
        self.adjectives = set()
        self.verbs = {}
        self.epithets = {}
        self.comparisons = {}
        self.synonyms = {}
        self.hypernyms = {}
        self.antonyms = {}
        self.emotional_adjectives = []
        self.emotional_nouns = []
        self.emotional_adverbs = []


        self.ngram_seed = []
        self.next_line = []
        self.inspiration = 0 #to be evaluated after generating words


    """Print all lines of poem"""
    def str_poem(self):
        s = ""
        s += self.title + "\n\n"
        for line in self.poem:
            try:
                s +=  str(line[0]) +"\n"
            except:
                pass
        return s

    def print_experts(self):
        s = ""
        for line in self.poem:
            try:
                s +=  str(line[1]) +": " + str(line[0])+"\n"
            except:
                pass
        return s

   
    def __str__(self):
        s = "Title: " + str(self.title) + "\n"
        s+= "Sentences: "+ str(len(self.sentences))+str(self.sentences) + "\n"
        
        s+= "Emotion: " +str(self.emotion) + "\n"
        s+= "Nouns: " + str(len(self.nouns))+ str(self.nouns) + "\n"
        s+= "Adjectives: "+ str(len(self.adjectives)) + str(self.adjectives) + "\n"
        s+= "Verbs: " + str(len(self.verbs))+str(self.verbs) + "\n"
        s+= "Epithets: " + str(len(self.epithets)) +str(self.epithets) + "\n" 
        s+= "Compraisons: "+ str(len(self.comparisons)) + str(self.comparisons) + "\n"
        s+= "Synonyms: "+ str(len(self.synonyms)) + str(self.synonyms) + "\n"
        s+= "Hypernyms: "+ str(len(self.hypernyms))+ str(self.hypernyms) + "\n"
        s+= "Antonyms: " + str(len(self.antonyms))+ str(self.antonyms) + "\n"
        s+= "Emotional adjectives: " + str(len(self.emotional_adjectives))+ str(self.emotional_adjectives) + "\n"
        s+= "Emotional nouns: "+ str(len(self.emotional_nouns)) + str(self.emotional_nouns) + "\n"
        s += "Emotional adverbs: "+ str(len(self.emotional_adverbs)) + str(self.emotional_adverbs) + "\n"
        s += "Inspiration: " + str(self.inspiration) + "\n"
        return s


        """Print all lines of poem"""
    def __repr__(self):
        s = ""
        s += self.title + "\n\n"
        for line in self.poem:
            try:
                s += repr(line[0]) +"\n"
            except:
                pass
        return s

    def __hash__(self):
       return hash(self.title)