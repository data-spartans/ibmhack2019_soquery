'''
Query Generator Module
----------------------

Provides a single class, QueryGenerator, whose object holds all the necessary
imports and functions for generating relevant queries for the API.
'''

from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize

from .base import Query


class QueryGenerator():
    ''' 
    This class provides methods to generate relevant alternative queries from
    a given query.

    The main function is generate() which takes as input a query, and outputs a 
    list of Query objects that could fetch a good answer.
    '''

    def __init__(self):
        pass

    def tokenize(self, text):
        return word_tokenize(text)

    def detokenize(self, tokenized_text):
        return ' '.join(tokenized_text)

    def remove_punctuations(self, tokenized_text):
        '''
        Removes punctutions from list of tokens.
        '''
        result = []
        for word in tokenized_text:
            if len(word) > 1 or str.isalnum(word):
                result.append(word)
        return result

    def remove_stopwords(self, tokenized_text):
        '''
        Removes stopwords from list of tokens.
        '''
        result = []
        stop_words = set(stopwords.words("english"))
        for word in tokenized_text:
            if word not in stop_words:
                result.append(word)
        return result

    def is_only_noun_verb(self, word):
        '''
        Uses wordnet to tell if the word can only be a verb or noun.
        '''
        syns = wordnet.synsets(word)
        if not syns:        # when word is proper noun
            return True
        for syn in syns:
            if syn.pos() != 'n' and syn.pos() != 'v':
                return False
        return True

    def is_noun(self, word):
        '''
        Uses wordnet to tell if the word may be a noun.
        '''
        syns = wordnet.synsets(word)
        if not syns:        # when word is proper noun
            return True
        for syn in syns:
            if syn.pos() == 'n':
                return True
        return False

    def sure_nouns_and_verbs(self, tokenized_text):
        '''
        Picks and returns only those tokens that are definitely either noun or verbs.
        '''
        result = []
        for word in tokenized_text:
            if self.is_only_noun_verb(word):
                result.append(word)
        return result

    def nouns(self, tokenized_text):
        '''
        Picks and returns only those tokens that may be nouns.
        '''
        result = []
        for word in tokenized_text:
            if self.is_noun(word):
                result.append(word)
        return result

    def generate(self, base_query):
        q_strs = set()
        q_strs.add(base_query)

        tokenized_base = self.tokenize(base_query)
        no_puncts = self.remove_punctuations(tokenized_base)
        no_stopwords = self.remove_stopwords(no_puncts)
        only_noun_verbs = self.sure_nouns_and_verbs(no_stopwords)
        only_nouns = self.nouns(only_noun_verbs)

        q_strs.add(self.detokenize(no_puncts))
        q_strs.add(self.detokenize(no_stopwords))
        q_strs.add(self.detokenize(no_stopwords))
        q_strs.add(self.detokenize(only_noun_verbs))
        q_strs.add(self.detokenize(only_nouns))

        queries = []
        for s in q_strs:
            if s != "":
                queries.append(Query(q=s))
        if only_nouns != "":
            queries.append(Query(title=only_nouns))
        return queries
