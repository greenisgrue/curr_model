import pandas as pd
from gensim.models.keyedvectors import KeyedVectors
import re
from nltk.corpus import stopwords
from nltk import download
import stanza

from process_data.dictionary import get_dictionary

class W2v():
    def __init__(self):
        # stanza.download("sv")
        # stemmer = SnowballStemmer("swedish")
        # download('stopwords')  # Download stopwords list.
        self.ur_df = pd.read_csv("massive_data/stored_data/search_ur_cleaned.csv", engine='python')
        self.word_vectors = KeyedVectors.load('massive_data/word_vector_models/coNLL17_vectors.kv')
        self.nlp = stanza.Pipeline("sv", processors='tokenize,lemma')

        self.dictionary = get_dictionary()

    def generate_id(self):
        random_row = self.ur_df.sample()
        return random_row.iloc[0]['~uid'].strip('~')

    def find_CI(self, chosen_uid):
        chosen_uid = f'~{chosen_uid}'
        self.chosen_content = self.ur_df[self.ur_df['~uid'] == chosen_uid]

        self.content_id = chosen_uid.strip('~')
        self.title = self.chosen_content.iloc[0]['title']
        self.surtitle = self.chosen_content.iloc[0]['surtitle']
        self.thumbnail = self.chosen_content.iloc[0]['thumbnail']
        self.keywords = self.chosen_content.iloc[0]['keywords~']
        self.keywords = self.keywords.strip(',~')
        self.description = self.chosen_content.iloc[0]['description']
        self.subject = self.chosen_content.iloc[0]['subject'] 
        self.audience = self.chosen_content.iloc[0]['audience']
        self.media_type = self.chosen_content.iloc[0]['streaming_format']

        print(self.content_id)
        CI = pd.read_csv('massive_data/stored_data/CI_vocab.csv')
        CIT = pd.read_csv('massive_data/stored_data/CI_vocab_including_titles.csv')
        if not isinstance(self.surtitle, float):
            if 'Lilla Aktuellt' in self.surtitle:
                self.CI_current = CI[CI['uuid'] == '51e34da1-0e1d-11eb-b4ba-0ae95472d63c']
                self.CI_currentT = CIT[CIT['uuid'] == '51e34da1-0e1d-11eb-b4ba-0ae95472d63c']
        
            elif 'Newsreel' in self.surtitle and self.audience == 'Grundskola 4-6':
                self.CI_current = CI[(CI['uuid'] == '35518dcf-0a14-11eb-b4ba-0ae95472d63c') | (CI['uuid'] == '3e8c4968-0a14-11eb-b4ba-0ae95472d63c') | (CI['uuid'] == '0c60d903-0a14-11eb-b4ba-0ae95472d63c') | (CI['uuid'] == '1aa25dc9-0a14-11eb-b4ba-0ae95472d63c')]
                self.CI_currentT = CIT[(CIT['uuid'] == '35518dcf-0a14-11eb-b4ba-0ae95472d63c') | (CIT['uuid'] == '3e8c4968-0a14-11eb-b4ba-0ae95472d63c') | (CIT['uuid'] == '0c60d903-0a14-11eb-b4ba-0ae95472d63c') | (CIT['uuid'] == '1aa25dc9-0a14-11eb-b4ba-0ae95472d63c')]
        
            elif 'Newsreel' in self.surtitle and self.audience == 'Grundskola 7-9':
                self.CI_current = CI[(CI['uuid'] == 'ee776597-0a14-11eb-b4ba-0ae95472d63c') | (CI['uuid'] == 'f265d641-0a14-11eb-b4ba-0ae95472d63c') | (CI['uuid'] == '00be6ce6-0a15-11eb-b4ba-0ae95472d63c') | (CI['uuid'] == '9fdfda18-0a14-11eb-b4ba-0ae95472d63c')]
                self.CI_currentT = CIT[(CIT['uuid'] == 'ee776597-0a14-11eb-b4ba-0ae95472d63c') | (CIT['uuid'] == 'f265d641-0a14-11eb-b4ba-0ae95472d63c') | (CIT['uuid'] == '00be6ce6-0a15-11eb-b4ba-0ae95472d63c') | (CIT['uuid'] == '9fdfda18-0a14-11eb-b4ba-0ae95472d63c')]

        
        self.CI_current = CI[CI['subject'].isin(self.subject.split(', ')) & CI['audience'].isin(self.audience.split(', '))]
        self.CI_currentT = CIT[CIT['subject'].isin(self.subject.split(', ')) & CIT['audience'].isin(self.audience.split(', '))] 

        if self.media_type == 'video' or self.media_type == 'audio' or isinstance(self.media_type, float):
            self.CI_current = self.CI_current.drop(self.CI_current[self.CI_current.title == 'Texter'].index)
            self.CI_currentT = self.CI_currentT.drop(self.CI_currentT[self.CI_currentT.title == 'Texter'].index)


    def preprocess_texts(self, text):
        stop_words = stopwords.words('swedish')
        text = text.lower()
        text = re.sub(r"[^\w\s-]+", '', text)
        text = ' '.join([self.dictionary.get(i, i) for i in text.split()])
        text = " ".join([w for w in text.split() if w not in stop_words])

        for word in text.split():
            era = word
            if word == '800-1500':
                era = 'medeltiden'
            elif word == '1500-1800':
                era = 'renässansen'
            elif '-' in word and len(word) > 1:
                years = word.split('-')
                if years[0].isnumeric() and years[1].isnumeric():
                    era = [self.find_era(years[0]), self.find_era(years[1])]
                    era = ' '.join(era)
                elif years[0].isnumeric() and not (years[1].isnumeric()):
                    era = self.find_era(years[0])
            text = text.replace(word, era)
        return text.split(" ")

    def find_era(self, year):
        era = year
        if 800 <= int(year) <= 1459:
            era = 'medeltiden'
        elif 1500 <= int(year) <= 1759:
            era = 'renässansen'
        elif 1800 <= int(year) <= 1859 and int(year) != 1850:
            era = 'industrialiseringen'
        return era  
 
    def jaccard_similarity(self, query, document):
        #query = query.split()
        #document = document.split()
        intersection = set(query).intersection(set(document))
        union = set(query).union(set(document))
        return len(intersection)/len(union)

    def cos_sim(self, keywords, CI_doc):         
        try:
            similarity = self.word_vectors.n_similarity(keywords, CI_doc)
            return similarity
        except KeyError as e:
            error_code = e.args[0].split()
            error_term = error_code[1].strip("'")
            if error_term in CI_doc:
                CI_doc.remove(error_term)
            if error_term in keywords:
                keywords.remove(error_term) 
            results = self.cos_sim(keywords, CI_doc)
        if results: 
            return results

    def wmd(self, keywords, CI_doc):
        try:
            distance = self.word_vectors.wmdistance(keywords, CI_doc)
            return distance
        except KeyError as e:
            error_code = e.args[0].split()
            error_term = error_code[1].strip("'")
            if error_term in CI_doc:
                CI_doc.remove(error_term)
            if error_term in keywords:
                keywords.remove(error_term) 
            results = self.wmd(keywords, CI_doc)
        if results: 
            return results
    
    def format_result_cos(self, uid, CI, title, result):
        formatted_string = "{:.3f}".format(result)
        result = float(formatted_string)
        current_CI_ID = self.CI_keywords_dict.get(uid)
        if current_CI_ID is None or current_CI_ID.get('value') < result:
            self.CI_keywords_dict[uid] = {'CI': CI, 'title':  title, 'value': result}

    def format_result_wmd(self, uid, CI, title, result):
        formatted_string = "{:.3f}".format(result)
        result = float(formatted_string)
        current_CI_ID = self.CI_keywords_dict.get(uid)
        if current_CI_ID is None or current_CI_ID.get('value') < result:
            self.CI_keywords_dict[uid] = {'CI': CI, 'title':  title, 'value': result}

    def predict_CI(self, model, uid):
        self.find_CI(uid)
            
        self.CI_keywords_dict = {}


        if not isinstance(self.surtitle, float):
            keywords_titles = self.keywords + ', ' + self.title + ', ' + self.surtitle

        else:
            keywords_titles = self.keywords + ', ' + self.title

        content_processed_titles = self.preprocess_texts(keywords_titles)
        content_processed = self.preprocess_texts(self.keywords)

        if model.get('model') == 'jaccard':
            for i, row in self.CI_currentT.iterrows():
                CI_processed = self.preprocess_texts(row['value'])
                result_jaccard_CIT_CT = self.jaccard_similarity(content_processed_titles, CI_processed)
                self.format_result_cos(row['uuid'], row['CI'], row['title'], result_jaccard_CIT_CT)
            
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


        if model.get('model') == 'opti_cos':
           for i, row in self.CI_currentT.iterrows():
                CI_processed = self.preprocess_texts(row['value'])
                result_cos_CIT_CT = self.cos_sim(content_processed_titles, CI_processed)
                result_cos_CIT = self.cos_sim(content_processed, CI_processed)
                
                self.format_result_cos(row['uuid'], row['CI'], row['title'], result_cos_CIT_CT)
                self.format_result_cos(row['uuid'], row['CI'], row['title'], result_cos_CIT)

        if model.get('model') == 'opti_cos':
            for i, row in self.CI_current.iterrows(): 
                CI_processed = self.preprocess_texts(row['value'])
                result_cos_CT = self.cos_sim(content_processed_titles, CI_processed)
                result_cos = self.cos_sim(content_processed, CI_processed)
                
                self.format_result_cos(row['uuid'], row['CI'], row['title'], result_cos_CT)
                self.format_result_cos(row['uuid'], row['CI'], row['title'], result_cos)
            
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
                    if(key[1].get('value') > 0.85) and (key[0] not in top_id):
                        top_candidates.append(key)
                return top_candidates


        if model.get('model') == 'opti_wmd':
           for i, row in self.CI_currentT.iterrows():
                CI_processed = self.preprocess_texts(row['value'])
                result_wmd_CIT_CT = self.wmd(content_processed_titles, CI_processed)
                result_wmd_CIT = self.wmd(content_processed, CI_processed)
                 
                dict_wmd_CIT_CT = self.format_result_wmd(row['uuid'], row['CI'], row['title'], result_wmd_CIT_CT)
                dict_wmd_CIT = self.format_result_wmd(row['uuid'], row['CI'], row['title'], result_wmd_CIT)

        if model.get('model') == 'opti_wmd':
            for i, row in self.CI_current.iterrows():
                CI_processed = self.preprocess_texts(row['value'])
                result_wmd_CT = self.wmd(content_processed_titles, CI_processed)
                result_wmd = self.wmd(content_processed, CI_processed)
                
                dict_wmd_CT = self.format_result_wmd(row['uuid'], row['CI'], row['title'], result_wmd_CT)
                dict_wmd = self.format_result_wmd(row['uuid'], row['CI'], row['title'], result_wmd)
            
        
            if not isinstance(self.surtitle, float) and ('Lilla Aktuellt' in self.surtitle or 'Newsreel' in self.surtitle):
                sorted_dict = sorted(self.CI_keywords_dict.items(), reverse=False, key = lambda x: x[1]['value'])
                return (sorted_dict)

            else:
                sorted_dict = sorted(self.CI_keywords_dict.items(), reverse=False, key = lambda x: x[1]['value'])
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

        if model.get('model') == 'wmd' or model.get('model') == 'cos':
            if model.get('CI_parent'):
                for i, row in self.CI_currentT.iterrows():
                    CI_processed = self.preprocess_texts(row['value'])
                    if model.get('content_title'):
                        if model.get('model') == 'wmd':
                            result = self.wmd(content_processed_titles, CI_processed)
                        elif model.get('model') == 'cos':
                            result = self.cos_sim(content_processed_titles, CI_processed)
                    else:
                        if model.get('model') == 'wmd':
                            result = self.wmd(content_processed, CI_processed)
                        elif model.get('model') == 'cos':
                            result = self.cos_sim(content_processed, CI_processed)
                    formatted_string = "{:.3f}".format(result)
                    result = float(formatted_string)
                    self.CI_keywords_dict[row['uuid']] = {'CI': row['CI'], 'title':  row['title'], 'value': result}
            else:
                for i, row in self.CI_current.iterrows():
                    CI_processed = self.preprocess_texts(row['value'])
                    if model.get('content_title'):
                        if model.get('model') == 'wmd':
                            result = self.wmd(content_processed_titles, CI_processed)
                        elif model.get('model') == 'cos':
                            result = self.cos_sim(content_processed_titles, CI_processed)
                    else:
                        if model.get('model') == 'wmd':
                            result = self.wmd(content_processed, CI_processed)
                        elif model.get('model') == 'cos':
                            result = self.cos_sim(content_processed, CI_processed)
                    formatted_string = "{:.3f}".format(result)
                    result = float(formatted_string)
                    self.CI_keywords_dict[row['uuid']] = {'CI': row['CI'], 'title':  row['title'], 'value': result}


        if model.get('model') == 'wmd':
            if not isinstance(self.surtitle, float) and ('Lilla Aktuellt' in self.surtitle or 'Newsreel' in self.surtitle):
                sorted_dict = sorted(self.CI_keywords_dict.items(), reverse=False, key = lambda x: x[1]['value'])
                return (sorted_dict)

            else:
                sorted_dict = sorted(self.CI_keywords_dict.items(), reverse=False, key = lambda x: x[1]['value'])
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

        elif model.get('model') == 'cos':
            if not isinstance(self.surtitle, float) and ('Lilla Aktuellt' in self.surtitle or 'Newsreel' in self.surtitle):
                sorted_dict = sorted(self.CI_keywords_dict.items(), reverse=True, key = lambda x: x[1]['value'])
                return (sorted_dict)

            else:
                sorted_dict = sorted(self.CI_keywords_dict.items(), reverse=True , key = lambda x: x[1]['value'])
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
                    if(key[1].get('value') > 0.85) and (key[0] not in top_id):
                        top_candidates.append(key) 
                return top_candidates 








