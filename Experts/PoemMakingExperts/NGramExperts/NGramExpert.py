from nltk.probability import LidstoneProbDist  
from nltk.model import NgramModel
import nltk, random
from nltk.corpus import gutenberg
from Word import *
import string
from Experts.PoemMakingExperts.PoemMakingExpert import *
        


class NGramExpert(PoemMakingExpert):
    """Generating text from ngram model of input text"""

    def __init__(self, blackboard,  min_words = 4, max_words = 8):
         super(NGramExpert, self).__init__(blackboard, "NGram Expert")
         self.blackboard = blackboard
         self.min = min_words
         self.max = max_words
         self.poems = list(gutenberg.words('blake-poems.txt'))
         self.poems.extend(list(gutenberg.words('whitman-leaves.txt')))
         self.poems.extend(list(gutenberg.words('shakespeare-macbeth.txt')))
         self.poems.extend(list(gutenberg.words('shakespeare-hamlet.txt')))
         self.poems.extend(list(gutenberg.words('shakespeare-caesar.txt')))
         self.poems.extend(list(gutenberg.words('milton-paradise.txt')))
         exclude = set(string.punctuation)
         self.poems = [w.lower() for w in self.poems if w not in exclude] 
         self.poem_bigrams = nltk.bigrams(self.poems) 
         self.cfd = nltk.ConditionalFreqDist(self.poem_bigrams)


    """Split text into words and return list of words"""
    def tokenize(self, text):
        split = text.splitlines()
        tokenize = [nltk.word_tokenize(s) for s in split]
        words = [w for l in tokenize for w in l]
        return words

    def make_model(self, text):
        tokens = self.tokenize(text)
        bigrams = nltk.bigrams(tokens) 
        cfd = nltk.ConditionalFreqDist(bigrams)
        return cfd

    """Generate text from model"""
    def generate_text(self,text, word):
        self.cfd = self.make_model(text)
        generated_text = []
        num = random.randrange(self.min, self.max)
        for i in range(num):
            try:
                generated_text.append(word),
                word = self.cfd[word].max()
            except:
                return []
        return generated_text

    """generate from existing corpora of poems"""
    def generate_phrase(self, pool):
        word = random.choice(pool.ngram_seed)
        generated_text = []
        num = random.randrange(self.min, self.max)
        w = word.name
        for i in range(num):
            try:
                generated_text.append(w),
                w = self.cfd[w].max()
            except:
                return
        return [Word(w) for w in generated_text]

