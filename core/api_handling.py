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
        answer_ids = set()
        api_url = 'https://api.stackexchange.com/2.2/questions/'
        query_options1 = '/answers?order=desc&sort=votes&site=stackoverflow'
        query_options2 = '/answers?order=desc&sort=activity&site=stackoverflow'
        # ^ We need to to get sort in different ways to prevent outliers
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

        final_url1 = api_url + ids + query_options1 + key_param
        final_url2 = api_url + ids + query_options2 + key_param
        req1 = requests.get(final_url1)
        req2 = requests.get(final_url2)

        if req1.status_code == 200:
            data1 = req1.json()
            for item in data1['items']:
                if item['answer_id'] not in answer_ids:
                    answer_ids.add(item['answer_id'])

                    # remove outlier scores:
                    if int(item['score']) > 5000:
                        item['score'] = 5000

                    answers.append(CandidateAnswer(
                                        info = item, 
                                        question_title = qindex[item['question_id']][0].title,
                                        question_link = qindex[item['question_id']][0].link,
                                        relevance = qindex[item['question_id']][1]
                                   ))

        if req2.status_code == 200:
            data2 = req2.json()
            for item in data2['items']:
                if item['answer_id'] not in answer_ids:
                    answer_ids.add(item['answer_id'])

                    # remove outlier scores:
                    if int(item['score']) > 5000:
                        item['score'] = 5000

                    answers.append(CandidateAnswer(
                                        info = item, 
                                        question_title = qindex[item['question_id']][0].title,
                                        question_link = qindex[item['question_id']][0].link,
                                        relevance = qindex[item['question_id']][1]
                                   ))
        return answers
