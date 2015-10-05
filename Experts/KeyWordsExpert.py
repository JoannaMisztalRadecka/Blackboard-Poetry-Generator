from Experts.PoemMakingExperts.PoemMakingExpert import *
from Experts.GeneratingExperts.WordGeneratingExpert import *
import en, nltk
import KeyPhrasesExtractor
from PoolOfIdeas import *

class KeyWordsExpert(PoemMakingExpert, WordGeneratingExpert):
    """Expert extracting keyphrases, making pools, extracting keywords and adding them to pool"""

    def __init__(self, blackboard):
        super(KeyWordsExpert, self).__init__(blackboard, "Keywords Expert")


    """Find nouns in keyphrase"""
    def generate_words(self, pool):
        super(KeyWordsExpert, self).generate_words(pool)
        phrase = pool.title
        nouns = en.sentence.find(phrase, "NN")
        adjs = en.sentence.find(phrase, "JJ")
        for n in nouns:
            wn = Word(en.noun.singular(n[0][0]),"NN")
            pool.nouns.add(wn)
            pool.epithets[wn] =  []
            jn = "JJ " + wn.name
            epithets = en.sentence.find(phrase, jn)
            pool.epithets[wn]+=[Word(e[0][0],e[0][1]) for e in epithets]
        pool.adjectives |= set([Word(w[0][0],w[0][1]) for w in adjs])

    
    """Parse string phrase to list of words with tags """
    def generate_phrase(self, pool):
        phrase = pool.title
        tokens = nltk.word_tokenize(phrase)
        pos_phrase = nltk.pos_tag(tokens)
        new_phrase = [Word(w[0], w[1]) for w in pos_phrase]
        return new_phrase


    def _tokenize_sentences(self):
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = tokenizer.tokenize(self.blackboard.text)
        return sentences

    def _get_phrase_sents(self, pool):
        kp = self.generate_phrase(pool)
        sents = []
        for s in self.blackboard.sentences:
            contains = True
            for k in kp:
                if k.name not in s.lower():
                    contains = False
                    break
            if contains is True:
                sents.append(s)
        pool.sentences = sents

    def get_keyphrases(self):
         keyphrases = list(set(KeyPhrasesExtractor.get_keyphrases(self.blackboard.text)))
         self.blackboard.keyphrases = keyphrases
         self.blackboard.sentences = self._tokenize_sentences()
         #create space for generation from each keyphrase
         for kp in self.blackboard.keyphrases:
             if kp != '':
                 pool_kp = PoolOfIdeas(kp,self.blackboard.syllables)
                 self._get_phrase_sents(pool_kp)
                 self.blackboard.pool_of_ideas[kp] = pool_kp






