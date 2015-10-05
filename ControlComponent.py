import en, nltk
from Experts.GeneratingExperts import WordNetExpert, EmotionExpert, CollocationExpert
from Experts.EvaluationExperts import EvaluationExpert, SyllablesExpert, DiversityExpert, RhymesExpert
from Experts.PoemMakingExperts.GrammarExperts import ApostropheExpert, ComparisonExpert, EpithetExpert, MetaphoreExpert, OxymoronExpert, RhetoricalExpert, SentenceExpert
#from Experts.PoemMakingExperts.NGramExperts import AnaphoraExpert, EpiphoraExpert, NGramExpert
from Experts.PoemMakingExperts import ExclamationExpert, OverflowExpert, RepetitionExpert
from Experts.KeyWordsExpert import *
from Blackboard import *
from Properties import text_dir
from random import randint
import logging



class ControlComponent(object):
    """Control of experts priorities and actions, ending process"""

    def __init__(self, blackboard = None):
        logging.basicConfig(filename='poem.log',level=logging.INFO)
        #text_nr = randint(0,8)
        text_file = text_dir+".txt"
        print "Making blackboard..."
        self.blackboard = Blackboard(text_file,[8,8,8,8,0,8,8,8,8])
        print self.blackboard.text
        logging.info(self.blackboard.text)


    def _init_experts(self):
        self.keyword = KeyWordsExpert(self.blackboard)
        self.keyword.get_keyphrases()

        ###generating experts ###
        print "Words generating experts..."
        self.word_generating_experts = []
        self.word_generating_experts.append(self.keyword)
        self.word_generating_experts.append(WordNetExpert.WordNetExpert(self.blackboard))
        self.word_generating_experts.append(EmotionExpert.EmotionExpert(self.blackboard))
        self.word_generating_experts.append(CollocationExpert.CollocationExpert(self.blackboard))

        
        ### Poem making experts... ###
        print "Poem making experts..."
        self.poem_making_experts = []
        self.poem_making_experts.append(self.keyword)
        self.poem_making_experts.append(EpithetExpert.EpithetExpert(self.blackboard))
        self.poem_making_experts.append(ApostropheExpert.ApostropheExpert(self.blackboard))
        self.poem_making_experts.append(SentenceExpert.SentenceExpert(self.blackboard, self.blackboard.tense, self.blackboard.person))
        self.poem_making_experts.append(ComparisonExpert.ComparisonExpert(self.blackboard))
        self.poem_making_experts.append(ExclamationExpert.ExclamationExpert(self.blackboard))
       # self.poem_making_experts.append(NGramExpert.NGramExpert(self.blackboard))
        self.poem_making_experts.append(RepetitionExpert.RepetitionExpert(self.blackboard))
        self.poem_making_experts.append(OverflowExpert.OverflowExpert(self.blackboard))
        self.poem_making_experts.append(RhetoricalExpert.RhetoricalExpert(self.blackboard))
        self.poem_making_experts.append(MetaphoreExpert.MetaphoreExpert(self.blackboard))
        self.poem_making_experts.append(OxymoronExpert.OxymoronExpert(self.blackboard))

       # self.anaphora = AnaphoraExpert.AnaphoraExpert(self.blackboard)
       # self.epiphora = EpiphoraExpert.EpiphoraExpert(self.blackboard)
        print "Control experts..."
        self.syllables = SyllablesExpert.SyllablesExpert(self.blackboard)
        self.diversity = DiversityExpert.DiversityExpert(self.blackboard)
        self.rhymes = RhymesExpert.RhymesExpert(self.blackboard)
        self.emotion = EmotionExpert.EmotionExpert(self.blackboard)

    def _evaluate_pools_inspiration(self):
        ### estimating words for pool... ###
        for pool in self.blackboard.pool_of_ideas.values():
            print
            print pool.title
            ### estimating pool of words ###
            print "Estimating words..."
        
            for wg_e in self.word_generating_experts:
                try:
                    inspirations = wg_e.estimate_ideas_size(pool)
                    pool.inspiration += inspirations
                except:
                    print "Error: couldn't estimate words by expert: ", wg_e.name
        ### select best pool...  ###
        print "Evaluation expert..."
        self.evaluation = EvaluationExpert.EvaluationExpert(self.blackboard)
        pool = self.evaluation.select_pool()
        print "Generating poem for title: ", pool.title
        self.blackboard.pool = PoolOfIdeas(pool.title,self.blackboard.syllables, pool.sentences)


    def _generate_pool(self):
        ### generate words... ###
        for wg_e in self.word_generating_experts:
            try:
                wg_e.generate_words(self.blackboard.pool)
            except:
                print "Error: couldn't generate words by expert: ", wg_e.name

        print self.blackboard.pool
        logging.info(self.blackboard.pool)

        ### generating phrases... ###
        if len(self.blackboard.pool.nouns)>0:
            for line in range(len(self.blackboard.syllables)):
                if line > 0:
                    ### making phrases ###
                    print "Making phrases for line "+str(line)
                   # if len(self.blackboard.pool.next_line)>0:
                    #    self.blackboard.pool.poem.append(self.blackboard.pool.next_line)
                   # else:
                       # self.anaphora.add_anaphora(self.blackboard.pool)
                      #  self.epiphora.add_epiphora(self.blackboard.pool)
                    for i in range(5):
                        for e in self.poem_making_experts:
                            try:
                                e.add_phrase(self.blackboard.pool)
                                    
                            except:
                                print "Warning - couldn't add phrase by expert: ", e.name
                        logging.info(self.blackboard.pool.phrases_dict)
                        logging.info("Number of phrases: "+str(len(self.blackboard.pool.phrases_dict)))
                        
                        
                    ### selection...###
                    
                    self.rhymes.select_phrases(self.blackboard.pool, line)
                    logging.info("Rhymes selection: "+str(len(self.blackboard.pool.phrases_dict)) )
                    logging.info( self.blackboard.pool.phrases_dict)
                    
                    self.syllables.select_phrases(self.blackboard.pool, line)
                    logging.info("Syllables selection: "+str(len(self.blackboard.pool.phrases_dict) ))
                    logging.info( self.blackboard.pool.phrases_dict)
                    
                    self.emotion.select_phrases(self.blackboard.pool, line)                   
                    logging.info("Emotion selection: "+str(len(self.blackboard.pool.phrases_dict)) )
                    logging.info( self.blackboard.pool.phrases_dict)
                    poem_line = self.diversity.select_phrase(self.blackboard.pool.phrases_dict)
                    self.blackboard.pool.poem.append(poem_line)

                    ### cleaning... ###
                    self.blackboard.pool.phrases = self.blackboard.pool.next_line #overflow sentences
                    self.blackboard.pool.next_line = []
                    self.blackboard.pool.ngram_seed = []
                    self.blackboard.pool.phrases_dict = []

                elif line == 0:
                    self.blackboard.pool.poem.append([])

    def make_poem(self):
        self._init_experts()
        self._evaluate_pools_inspiration()
        self._generate_pool()        
        poem = self.blackboard.pool.str_poem()
        logging.info(self.blackboard.pool.print_experts())
        print poem
        logging.info(poem)
        print



