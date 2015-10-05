from nltk.tokenize.punkt import PunktWordTokenizer, PunktSentenceTokenizer
import nltk
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from Word import *

class Template(object):
    """Template of a poem"""

    def __init__(self, template_file):
        self._template_file = template_file
        self._token_template = self.tokenize_template()
        self.template = self.make_template()
        self.template_pos = self.make_pos_template()
        self.template_syllables = self.make_syllables_template()
        print self.template
        
            
    def tokenize_template(self):
        with open(self._template_file, 'r') as f:
            poem_template_text=f.read()
        template_split = poem_template_text.splitlines()
        template_tokenize = [nltk.word_tokenize(s) for s in template_split]
        template_words = [[Word(w) for w in l]for l in template_tokenize]
        return template_words

    def make_template(self):
        def check_stopword(w):
            if w.name not in stopwords.words('english'):
                w.name = None
            return w
        template = [[check_stopword(w) for w in l]for l in self._token_template]
        return template

    def make_pos_template(self):    
        template_pos = [[t.pos for t in l]for l in self._token_template]
        return template_pos

    def make_syllables_template(self):
        syllables = [sum([s.syllables for s in t]) for t in self._token_template]
        return syllables

    




