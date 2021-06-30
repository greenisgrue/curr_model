import stanza
from nltk.stem import SnowballStemmer
import re
from gensim.models.keyedvectors import KeyedVectors


# stanza.download("sv")
# stemmer = SnowballStemmer("swedish")


# text = 'Livsfrågor med betydelse för eleven, till exempel gott och ont, rätt och orätt, kamratskap, könsroller, jämställdhet och relationer.'
# text = re.sub(r'[^\w\s]', '', text)


# nlp = stanza.Pipeline("sv", processors='tokenize,lemma')
# lemm = nlp(text)
# lemmed_string = " ".join(
# [word.lemma for sent in lemm.sentences for word in sent.words])
# print(f'original: {text}')
# print(f'lem: {lemmed_string}')

# text = text.split(" ")
# stemmed_string = list(map(stemmer.stem, text))
# stemmed_string = " ".join(stemmed_string)
# print(f'stem: {stemmed_string}')


word_vectors = KeyedVectors.load('../massive_data/coNLL17_vectors.kv')

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
result = word_vectors.similar_by_word("musikinstrumentens")
most_similar_key, similarity = result[0] 
print(f"{most_similar_key}: {similarity:.4f}")


