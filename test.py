from query_gen import QueryGenerator
from api_handling import SOHandler

query = input('Enter query: ')
qgen = QueryGenerator(query)
query_list = qgen.generate()

so = SOHandler()
answers = so.get_answers(query_list)

if len(answers) > 0:
    cnt = 0
    print('---------------------------- TOP 5 ANSWERS -------------------------------')
    for answer in answers:
        print('->\tUSER ', answer.info['owner']['display_name'], 'SAYS:\n')
        answer.fetch_body()
        print(answer.to_markdown())
        print('--------------------------------------------------------------------------')
        print()
        cnt += 1
        if cnt == 5:
            break;
else:
    print('Sorry, no answers found :(')
