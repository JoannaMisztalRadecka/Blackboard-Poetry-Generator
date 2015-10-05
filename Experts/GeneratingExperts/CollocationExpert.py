import nltk
from Word  import *
import random
from Experts.GeneratingExperts.WordGeneratingExpert import *

class CollocationExpert(WordGeneratingExpert):
    """Generating most common contexts for words for words"""


    def __init__(self, blackboard):
        super(CollocationExpert, self).__init__(blackboard, "Collocation Expert")
        tagged_words = nltk.corpus.brown.tagged_words(simplify_tags=True)
        self.word_tag_pairs = nltk.bigrams(tagged_words)

    '''Finding verbs for noun '''
    def _find_verbs(self, word):
        verbs = list(nltk.FreqDist(b[0] for (a, b) in self.word_tag_pairs if a[0] == word.name and a[1] == 'N' and b[1].startswith('V')))
        return verbs
    
    '''Finding adjectives for noun'''
    def _find_epithets(self,word):
        epithets = list(nltk.FreqDist(a[0] for (a, b) in self.word_tag_pairs if b[0] == word.name and b[1] == 'N' and a[1] == 'ADJ'))
        return epithets

    '''Finding nouns described by adjective'''
    def _find_comparisons(self, adjective):
        comparisons = list(nltk.FreqDist(b[0] for (a, b) in self.word_tag_pairs if a[0] == adjective.name and b[1] == 'N' and a[1] == 'ADJ'))
        return comparisons

    '''Adding epithets for noun to pool'''
    def _add_epithets(self, word, pool):
        epithets = set([Word(w,"JJ") for w in self._find_epithets(word)])
        if word not in pool.epithets:
            pool.epithets[word] = []
        pool.epithets[word] += list(epithets)
        return epithets
        

    def _add_verbs(self, word, pool):
        verbs = set([Word(w,"V") for w in self._find_verbs(word)])
        pool.verbs[word] = list(verbs)
        return verbs

        
    '''Adding nouns for adjectives to pool'''
    def _add_comparisons(self, adj, pool):
   
        comparisons = set([Word(w,"N") for w in self._find_comparisons(adj)])
        pool.comparisons[adj] = comparisons
        return comparisons

    def _find_collocations(self,word_collection):
        finder = deepcopy(self.finder)
        finder.apply_ngram_filter(lambda w1, w2: w1 not in word_collection and w2 not in word_collection )# w1 != word and w2!= word# or w1 in (stopwords.words('english')+string.punctuation) or w2 in (stopwords.words('english')+string.punctuation)) #filtering collocations with keywords
        #filtering stopwords and punctuation
        finder.apply_word_filter(lambda x: x in (stopwords.words('english')))
        finder.apply_word_filter(lambda x: x in (string.punctuation))
        return finder.nbest(max,10)

    def generate_words(self, pool):
        super(CollocationExpert, self).generate_words(pool)
        counter = 0
        for w in pool.nouns:
            eps = self._add_epithets(w, pool)
            vs = self._add_verbs(w,pool)
            le = len(eps)
            lv = len(vs)
            counter += le + lv
        for adj in pool.adjectives:
            comps = self._add_comparisons(adj, pool)
            counter += len(comps)
        return counter

