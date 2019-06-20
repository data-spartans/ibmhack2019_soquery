from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from base import Query

class QueryGenerator():
    def __init__(self, base_query=""):
        self.base_query = base_query

    def tokenize(self, text):
        sentences = sent_tokenize(text)
        result = []
        for s in sentences:
            result.append(word_tokenize(s))
        return result

    def remove_punctuations(self, tokenized_text):
        result = []
        for s in tokenized_text:
            new_sent = []
            for word in s:
                if len(word) > 1 or str.isalnum(word):
                    new_sent.append(word)
            result.append(new_sent)
        return result

    def remove_stopwords(self, tokenized_text):
        result = []
        stop_words = set(stopwords.words("english"))
        for s in tokenized_text:
            new_sent = []
            for word in s:
                if word not in stop_words:
                    new_sent.append(word)
            result.append(new_sent)
        return result

    def detokenize(self, tokenized_text):
        return ' '.join([' '.join(sent) for sent in tokenized_text])

    def generate(self):
        queries = []
        queries.append(Query(intitle=self.base_query))
        tokenized_base = self.tokenize(self.base_query)
        no_puncts = self.remove_punctuations(tokenized_base)
        no_stopwords = self.remove_stopwords(no_puncts)
        queries.append(Query(intitle = self.detokenize(no_puncts)))
        queries.append(Query(intitle = self.detokenize(no_stopwords)))
        return queries

if __name__ == '__main__':
    q = input("Enter your query: ")
    qgen = QueryGenerator(q)
    alternates = qgen.generate()
    for q in alternates:
        print(q.intitle)

