from gensim.models.fasttext import load_facebook_model, load_facebook_vectors
import fasttext.util

# stanza.download("sv")
# stemmer = SnowballStemmer("swedish")
# download('stopwords')  # Download stopwords list.
self.nlp = stanza.Pipeline("sv", processors='tokenize,lemma')


# Downloaded pre-trained embeddings will be used. 
# These are loaded into a Gensim Word2Vec model class.
fasttext.util.download_model('sv', if_exists='ignore') 
model = KeyedVectors.load_word2vec_format('../massive_data/model.txt', limit=500000, unicode_errors='ignore')
model.save('coNLL17_vectors.kv')

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

fontawesome==5.10.1.post1
pymongo==3.11.4
pymongo[srv]



        if model.get('model') == 'jaccard':
            for i, row in self.CI_currentT.iterrows():
                CI_processed = self.preprocess_texts(row['value'])
                result_jaccard_CIT_CT = self.jaccard_similarity(content_processed_titles, CI_processed)
                result_jaccard_desc = self.jaccard_similarity(content_processed_desc, CI_processed)
                result_jaccard_desc_titles = self.jaccard_similarity(content_processed_desc_titles, CI_processed)


                self.format_result_cos(row['uuid'], row['CI'], row['title'], result_jaccard_CIT_CT)
                self.format_result_cos(row['uuid'], row['CI'], row['title'], result_jaccard_desc)
                self.format_result_cos(row['uuid'], row['CI'], row['title'], result_jaccard_desc_titles)

            
            if not isinstance(self.surtitle, float) and ('Lilla Aktuellt' in self.surtitle or 'Newsreel' in self.surtitle):
                sorted_dict = sorted(self.CI_keywords_dict.items(), reverse=True, key = lambda x: x[1]['value'])
                return (sorted_dict)

            else:
                sorted_dict = sorted(self.CI_keywords_dict.items(), reverse=True, key = lambda x: x[1]['value'])
                top_candidates = []
                memory = []
                i = 0
                while len(top_candidates) < 3:
                    if (sorted_dict[i][1].get('CI')) not in memory:
                        top_candidates.append(sorted_dict[i])
                        memory.append(sorted_dict[i][1].get('CI'))
                    i += 1
                for key in sorted_dict:
                    top_id = []
                    for value in top_candidates:
                        top_id.append(value[0])
                    if(key[1].get('value') < 0.90) and (key[0] not in top_id):
                        top_candidates.append(key)

                return top_candidates

