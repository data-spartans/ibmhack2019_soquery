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
    words1 = word_tokenize(t1)
    words2 = word_tokenize(t2)
    
    words1 = [ps.stem(w) for w in words1]
    words2 = [ps.stem(w) for w in words2]

    set1 = set(words1)
    set2 = set(words2)

    return len(set1.intersection(set2))/len(set1.union(set2))


if __name__ == '__main__':
    t1 = input('Enter first sentence: ')
    t2 = input('Enter second sentence: ')

    print('Similarity:', jaccard_similarity(t1, t2))


