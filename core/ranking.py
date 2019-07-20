from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

def jaccard_similarity(t1, t2):
    '''
    Finds similarity between two strings as the (size of intersection)/(size of union)

    Returns similarity measure between 0 and 1
    '''
    # First stem the words in the strings, 
    # then convert to set and take intersection
    ps = PorterStemmer()
    words1 = word_tokenize(t1.lower())
    words2 = word_tokenize(t2.lower())
    
    words1 = [ps.stem(w) for w in words1]
    words2 = [ps.stem(w) for w in words2]

    set1 = set(words1)
    set2 = set(words2)

    return len(set1.intersection(set2))/len(set1.union(set2))

def overall_confidence(query, candidate):
    '''
    Returns overall confidence in an answer based on a (currently ad-hoc) formula. The main factors that influence the confidence are:

        * The similarity of its question to original query
        * How far up it's question is in the search results (i.e relevance)
        * The answer's score/upvotes
        * Whether the answer is accepted

    Basically, the answer's score and acceptance act as weights for the similarity + relevance.
    '''
    sim = jaccard_similarity(query, candidate.question_title)
    rel = candidate.relevance
    scr = int(candidate.info['score'])
    acc = None

    # we take acceptance of answer being equivalent to 50 upvotes
    if candidate.info['is_accepted'] == 'true': acc = 50
    else: acc = 0
    
    # similarity to original query is highly valued
    return (scr + acc) * (sim + 1/rel) + 10000 * sim

