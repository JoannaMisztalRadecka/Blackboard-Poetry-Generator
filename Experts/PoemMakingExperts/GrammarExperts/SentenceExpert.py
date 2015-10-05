from nltk import parse_cfg, ChartParser
import nltk
from random import choice
import en
from Word import *
from GrammarExpert import *

class SentenceExpert(GrammarExpert):
    """Expert generating sentences from defined CFG grammar"""

    def __init__(self, blackboard, tense = "present", person = 1):
        super(SentenceExpert, self).__init__(blackboard, "Sentence Expert", tense, person,5)
        self.eva = ["be", "look", "feel"]
        self.atv = ["like", "hate", "love", "know", "need", "see"]

        """ eva - emotional verb active
            evp - emotional verb passive
            ej - emotion adjective
            en - emotional noun
            atv - attitude verb
        """
        self.grammar = nltk.parse_cfg("""
            S -> P | EP | Person ATV NP
            P -> NP VP 
            EP -> Person EVA EJ | NP EVP Pron EJ | ENP VP
            ENP ->  EN OF NP 
            NP -> Det N | Det JJ N | Det EJ JJ N | Det EJ N | Det EN
            VP -> V | V ERB | ERB V
            Det -> 'the'
            N -> 'n'
            V -> 'v' 
            EVA -> 'eva'
            EVP -> 'makes' 
            EN -> 'en'
            EJ -> 'ej'
            JJ -> 'adj'
            ERB -> 'erb'
            ATV -> 'atv'
            Person -> 'person'
            Pron -> 'pron'
            OF -> 'of'
            CC -> 'and' | 'but' | 'because' | 'so'
            """)
    


    ''' Generate phrase according to grammar and lexical rules'''
    def generate_phrase(self, pool):
        parser = ChartParser(self.grammar)
        gr = parser.grammar()
        phrase = self.produce(gr, gr.start())
        noun = choice(list(pool.nouns))
        try:
            replace_words = {'n':[noun], 'v': [Word(self.conjugate(v.name)) for v in list(pool.verbs[noun])], 
                             'adj': pool.epithets[noun],
                             'atv':[Word(self.conjugate(v, self.person)) for v in self.atv],
                             'eva':[Word(self.conjugate(v, self.person)) for v in self.eva],
                             'ej': pool.emotional_adjectives,'en':pool.emotional_nouns,
                             'erb': pool.emotional_adverbs, 'person':[Word(self.persons[self.person][0])], 
                             'pron':[Word(self.persons[self.person][1])]}
        except:
            return
        for pos in replace_words:
            while pos in phrase:
                try:
                    word = choice(replace_words[pos])
                    phrase = self.replace_pos(pos,word,phrase)
                except:
                    return
        for w in phrase:
            if not isinstance(w, Word):
                phrase[phrase.index(w)] = Word(w)
        return phrase




