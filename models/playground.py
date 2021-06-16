import stanza
from nltk.stem import SnowballStemmer
import re

stanza.download("sv")
stemmer = SnowballStemmer("swedish")


text = 'Livsfrågor med betydelse för eleven, till exempel gott och ont, rätt och orätt, kamratskap, könsroller, jämställdhet och relationer.'
text = re.sub(r'[^\w\s]', '', text)


nlp = stanza.Pipeline("sv", processors='tokenize,lemma')
lemm = nlp(text)
lemmed_string = " ".join(
[word.lemma for sent in lemm.sentences for word in sent.words])
print(f'original: {text}')
print(f'lem: {lemmed_string}')

text = text.split(" ")
stemmed_string = list(map(stemmer.stem, text))
stemmed_string = " ".join(stemmed_string)
print(f'stem: {stemmed_string}')


