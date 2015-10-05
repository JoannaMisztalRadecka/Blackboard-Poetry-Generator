from Word import *
import itertools
from Utils import *
from nltk.corpus import words
import en


class Knowledge(object):
    """Knowledge of expert"""

    def __init__(self, phrases, one_letter = False):
        list_p = phrases
        if len(phrases)>0:
        #if without pos
            if type(phrases[0]) is not tuple:
                #don't allow one-letter words
                if not one_letter:
                    list_p = filter(lambda x: len(x)>1, phrases)
                    list_p = itertools.chain(*map(lambda x:x.split('_', 1 ),list_p))
                self.phrases = list(set([Word(w) for w in list_p if w in english_wordlist]))
            #if basic knowledge - key words
            else:
                if not one_letter:
                    list_p = filter(lambda x: len(x[0])>1, phrases)
                self.phrases = [Word(w[0],w[1]) for w in phrases if w[0] in english_wordlist]
            self.phrases = list(set(self.phrases))
            #print [ (w.name,w.pos) for w in self.phrases]  
            forms = self.add_forms()
            self.phrases = list(set(self.phrases)) + list(set(forms))
            self.phrases = list(set(self.phrases))
        else:
            self.phrases = []

    def add_forms(self):
        forms = []
        for w in self.phrases:
            if en.is_verb(w.name):
                try:
                    vb = en.verb.infinitive(w.name)
                    vbd = en.verb.past(w.name)
                    vbp1 = en.verb.present(w.name, person = 1)
                    vbp2 = en.verb.present(w.name, person = 2)
                    vbz = en.verb.present(w.name, person = 3)
                    vbg = en.verb.present_participle(w.name)
                    forms.append(Word(vb,"VB"))
                    forms.append(Word(vbd,"VBD"))
                    forms.append(Word(vbp1,"VBP"))
                    forms.append(Word(vbz,"VBZ"))
                    forms.append(Word(vbg,"VBG"))
                except:
                    print "Error in conjugation for verb:" + w.name
            elif en.is_noun(w.name):
                nns = en.noun.plural(w.name)
                forms.append(Word(nns, "NNS"))

        return forms
        

                
                
