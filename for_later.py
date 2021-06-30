from gensim.models.fasttext import load_facebook_model, load_facebook_vectors
import fasttext.util


# Downloaded pre-trained embeddings will be used. 
# These are loaded into a Gensim Word2Vec model class.
fasttext.util.download_model('sv', if_exists='ignore') 
model = KeyedVectors.load_word2vec_format('../massive_data/model.txt', limit=500000, unicode_errors='ignore')
model.save('coNLL17_vectors.kv')