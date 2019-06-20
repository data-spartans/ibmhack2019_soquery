class Query():
    def __init__(self, q="", title="", tagged=None, sort=None):
        self.q = q
        self.title = title
        self.tagged = tagged
        self.sort = sort

class CandidateAnswer():
    def __init__(self, ID=None, question_id=None, question_text = "", \
                 accepted=False, score=None):
        self.question = question
        self.score = score
        self.accepted = accepted
        self.ID = ID
        self.confidence = 0

