from html2text import HTML2Text
import stackexchange

class Query():
    def __init__(self, q="", title="", tagged=None, sort='relevance'):
        self.q = q
        self.title = title
        self.tagged = tagged
        self.sort = sort

class CandidateAnswer():
    def __init__(self, info={}, question_title=None, question_link=None, relevance=None):
        self.info = info
        self.confidence = 0
        self.body = ''
        self.question_title = question_title
        self.question_link = question_link
        self.relevance = relevance

    def fetch_body(self):
        ''' 
        Fetch body of answer on demand, to save bandwidth
        '''
        so = stackexchange.Site(stackexchange.StackOverflow)
        self.body = so.answer(self.info['answer_id'], body=True).body
        
    def to_markdown(self):
        h = HTML2Text()
        return h.handle(self.body)

