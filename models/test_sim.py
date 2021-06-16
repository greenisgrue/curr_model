import pandas as pd
from gensim.models.fasttext import load_facebook_model, load_facebook_vectors
from gensim.models.keyedvectors import KeyedVectors
import fasttext.util
import logging
import re
from nltk.corpus import stopwords
from nltk import download

download('stopwords')  # Download stopwords list.
stop_words = stopwords.words('swedish')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


CI1 = "Exempel på hur forntiden, medeltiden, 1500-talet, 1600-talet och 1700-talet kan avläsas i våra dagar genom traditioner, namn, språkliga uttryck, byggnader, städer och gränser."
CI2 = "Skildringar av livet förr och nu i barnlitteratur, sånger och filmer, till exempel skildringar av familjeliv och skola. Minnen berättade av människor som lever nu."
CI3 = "Hur den psykiska och fysiska hälsan påverkas av sömn, kost, motion, sociala relationer och beroendeframkallande medel. Några vanliga sjukdomar och hur de kan förebyggas och behandlas."
ur_df = pd.read_csv("../massive_data/search_ur.csv", sep='~,~', engine='python')

chosen_uid = '~208949'
chosen_content = ur_df[ur_df['~uid'] == chosen_uid]
keywords = chosen_content.iloc[0]['keywords~']
keywords = keywords.strip('~')


def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^\w\d'\s\-]+", '', text)
    text = " ".join([w for w in text.split() if w not in stop_words])
    return text


# Downloaded pre-trained embeddings will be used. 
# These are loaded into a Gensim Word2Vec model class.
#fasttext.util.download_model('sv', if_exists='ignore') 
#model = KeyedVectors.load_word2vec_format('../massive_data/model.txt', limit=500000, unicode_errors='ignore')
#model.save('coNLL17_vectors.kv')

word_vectors = KeyedVectors.load('coNLL17_vectors.kv')

# Check the "most similar words", using the default "cosine similarity" measure
result = word_vectors.most_similar(positive=['kvinna', 'kung'], negative=['man'])
most_similar_key, similarity = result[0]  # look at the first match
print(f"{most_similar_key}: {similarity:.4f}")
print(result)

# Find word that does not match
print(word_vectors.doesnt_match("tak vägg hus golv".split()))

# Find similarity between words
similarity = word_vectors.similarity('motorcykel', 'bil')
print(similarity)

# Find most similar word
result = word_vectors.similar_by_word("lampa")
most_similar_key, similarity = result[0]  # look at the first match
print(f"{most_similar_key}: {similarity:.4f}")

# Find similarity between sentences
sentence_1 = preprocess(CI2)
sentence_2 = preprocess(CI3)
print(sentence_1)
print(sentence_2)
distance = word_vectors.wmdistance(sentence_1.split(), sentence_2.split())
print('distance = %.4f' % distance)

# Find cosine similarity
similarity = word_vectors.n_similarity(sentence_1.split(), sentence_2.split())
print('Cos sim = %.4f' % similarity)


