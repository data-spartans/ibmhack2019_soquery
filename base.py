class Query():
    def __init__(self, intitle="", tags="", sortby=""):
        self.intitle = intitle
        self.tags = tags
        self.sortby = sortby

class CandidateAnswer():
    def __init__(self, ID=None, question_id=None, question_text = "", \
                 accepted=False, votes=None):
        self.question = question
        self.votes = votes
        self.accepted = accepted
        self.ID = ID
        self.confidence = 0

