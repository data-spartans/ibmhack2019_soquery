import os, nltk

file_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(file_dir, 'nltk_data')
nltk_packages = [{'id': 'stopwords', 'name': 'corpora/stopwords'},
                 {'id': 'punkt', 'name': 'tokenizers/punkt'}]
nltk.data.path.append(data_dir)

for package in nltk_packages:
    try:
        nltk.data.find(package['name'])
    except LookupError:
        print('-> Installing NLTK package:', package['name'])
        nltk.download(package['id'], download_dir=data_dir)
