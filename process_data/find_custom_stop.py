import pandas as pd
import re
from gensim.models.keyedvectors import KeyedVectors

import stanza
from nltk.stem import SnowballStemmer

#stanza.download("sv")
stemmer = SnowballStemmer("swedish")


ur_df = pd.read_csv("../massive_data/search_ur_cleaned.csv", engine='python')
keywords = ur_df['keywords~'].unique()
print(len(keywords))



CI = pd.read_csv('../massive_data/CI_vocab.csv')
unique_CI = CI['value'].unique()


comparison = ['hej']

def find_missing_words(domain, vector):
    word_vectors = KeyedVectors.load(f'../massive_data/{vector}')
    nlp = stanza.Pipeline("sv", processors='tokenize,lemma')
    missing_words = []
    dictionary = dict()

    for word in domain:
        result = sim(word_vectors, nlp, word, None, comparison, None, dictionary)
        if result != None:
            missing_words.append(result)

    print(dictionary)
    return missing_words

def sim(wv, nlp, word, error_term, comparison, memory, d):
    new=None
    memory = memory
    if isinstance(word, list):
        word = "".join(word)
    word = word.lower()
    word = re.sub(r"[^\w\d'\s\-]+", '', word)
    if memory:
        lemm = nlp(error_term)
        new = [error_term.lemma for sent in lemm.sentences for error_term in sent.words]
        word = word.replace(error_term, ''.join(new))

    try:
        similarity = wv.n_similarity(word.split(" "), comparison)
        if new:
            d[error_term] = ''.join(new)
        return None
    except KeyError as e:
        error_code = e.args[0].split()
        error_term = error_code[1].strip("'")

        if error_term == memory:
            return error_term
        else:
            memory = error_term
            results = sim(wv, nlp, word, error_term, comparison, memory, d)
    
    if results:
        return results
            



CI_missing_coNLL17 = find_missing_words(unique_CI, 'model.hdf5')
keywords_missing_coNLL17 = find_missing_words(keywords, 'model.hdf5')
CI_unique_list = (list(set(CI_missing_coNLL17)))
keywords_unique_list = (list(set(keywords_missing_coNLL17)))

print(CI_unique_list)
print(keywords_unique_list)
print(len(CI_unique_list))
print(len(keywords_unique_list))


# missing_wiki = find_missing_words('wiki_vectors.kv')
# print(missing_wiki)
# print(len(missing_wiki))

# missing_vec = find_missing_words('vectors.kv')
# print(missing_vec)
# print(len(missing_vec))

# missing_cc = find_missing_words('cc_vectors.kv')
# print(missing_cc)
# print(len(missing_cc))

