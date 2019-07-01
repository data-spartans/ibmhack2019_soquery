import stackexchange
import requests
from .base import CandidateAnswer
from .base import Query

class SOHandler():
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.so = stackexchange.Site(stackexchange.StackOverflow, self.api_key)
        self.so.impose_throttling = True
        self.so.throttle_stop = False
        self.QS_PER_QUERY = 10         
        # ^ no of questions to consider for each query

    def search_queries(self, query_list):
        qindex = {}
        qids = set()
        questions = []
        for query in query_list:
            qs = self.so.search_advanced (
                    q = query.q,
                    title = query.title,
                    tagged = query.tagged,
                    sort = query.sort,
                    answers = 1
                 )
            cnt = 0
            for q in qs:
                cnt += 1
                if q.id not in qids:
                    qids.add(q.id)
                    questions.append(q)
                    qindex[q.id] = (q, cnt)
                if cnt == self.QS_PER_QUERY: 
                    break
        return (questions, qindex)

    def get_answers(self, query_list):
        # The current version of py-stackexchange doesn't seem 
        # to support the method that fetches answers to a question.
        # So, we need to make requests directly to the API
        answers = []
        api_url = 'https://api.stackexchange.com/2.2/questions/'
        query_options = '/answers?order=desc&sort=votes&site=stackoverflow'
        key_param = ''
        if self.api_key:
            key_param='&key=%s' % (self.api_key)

        ids = ''
        questions, qindex = self.search_queries(query_list)

        if len(questions) == 0:
            print('Error - no questions match!')
            return []

        for i, ques in enumerate(questions):
            ids += str(ques.id)
            if i < len(questions) - 1:
                ids += '%3B'

        final_url = api_url + ids + query_options + key_param
        req = requests.get(final_url)
        if req.status_code != 200:
            print(req.status_code, '- Error while fetching data!')
            return []
        data = req.json()

        for item in data['items']:
            answers.append(CandidateAnswer(
                                info = item, 
                                question_title = qindex[item['question_id']][0].title,
                                relevance = qindex[item['question_id']][1]
                           ))
        return answers
