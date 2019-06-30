import urllib

from flask import Flask, render_template, request, url_for

from api_handling import SOHandler
from query_gen import QueryGenerator
from ranking import overall_confidence
from utils import color_for_confidence

qgen = QueryGenerator()
so_handler = SOHandler()

app = Flask(__name__)

@app.route("/")
def home(not_found=False):
    return render_template('home.html', not_found=not_found)

@app.route("/search")
def search():
    query = request.args.get('query')
    query_list = qgen.generate(query)
    answers = so_handler.get_answers(query_list)
    for answer in answers:
        answer.confidence = overall_confidence(query, answer)
    answers = sorted(answers, key=lambda x: x.confidence, reverse = True)
    if len(answers) == 0:
        return home(not_found=True)
    if len(answers) > 5:
        answers = answers[:5]
    for answer in answers:
        answer.fetch_body()
    colors = [color_for_confidence(x.confidence, 
                                    thresh=700, 
                                    c1=(204, 0, 0), 
                                    c2=(0, 180, 204)) for x in answers]
    data = [(x, y) for x, y in zip(answers, colors)]
    return render_template('search.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
