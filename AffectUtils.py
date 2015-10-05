from xml.dom import minidom
import Properties
from Utils import *
import pickle
from nltk.tokenize.punkt import PunktWordTokenizer
import math
import string

class AffectNode:
    """ element from xml hierarchy for WN Affects"""

    def __init__(self, value, parent = None):
        self.value = value
        self.parent = parent
        if parent is not None:
            parent.add_child(self)
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class AffectTree:

    def __init__(self, root):
        self.root = root

    def find_ancestors(self, node):
        if node is self.root:
            return []
        else:
            return self.find_ancestor(node.parent).append(node.parent)

    def is_ancestor(self, node, parent):
        anc_list = self.find_ancestors(node)
        if parent in anc_list:
            return true
        else:
            return false 

    def find_offsprings_node(self, node):
        list = []
        if len(node.children)>0:
            for n in node.children:
                list.append(str(n))              
                list = list + self.find_offsprings_node(n)
        return list

    def find_offsprings(self, node_name):
        node = self.find_node(node_name)
        return self.find_offsprings_node(node)
                

    def find_from_node(self, node, node_name):
        if node.value == node_name:
            return node
        for n in node.children:
            found = self.find_from_node(n, node_name)
            if found is not None:
                return found
                      
                

    def find_node(self, node_name):
        return self.find_from_node(self.root,node_name)

##################help functions for affect computations#######################

'''calculate valence and arousal for given text ''' 
def calculate_text_sentiment(text):
#Sentiment calculation for each sentence
    sentences = tokenize_sentences(text)
    print "Rating text sentiment..."
    sentiments_valence = {s:calculate_valence(s) for s in sentences}
    pos_sent = sum([s[0] for s in sentiments_valence.values()])
    neg_sent = sum([s[1] for s in sentiments_valence.values()])
    #print (pos_sent,neg_sent)
    valence = pos_sent+neg_sent
    sentiments_arousal = {s:calculate_arousal(s) for s in sentences}
    arousal = sum(sentiments_arousal.values())/ float(len(sentiments_arousal))
    print "Valence: " + str(valence)
    print "arousal: "+ str(arousal)

    print "Generating affect words..."
    affect_tree = make_wn_affect_tree()
    emotion = get_emotion(valence,arousal)
    print "The emotional state is "+ emotion
    affect_words = find_affect_synsets_for_emotion(emotion,affect_tree)
    return list(set(affect_words))



''' Use sentistrength.jar to calculate text valence'''
#Alec Larsen - University of the Witwatersrand, South Africa, 2012 import shlex, subprocess
def calculate_valence(text):
    if text == '':
        return []
    #open a subprocess using shlex to get the command line string into the correct args list format
    p = subprocess.Popen(shlex.split("java -jar SentiStrength.jar stdin exclamations2 noIgnoreBoosterWordsAfterNegatives sentidata C:/SentStrength_Data/"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #communicate via stdin the string to be rated. Note that all spaces are replaced with +
    stdout_text, stderr_text = p.communicate(text.replace(" ","+"))
    #remove the tab spacing between the positive and negative ratings. e.g. 1    -5 -> 1-5
    stdout_text = stdout_text.rstrip().split("\t")
    return [int(s) for s in stdout_text][:2]

'''Make category hierarchy for Wordnet Affect hierarchy xml'''
def make_wn_affect_tree():
    affect_hierarchy_xml = minidom.parse(Properties.WN_affect_hierarchy_filename)
    categories_list = affect_hierarchy_xml.getElementsByTagName('categ') 
    for cat in categories_list:
        name = cat.attributes['name'].value
        if name == "root":
            root = AffectNode(name)
            affect_tree = AffectTree(root)
        else:
             parent_name = cat.attributes['isa'].value
             parent = affect_tree.find_node(parent_name)
             node = AffectNode(name, parent)
    return affect_tree  

        

''' Read synsets from WN Affect xml file'''
def read_wn_affect_noun_synsets():
    affect_synsets_xml = minidom.parse(Properties.WN_affect_synsets_filename)
    noun_synsets_list = affect_synsets_xml.getElementsByTagName('noun-syn') 
    return  noun_synsets_list # + adj_synsets_list + verb_synsets_list + adv_synsets_list


def read_wn_affect_not_noun_synsets():
    affect_synsets_xml = minidom.parse(Properties.WN_affect_synsets_filename)
    adj_synsets_list = affect_synsets_xml.getElementsByTagName('adj-syn')    
    verb_synsets_list = affect_synsets_xml.getElementsByTagName('verb-syn')  
    adv_synsets_list = affect_synsets_xml.getElementsByTagName('adv-syn') 
    return  adj_synsets_list + verb_synsets_list + adv_synsets_list

    
def make_wn_affect_dictionary():
    wn_affect_nouns = read_wn_affect_noun_synsets()
    wn_affect_other_pos = read_wn_affect_not_noun_synsets()
    noun_dict = {c.attributes['id'].value: c.attributes['categ'].value for c in wn_affect_nouns}
    other_pos_dict = {c.attributes['id'].value: noun_dict[c.attributes['noun-id'].value] for c in wn_affect_other_pos}
    noun_dict.update(other_pos_dict)
    return noun_dict


'''Return words fitting given emotion from Wordnet Affect '''
def find_affect_synsets_for_emotion(emotion_name, wn_affect_tree):
    with open(wn_id_dict_filename, 'rb') as handle:
        wn_id_dict = pickle.loads(handle.read())
    wn_affect_syns = make_wn_affect_dictionary()
    affect_categories = wn_affect_tree.find_offsprings(emotion_name)
    affect_synsets = [wn_id_dict[int(syn_id[2:])] for syn_id in wn_affect_syns if wn_affect_syns[syn_id] in affect_categories]
    return affect_synsets


'''Calculating words arousal'''
def calculate_arousal(text):
    arousal = 0
    if "!" in text:
        arousal+=1
    if "!!" in text:
        arousal+=2
    if "..." in text:
        arousal-=1
    words = nltk.word_tokenize(text)
    for w in words:
        if w.isupper():
            arousal+=1
    words_arousal = [Utils.anew_list[string.lower(w)][1]-4 for w in words if w in Utils.anew_list]#get anew arousal for words
    average= lambda l:sum(l) / float(len(l))
    if len(words_arousal)>0:
        arousal+= average(words_arousal)
    return round(arousal)
    

   

emotions_dict = {"joy":(4.60, 3.22), "love":(4.72, 2.44), "affection":(4.39, 2.21), "liking":(3.52, 2.63), "enthusiasm": (4.17, 3.38), "security":(3.28, 0.22), "gratitude": (2.89, 0.34), "self-pride": (3.00, 1.83), "calmness": (2.73, -0.4), "positive-hope":(3.05, 1.44), "negative-fear":(-1.24, 2.96), "sadness" :(-1.79, 1.21), "shame":(-1.87, 2.33),"anger":(-1.66, 3.63), "hate":(1.88, 2.95),"compassion":(1.33, 1.03), "humility":(-2.1, 2.97), "despair":(-1.57, 1.68), "anxiety":(-1.23, 2.72), "apathy":(0.30, 0.00)}

''' Get emotion from sentiment rate'''
def get_emotion(valence, arousal):
    def emotion_distance2d((v1,a1),(v2,a2)):
        return math.sqrt((v2-v1)**2+(a2-a1)**2)

    d={em:emotion_distance2d(emotions_dict[em],(valence,arousal)) for em in emotions_dict}
    emotion = min(d, key=d.get)
    return emotion

def get_emotion_distance(valence, arousal, emotion):
    def emotion_distance2d((v1,a1),(v2,a2)):
        return math.sqrt((v2-v1)**2+(a2-a1)**2)
    try:
        d= emotion_distance2d(emotions_dict[emotion],(valence,arousal))
    except:
        d=100000
    return d


