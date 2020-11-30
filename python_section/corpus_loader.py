from sklearn import feature_extraction

import pickle
import os


class CorpusLoader(object):

    def __init__(self, datasetFile, textDir):
        self.datasetFile = datasetFile
        self.textDir = textDir

    def load_folder_list(self, path=''):
        return [os.path.join(path, o) for o in os.listdir(path) if os.path.isdir(os.path.join(path, o))]

    def TrainVocab(self):
        caption_dir = os.path.join(self.datasetFile, self.textDir)
        full_corpus_file = os.path.join(caption_dir, 'full_corpus.txt')

        vec_name = 'vectorizer.pickle'
        vec_file = os.path.join(caption_dir, vec_name)
        if os.path.isfile(vec_file):
            vec = pickle.load(open(vec_file, 'rb'))
            print('Pickle file exists.')
            return vec

        captions_corpus = []
        with open(full_corpus_file, "r") as f:
            captions_corpus = f.readlines()
            captions_corpus = [s.replace('\n', '') for s in captions_corpus]

        vectorizer = feature_extraction.text.TfidfVectorizer(stop_words='english', max_features=1024, binary=False)
        vectorizer.fit(raw_documents=captions_corpus)

        pickle.dump(vectorizer, open(vec_file, 'wb'))
        print('Pickle file created.')

        return vectorizer
