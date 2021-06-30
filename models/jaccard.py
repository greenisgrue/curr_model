import pandas as pd
from nltk.corpus import stopwords
from nltk import download
import re
import stanza
from nltk.stem import SnowballStemmer


class Jaccard():

    def __init__(self):
        #stanza.download("sv")
        #stemmer = SnowballStemmer("swedish")
        
        self.ur_df = pd.read_csv("massive_data/stored_data/search_ur.csv", sep='~,~', engine='python')
        self.ur_df['subject'] = self.ur_df['subject'].str.replace('Moderna språk','Moderna_språk')

    def find_CI(self, chosen_uid):
        chosen_uid = f'~{chosen_uid}'
        self.chosen_content = self.ur_df[self.ur_df['~uid'] == chosen_uid]
        self.keywords = self.chosen_content.iloc[0]['keywords~']
        self.keywords = self.keywords.strip('~')
        self.subject = self.chosen_content.iloc[0]['subject']
        self.subject = self.subject.split()
        self.subject = self.subject[0]
        self.subject = self.subject.replace('_', ' ')
        self.audience = self.chosen_content.iloc[0]['audience']
        self.audience = self.audience.replace('Gymnasieskola', '').strip()
        self.audience = self.audience.replace('Grundskola F-3', 'Grundskola 1-3').strip()

        print(self.keywords)
        print(self.subject)
        print(self.audience)

        CI = pd.read_csv('massive_data/stored_data/CI_vocab.csv')
        self.CI_current = CI.loc[(CI['subject'] == self.subject) & (CI['audience'] == self.audience)]


    def preprocess_texts(self, text):
        download('stopwords')  # Download stopwords list.
        stop_words = stopwords.words('swedish')
        text = text.lower()
        text = re.sub(r"[^\w\d'\s\-]+", '', text)
        text = " ".join([w for w in text.split() if w not in stop_words])
        print(text)
        return text.split(" ")

    def jaccard_similarity(self, query, document):
        #query = query.split()
        #document = document.split()
        intersection = set(query).intersection(set(document))
        union = set(query).union(set(document))
        return len(intersection)/len(union)


    def predict_CI(self, uid):

        self.find_CI(uid)

        CI_keywords_dict = {}

        content_processed = self.preprocess_texts(self.keywords)
        for i, row in self.CI_current.iterrows():
            CI_processed = self.preprocess_texts(row['value'])
            result = self.jaccard_similarity(content_processed, CI_processed)
            formatted_string = "{:.3f}".format(result)
            result = float(formatted_string)
            if result > 0:
                CI_keywords_dict[row['value']] = result


        sorted_dict = sorted(CI_keywords_dict.items() , reverse=True, key=lambda x: x[1])

        for elem in sorted_dict:
            print(f'{elem[0]} : {elem[1]*100} %')  

        return sorted_dict  




