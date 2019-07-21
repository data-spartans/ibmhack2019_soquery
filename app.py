import re
import urllib

from flask import Flask, render_template, request, url_for

from config import API_KEY
from core.api_handling import SOHandler
from core.query_gen import QueryGenerator
from core.ranking import overall_confidence
from utils import color_for_confidence

qgen = QueryGenerator()
so_handler = SOHandler(API_KEY)

app = Flask(__name__)

@app.route("/")
def home(not_found=False):
    return render_template('home.html', not_found=not_found)

@app.route("/search")
def search():
    query = request.args.get('query')
    if query == '':
        return render_template('home.html')
    n_ans = int(request.args.get('n_ans'))
    query_list = qgen.generate(query)
    try:
        answers = so_handler.get_answers(query_list)
    except:
        return render_template('home.html', error=True)
    for answer in answers:
        answer.confidence = overall_confidence(query, answer)
    answers = sorted(answers, key=lambda x: x.confidence, reverse = True)
    if len(answers) == 0:
        return render_template('home.html', not_found=True)
    if len(answers) > n_ans:
        answers = answers[:n_ans]
    for answer in answers:
        answer.fetch_body()
    colors = [color_for_confidence(x.confidence, 
                                    thresh=6000,
                                    c1=(204, 0, 0), 
                                    c2=(0, 180, 204)) for x in answers]
    data = [(x, y) for x, y in zip(answers, colors)]
    return render_template('search.html',
                            data=data,
                            sub=re.sub,
                            query=query,
                            n_ans=n_ans)

if __name__ == '__main__':
    app.run(debug=True)
