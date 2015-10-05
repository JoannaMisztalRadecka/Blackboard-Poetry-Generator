from curses.ascii import isdigit
from nltk.tokenize.punkt import PunktWordTokenizer
from nltk.corpus import cmudict, wordnet
from nltk import pos_tag, WordNetLemmatizer,FreqDist
from Utils import *
from PhoneticsUtils import *
import nltk
from Properties import *


class Word(object):
    """Basic component of the poem"""

    def __init__(self, name, pos=None):
        if name is not None:
            self.name = name.lower()
        else:
            self.name = None
        if name is not None:
           # self.phonetics = self.check_phonetics(self.name)
            self.syllables = count_word_syllables(self.name)
        if pos is None:
             self.pos= pos_tag([self.name])[0][1]
        else:
            self.pos = pos
        self.wn_tag = self.get_wordnet_pos()
        if self.name is not None and self.wn_tag is not '':
            self.lemma = self.get_lemma()
        else:
            self.lemma = ''
        #self.sentiment = self.get_sentiment_swd()



    '''get simplified pos tag for wordnet'''
    def get_wordnet_pos(self):
        if self.pos.startswith('J'):
            return wordnet.ADJ
        elif self.pos.startswith('V'):
            return wordnet.VERB
        elif self.pos.startswith('N'):
            return wordnet.NOUN
        elif self.pos.startswith('R'):
            return wordnet.ADV
        else:
            return ''


    '''find base form of word'''
    def get_lemma(self):
        lemmatizer = nltk.WordNetLemmatizer()
        lemma = lemmatizer.lemmatize(self.name, self.wn_tag)
        return lemma


    def similar(self,context, word, num=20):
        word = word.lower()
        wci = context._word_to_contexts
        if word in wci.conditions():
            contexts = set(wci[word])
            fd = FreqDist(w for w in wci.conditions() for c in wci[w]
                          if c in contexts and not w == word)
            words = fd.keys()[:num]
            del fd
            return words
        else:
            return []

    #def count_syllables(self):
    #    if len(self.phonetics)>0:
    #        return len(list(y for y in self.phonetics[0] if isdigit(y[-1])))

    #    return 0

    #'''reading sentiment value for word from Sentiwordnet'''
    #def get_sentiment_swd(self):
    #     #sentiment analysis
    #    n = lambda x: x.name.split(".",1)[0]
    #    if self.name is not None:
    #        sents = swn.senti_synsets(self.name,self.get_wordnet_pos())
    #        if len(sents)>0:
    #            #which meaning?
    #            return sents[0]
    #    return []
    
    #''' check pronounciation in dictionary''' #todo: for words that are not in dict
    #def check_phonetics(self):
    #    return check_phonetics(self.name)

    def __str__(self):
        if self.name is not None:
            return self.name
        return self.pos

    def __repr__(self):
        if self.name is not None:
            return self.name
        return self.pos

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name
        else:
            return False

    def __hash__(self):
        return hash((self.name, self.pos))

    def __ne__(self, other):
        return not self.__eq__(other)



