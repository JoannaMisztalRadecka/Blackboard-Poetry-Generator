from nltk.corpus import stopwords,WordNetCorpusReader
from nltk.tokenize.punkt import PunktWordTokenizer, PunktSentenceTokenizer
import nltk,subprocess, shlex, Properties
from nltk import pos_tag, ContextIndex
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import cmudict, wordnet, WordNetCorpusReader, words
from Word import *
from Properties import *

#from sentiwordnet import SentiWordNetCorpusReader, SentiSynset

from AffectTree import *
import pickle

#preparing resources...
#pronounciation dictionary - cmu
pron_dict= cmudict.dict()
#SentiWordNet
#swn = SentiWordNetCorpusReader(swn_filename)
wordnet_1_6 = WordNetCorpusReader(wn_1_6_corpus_root)
#wordnet dict for id search
english_wordlist = list(w.lower() for w in nltk.corpus.words.words())
with open(Properties.anew_filename, 'r') as f:
        anew_list = {l.rstrip().split("\t")[0]:(float(l.rstrip().split("\t")[2]),float(l.rstrip().split("\t")[4])) for l in f.readlines()[1:]}
web_text = nltk.Text(word.lower() for word in nltk.corpus.webtext.words()) 
#if '_word_context_index' not in web_text.__dict__:
#    print 'Building word-context index...'
#    word_context_index = ContextIndex(web_text.tokens, filter=lambda x:x.isalpha(), key=lambda s:s.lower())
          

def pickle_wn_dict_id():
    #wordnet dict for id search
    n= lambda s: s.name.split(".",1)[0]
    syns = list(wordnet_1_6.all_synsets())
    wn_id_dict = dict([(s.offset, n(s)) for s in syns])
    with open('wn_id_dict.txt', 'wb') as handle:
        pickle.dump(wn_id_dict, handle)

''' Return words from text without stopwords'''
def filter_words(text_file):
    text=read_text(text_file)
    tokenizer = RegexpTokenizer(r'\w+')
    token = tokenizer.tokenize(text)
    pos_list=nltk.pos_tag(token)
    filtered_words = [w for w in pos_list if not w[0] in stopwords.words('english')]
    return filtered_words

def filter_stopwords_tokens(tokens):
    filtered_words = [w for p in tokens for w in p if not w[0] in stopwords.words('english')]
    return list(set(filtered_words))

def read_text(text_file):
    with open(text_file, 'r') as f:
        text=f.read()
    return text


"""return pronounciation if word in phonetic dict"""
def check_phonetics(word):
    try:
        return pron_dict[word]
    except:
        return []

"""Split text into words and return list of Word objects"""
def tokenize(text):
        split = text.splitlines()
        tokenize = [nltk.word_tokenize(s) for s in split]
        words = [[Word(w) for w in l]for l in tokenize]
        return words

def get_pos(token):    
        pos = [[t.pos for t in l]for l in tokoens]
        return pos

def tokenize_sentences(text):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(text)
    return sentences



def get_key_phrases(text):
    print "Tokenizing text..."
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(text)
    tokens = [nltk.word_tokenize(s) for s in sentences]
    print "POS tagging of text..."
    pos = [nltk.pos_tag(t) for t in tokens]
    print "Finding noun phrases..."

    grammar = r"""
  NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN
  PP: {<IN><NP>}               # Chunk prepositions followed by NP
  VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
  CLAUSE: {<NP><VP>}           # Chunk NP, VP
  """
    cp = nltk.RegexpParser(grammar)
    phrases = []
    for sent in pos:
        tree = cp.parse(sent)
        for subtree in tree.subtrees():
            if subtree.node in ['NP','PP','VP','CLAUSE']: 
                phrases.append(subtree.leaves())
    return phrases

    
    



'''Preparing emotion lookup table - joining AFINN and SentiStrength'''
def extend_emotion_lookup():
    file_afinn = "C:/SentStrength_Data/AFINN.txt"
    file_emot = "C:/SentStrength_Data/EmotionLookupTable old version.txt"
    file_new_emot = "C:/SentStrength_Data/new.txt"
    try:
        f = open(file_afinn, "r")
        try:
            lines_finn = f.readlines()
            
            lines_split_finn = [l.replace(" ","\t").split("\t") for l in lines_finn]
            lines_temp = list(lines_split_finn)
            f.close()
            f = open(file_emot, 'r')
            lines_emot = f.readlines()
            lines_split_emot = [l.replace(" ","\t").split("\t") for l in lines_emot]
            for l in lines_split_emot:
                if l[0][-1] is '*':
                    for finn in lines_split_finn:
                       # print finn
                        if finn[0].startswith(l[0][:-1]):
                            if finn in lines_temp:
                                lines_temp.remove(finn)
            f.close()
            for l in lines_temp:
                if l[0] not in [w[0] for w in lines_split_emot]:
                    lines_split_emot.append(l)
            f = open(file_new_emot, 'w')
            new_lines = ['\t'.join(l)for l in lines_split_emot]
            new_lines.sort()
            f.writelines(new_lines) # Write a sequence of strings to a file
            f.close()
        finally:
            f.close()
    except IOError:
        pass

def draw_emotions():
    import matplotlib.pyplot as plt
    import numpy as np
    emotions_dict = {"joy":(4.60, 3.22), "love":(4.72, 2.44), "affection":(4.39, 2.21), "liking":(3.52, 2.63), "enthusiasm": (4.17, 3.38),"levity":(4.10, 2.93), "security":(3.28, 0.22), "gratitude": (2.89, 0.34), "pride": (3.00, 1.83), "calmness": (2.73, -0.4), "hope":(3.05, 1.44), "fear":(-1.24, 2.96), "sadness" :(-1.79, 1.21), "shame":(-1.87, 2.33),"anger":(-1.66, 3.63), "hate":(1.88, 2.95),"sympathy":(1.33, 1.03), "humility":(-2.1, 2.97), "despair":(-1.57, 1.68), "anxiety":(-1.23, 2.72), "apathy":(0.30, 0.00)}
    # emotions_dict = {"joy":(4.60, 3.22), "love":(4.72, 2.44), "affection":(4.39, 2.21), "liking":(3.52, 2.63), "enthusiasm": (4.17, 3.38), "gratitude": (2.89, 0.34), "self-pride": (3.00, 1.83), "calmness": (2.73, -0.4), "hope":(3.05, 1.44), "fear":(-1.24, 2.96), "sadness" :(-1.79, 1.21), "shame":(-1.87, 2.33),  "humility":(-2.1, 2.97), "despair":(-1.57, 1.68), "anxiety":(-1.23, 2.72), "daze":(1.04, 0.00), "apathy":(0.30, 0.00)}
    N = len(emotions_dict)
    X = [e[0] for e in emotions_dict.values()]
    Y = [e[1] for e in emotions_dict.values()]
   
    labels = emotions_dict.keys()#['point{0}'.format(i) for i in range(N)]
    plt.subplots_adjust(bottom = 0.1)
    plt.scatter(
        X, Y, marker = 'o', cmap = plt.get_cmap('Spectral'))
    for label, x, y in zip(labels,X, Y):
        plt.annotate(
            label, 
            xy = (x, y), xytext = (-1, 1),
            textcoords = 'offset points', ha = 'right', va = 'bottom')
            #bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
            #arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

    plt.xlabel('Valence')
    plt.ylabel('Arousal')
    plt.show()