from nltk import ConditionalFreqDist
from nltk.corpus import brown
from nltk.corpus import stopwords
from nltk.corpus import cmudict
from nltk import pos_tag
import nltk

class CorpusData(object):
    """some functions operating on corpus"""

    def __init__(self):
        self.cond_freq = self.conditional_frequencies()
        self.category = 'fiction'
        self.unigram_tagger = self.unigram_tagger()
        print "Opening phonetic dictionary... "
        self.pron_dict= cmudict.dict()

    def find_POS(self, word):
        #words_list = [w.name for w in self.words]
        return pos_tag(word.name)
      

    def conditional_frequencies(self):#dlugo... moze dla mniejszego zbioru?
        print "Making conditional frequencies..."
        cfd = ConditionalFreqDist((genre, word)for genre in brown.categories()
          for word in brown.words(categories=genre))
        return cfd

    #za dlugo
    def word_category(self,word):
        print "Finding category"
        if (word.name in stopwords.words('english')):
            return 'stopwords'
        categories = brown.categories()
        return max(categories, key=lambda cat:self.cond_freq[cat][word.name])


    def unigram_tagger(self):
        print "Making unigram model..."
        brown_tagged_sents = brown.tagged_sents(categories=self.category)
        brown_sents = brown.sents(categories=self.category)
        unigram_tagger = nltk.UnigramTagger(brown_tagged_sents)
        return unigram_tagger

    def check_phonetics(self,word):
        return self.pron_dict[word.name]