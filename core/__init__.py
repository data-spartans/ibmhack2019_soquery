import os, nltk

file_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(file_dir, 'nltk_data')
nltk_packages = [{'name': 'stopwords', 'path': 'corpora/stopwords'},
                 {'name': 'punkt', 'path': 'tokenizers/punkt'}]
nltk.data.path.append(data_dir)

for package in nltk_packages:
    try:
        nltk.data.find(package['path'])
    except LookupError:
        print('-> Installing NLTK package:', package)
        nltk.download(package, download_dir=data_dir)
