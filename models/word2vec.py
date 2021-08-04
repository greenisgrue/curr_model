import pandas as pd
import re
from nltk.corpus import stopwords
from nltk import download
import stanza
import math
import json
import numpy
import pickle


class W2v():
    def __init__(self, index):
        from skolmedia_client.skolfilm_client import Skolfilm
        client = Skolfilm(index)
        self.ur_df = client.ur_df
        self.word_vectors = client.word_vectors
        self.dictionary = client.dictionary
        self.self_learn = client.self_learn
 
    def generate_id(self):
        random_row = self.ur_df.sample()
        return random_row.iloc[0]['~uid'].strip('~')

    def find_CI(self, chosen_uid):
        # Get metadata from content
        chosen_uid = f'~{chosen_uid}'
        chosen_content = self.ur_df[self.ur_df['~uid'] == chosen_uid]
        self.content_id = chosen_uid.strip('~')
        self.title = chosen_content.iloc[0]['title']
        self.surtitle = chosen_content.iloc[0]['surtitle']
        self.thumbnail = chosen_content.iloc[0]['thumbnail']
        self.description = chosen_content.iloc[0]['description']
        self.subject = chosen_content.iloc[0]['subject'] 
        self.audience = chosen_content.iloc[0]['audience']
        media_type = chosen_content.iloc[0]['streaming_format']
        freetext = chosen_content.iloc[0]['freetext']
        tags = chosen_content.iloc[0]['tags']
        barn = chosen_content.iloc[0]['barn']
        sao = chosen_content.iloc[0]['sao~']
        sao = sao.strip(',~')
        fields = [freetext, tags, barn, sao]

        # Freetext, tags, barn and sao is used in combination as the keywords field
        self.keywords = "" 
        for field in fields:
            if not isinstance(field, float) and len(field) > 0:
                if len(self.keywords) > 0:
                    self.keywords += ', ' + field
                else:
                    self.keywords += field

        # Combining keywords and description with titles
        if not isinstance(self.surtitle, float):
            self.keywords_titles = self.keywords + ', ' + self.title + ', ' + self.surtitle
            self.desc_titles = self.description + ', ' + self.title + ', ' + self.surtitle
        else:
            self.keywords_titles = self.keywords + ', ' + self.title
            self.desc_titles = str(self.description) + ', ' + self.title

        # Get length of keywords field for wiegthing results
        self.keywords_length = len(self.keywords.split(', '))

        # Basfaktor avgör med vilken hastighet kurvan ökar. Högre ökar hastigheten
        # Konstanterna avgör hur nära 1 maxtaket ligger samt faktorn vid k = 1. Mindre differens ger närmare 1.
        self.key_len_factor = (math.log(self.keywords_length,3)+0.4)/(math.log(self.keywords_length,3)+0.47) 

        # CSV-files with "centralt innehåll" including and not including titles for each
        CI = pd.read_csv('massive_data/stored_data/CI_vocab.csv')
        CI_inc_titles = pd.read_csv('massive_data/stored_data/CI_vocab_including_titles.csv')

        # Checking for series to be manually mapped with specific "centralt innehåll". 
        if not isinstance(self.surtitle, float):
            if 'Lilla Aktuellt skola' in self.surtitle:
                self.relevant_CI = CI[CI['uuid'] == '51e34da1-0e1d-11eb-b4ba-0ae95472d63c']
                self.relevant_CI_inc_titles = CI_inc_titles[CI_inc_titles['uuid'] == '51e34da1-0e1d-11eb-b4ba-0ae95472d63c']
        
            elif 'Newsreel' in self.surtitle and self.audience == 'Grundskola 4-6':
                self.relevant_CI = CI[(CI['uuid'] == '35518dcf-0a14-11eb-b4ba-0ae95472d63c') | (CI['uuid'] == '3e8c4968-0a14-11eb-b4ba-0ae95472d63c') | (CI['uuid'] == '0c60d903-0a14-11eb-b4ba-0ae95472d63c') | (CI['uuid'] == '1aa25dc9-0a14-11eb-b4ba-0ae95472d63c')]
                self.relevant_CI_inc_titles = CI_inc_titles[(CI_inc_titles['uuid'] == '35518dcf-0a14-11eb-b4ba-0ae95472d63c') | (CI_inc_titles['uuid'] == '3e8c4968-0a14-11eb-b4ba-0ae95472d63c') | (CI_inc_titles['uuid'] == '0c60d903-0a14-11eb-b4ba-0ae95472d63c') | (CI_inc_titles['uuid'] == '1aa25dc9-0a14-11eb-b4ba-0ae95472d63c')]
        
            elif 'Newsreel' in self.surtitle and self.audience == 'Grundskola 7-9':
                self.relevant_CI = CI[(CI['uuid'] == 'ee776597-0a14-11eb-b4ba-0ae95472d63c') | (CI['uuid'] == 'f265d641-0a14-11eb-b4ba-0ae95472d63c') | (CI['uuid'] == '00be6ce6-0a15-11eb-b4ba-0ae95472d63c') | (CI['uuid'] == '9fdfda18-0a14-11eb-b4ba-0ae95472d63c')]
                self.relevant_CI_inc_titles = CI_inc_titles[(CI_inc_titles['uuid'] == 'ee776597-0a14-11eb-b4ba-0ae95472d63c') | (CI_inc_titles['uuid'] == 'f265d641-0a14-11eb-b4ba-0ae95472d63c') | (CI_inc_titles['uuid'] == '00be6ce6-0a15-11eb-b4ba-0ae95472d63c') | (CI_inc_titles['uuid'] == '9fdfda18-0a14-11eb-b4ba-0ae95472d63c')]
            else:
                self.relevant_CI = CI[CI['subject'].isin(self.subject.split(', ')) & CI['audience'].isin(self.audience.split(', '))]
                self.relevant_CI_inc_titles = CI_inc_titles[CI_inc_titles['subject'].isin(self.subject.split(', ')) & CI_inc_titles['audience'].isin(self.audience.split(', '))]                 

        # Finding all relevant "centralt innehåll" for the provided content id.
        else:
            self.relevant_CI = CI[CI['subject'].isin(self.subject.split(', ')) & CI['audience'].isin(self.audience.split(', '))]
            self.relevant_CI_inc_titles = CI_inc_titles[CI_inc_titles['subject'].isin(self.subject.split(', ')) & CI_inc_titles['audience'].isin(self.audience.split(', '))] 

        # Drop "centralt innehåll" with title "Texter" as no content involves reading
        # if media_type == 'video' or media_type == 'audio' or isinstance(self.media_type, float):
        self.relevant_CI = self.relevant_CI.drop(self.relevant_CI[self.relevant_CI.title == 'Texter'].index)
        self.relevant_CI_inc_titles = self.relevant_CI_inc_titles.drop(self.relevant_CI_inc_titles[self.relevant_CI_inc_titles.title == 'Texter'].index)

        self.versions = chosen_content.iloc[0]['versions']
        self.versions_dict = []

        self.primary = None
        if self.versions != '[]':
            versions = [self.versions]
            versions_dict = [json.loads(idx.replace("'", '"')) for idx in versions]
            self.versions_dict = versions_dict[0]
            self.primary = next((item for item in self.versions_dict if item['primary'] == 'true'), None)    
            if len(self.versions_dict) < 2 or self.primary is None: 
                return None 
            if str(self.primary.get('uid')) != chosen_uid:
                primary_uid = str(self.primary.get('uid'))
                primary_uid = f'~{primary_uid}' 
                chosen_uid = primary_uid
                primary_content = self.ur_df[self.ur_df['~uid'] == chosen_uid]
                self.primary_subject = primary_content.iloc[0]['subject'] 
                title = primary_content.iloc[0]['title']
                surtitle = primary_content.iloc[0]['surtitle']
                freetext = primary_content.iloc[0]['freetext']
                tags = primary_content.iloc[0]['tags']
                barn = primary_content.iloc[0]['barn']
                sao = primary_content.iloc[0]['sao~']
                sao = sao.strip(',~')
                fields = [freetext, tags, barn, sao]

                # Freetext, tags, barn and sao is used in combination as the keywords field
                self.primary_keywords = "" 
                for field in fields:
                    if not isinstance(field, float) and len(field) > 0:
                        if len(self.primary_keywords) > 0:
                            self.primary_keywords += ', ' + field
                        else:
                            self.primary_keywords += field

                # Combining keywords and description with titles
                if not isinstance(self.surtitle, float):
                    self.keywords_titles = self.primary_keywords + ', ' + title + ', ' + surtitle
                    self.desc_titles = self.description + ', ' + title + ', ' + surtitle
                else:
                    self.keywords_titles = self.primary_keywords + ', ' + title
                    self.desc_titles = self.description + ', ' + title               

                # Get length of keywords field for weighting results
                self.keywords_length = len(self.primary_keywords.split(', '))

                # Basfaktor avgör med vilken hastighet kurvan ökar. Högre ökar hastigheten
                # Konstanterna avgör hur nära 1 maxtaket ligger samt faktorn vid k = 1. Mindre differens ger närmare 1.
                self.key_len_factor = (math.log(self.keywords_length,3)+0.4)/(math.log(self.keywords_length,3)+0.47) 

                # Finding all relevant "centralt innehåll" for the provided content id.
                self.relevant_CI = CI[CI['subject'].isin(self.primary_subject.split(', ')) & CI['audience'].isin(self.audience.split(', '))]
                self.relevant_CI_inc_titles = CI_inc_titles[CI_inc_titles['subject'].isin(self.primary_subject.split(', ')) & CI_inc_titles['audience'].isin(self.audience.split(', '))] 

                # Lock specific language related "centralt innehåll" for content in other languages that are based on a swedish version
                if self.audience == 'Grundskola 1-3':
                    if 'Modersmål -  finska som nationellt minoritetsspråk' in self.subject:
                        self.relevant_CI = self.relevant_CI.append(CI[((CI['value'] == 'Samtal om vardagliga företeelser och händelser.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter.')) & (CI['subject'] == 'Modersmål -  finska som nationellt minoritetsspråk')], ignore_index=True)
                        self.relevant_CI_inc_titles = self.relevant_CI_inc_titles.append(CI[((CI['value'] == 'Samtal om vardagliga företeelser och händelser.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter.')) & (CI['subject'] == 'Modersmål -  finska som nationellt minoritetsspråk')], ignore_index=True)
                    elif 'Modersmål -  jiddish som nationellt minoritetsspråk' in self.subject:
                        self.relevant_CI = self.relevant_CI.append(CI[((CI['value'] == 'Samtal om vardagliga företeelser och händelser.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter.')) & (CI['subject'] == 'Modersmål -  jiddish som nationellt minoritetsspråk')], ignore_index=True)
                        self.relevant_CI_inc_titles = self.relevant_CI_inc_titles.append(CI[((CI['value'] == 'Samtal om vardagliga företeelser och händelser.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter.')) & (CI['subject'] == 'Modersmål -  jiddish som nationellt minoritetsspråk')], ignore_index=True)
                    elif 'Modersmål -  meänkieli som nationellt minoritetsspråk' in self.subject:
                        self.relevant_CI = self.relevant_CI.append(CI[((CI['value'] == 'Samtal om vardagliga företeelser och händelser.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter.')) & (CI['subject'] == 'Modersmål -  meänkieli som nationellt minoritetsspråk')], ignore_index=True)
                        self.relevant_CI_inc_titles = self.relevant_CI_inc_titles.append(CI[((CI['value'] == 'Samtal om vardagliga företeelser och händelser.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter.')) & (CI['subject'] == 'Modersmål -  meänkieli som nationellt minoritetsspråk')], ignore_index=True)
                    elif 'Modersmål -  romani chib som nationellt minoritetsspråk' in self.subject:
                        self.relevant_CI = self.relevant_CI.append(CI[((CI['value'] == 'Samtal om vardagliga företeelser och händelser.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter.')) & (CI['subject'] == 'Modersmål -  romani chib som nationellt minoritetsspråk')], ignore_index=True)
                        self.relevant_CI_inc_titles = self.relevant_CI_inc_titles.append(CI[((CI['value'] == 'Samtal om vardagliga företeelser och händelser.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter.')) & (CI['subject'] == 'Modersmål -  romani chib som nationellt minoritetsspråk')], ignore_index=True)
                    elif 'Modersmål -  utom nationella minoritetsspråk' in self.subject:
                        self.relevant_CI = self.relevant_CI.append(CI[((CI['value'] == 'Samtal om vardagliga företeelser och händelser.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter.') | (CI['value'] == 'Uttal, betoning och satsmelodi och uttalets betydelse för att göra sig förstådd.')) & ((CI['subject'] == 'Modersmål -  utom nationella minoritetsspråk') | (CI['subject'] == 'Modersmål -  utom nationellt minoritetsspråk'))], ignore_index=True)
                        self.relevant_CI_inc_titles = self.relevant_CI_inc_titles.append(CI[((CI['value'] == 'Samtal om vardagliga företeelser och händelser.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter.') | (CI['value'] == 'Uttal, betoning och satsmelodi och uttalets betydelse för att göra sig förstådd.')) & ((CI['subject'] == 'Modersmål -  utom nationella minoritetsspråk') | (CI['subject'] == 'Modersmål -  utom nationellt minoritetsspråk'))], ignore_index=True)

                if self.audience == 'Grundskola 4-6':
                    if 'Modersmål -  finska som nationellt minoritetsspråk' in self.subject:
                        self.relevant_CI = self.relevant_CI.append(CI[((CI['value'] == 'Samtal om egna och andras upplevelser samt om vardagliga företeelser och händelser.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter. Ords och begrepps nyanser och värdeladdning.')) & (CI['subject'] == 'Modersmål -  finska som nationellt minoritetsspråk')], ignore_index=True)
                        self.relevant_CI_inc_titles = self.relevant_CI_inc_titles.append(CI[((CI['value'] == 'Samtal om egna och andras upplevelser samt om vardagliga företeelser och händelser.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter. Ords och begrepps nyanser och värdeladdning.')) & (CI['subject'] == 'Modersmål -  finska som nationellt minoritetsspråk')], ignore_index=True)
                    elif 'Modersmål -  jiddish som nationellt minoritetsspråk' in self.subject:
                        self.relevant_CI = self.relevant_CI.append(CI[((CI['value'] == 'Samtal om egna och andras upplevelser samt om vardagliga företeelser och händelser.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter. Ords och begrepps nyanser och värdeladdning.')) & (CI['subject'] == 'Modersmål -  jiddish som nationellt minoritetsspråk')], ignore_index=True)
                        self.relevant_CI_inc_titles = self.relevant_CI_inc_titles.append(CI[((CI['value'] == 'Samtal om egna och andras upplevelser samt om vardagliga företeelser och händelser.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter. Ords och begrepps nyanser och värdeladdning.')) & (CI['subject'] == 'Modersmål -  jiddish som nationellt minoritetsspråk')], ignore_index=True)
                    elif 'Modersmål -  meänkieli som nationellt minoritetsspråk' in self.subject:
                        self.relevant_CI = self.relevant_CI.append(CI[((CI['value'] == 'Samtal om egna och andras upplevelser samt om vardagliga företeelser och händelser.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter. Ords och begrepps nyanser och värdeladdning.')) & (CI['subject'] == 'Modersmål -  meänkieli som nationellt minoritetsspråk')], ignore_index=True)
                        self.relevant_CI_inc_titles = self.relevant_CI_inc_titles.append(CI[((CI['value'] == 'Samtal om egna och andras upplevelser samt om vardagliga företeelser och händelser.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter. Ords och begrepps nyanser och värdeladdning.')) & (CI['subject'] == 'Modersmål -  meänkieli som nationellt minoritetsspråk')], ignore_index=True)
                    elif 'Modersmål -  romani chib som nationellt minoritetsspråk' in self.subject:
                        self.relevant_CI = self.relevant_CI.append(CI[((CI['value'] == 'Samtal om egna och andras upplevelser samt om vardagliga företeelser och händelser.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter. Ords och begrepps nyanser och värdeladdning.')) & (CI['subject'] == 'Modersmål -  romani chib som nationellt minoritetsspråk')], ignore_index=True)
                        self.relevant_CI_inc_titles = self.relevant_CI_inc_titles.append(CI[((CI['value'] == 'Samtal om egna och andras upplevelser samt om vardagliga företeelser och händelser.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter. Ords och begrepps nyanser och värdeladdning.')) & (CI['subject'] == 'Modersmål -  romani chib som nationellt minoritetsspråk')], ignore_index=True)
                    if 'Modersmål -  utom nationella minoritetsspråk' in self.subject:
                        self.relevant_CI = self.relevant_CI.append(CI[((CI['value'] == 'Uttal, betoning och satsmelodi och uttalets betydelse för att göra sig förstådd.') | (CI['value'] == 'Synonymer, motsatsord och andra relationer mellan ord.')) & ((CI['subject'] == 'Modersmål -  utom nationellt minoritetsspråk') | (CI['subject'] == 'Modersmål -  utom nationella minoritetsspråk'))], ignore_index=True)
                        self.relevant_CI_inc_titles = self.relevant_CI_inc_titles.append(CI[((CI['value'] == 'Uttal, betoning och satsmelodi och uttalets betydelse för att göra sig förstådd.') | (CI['value'] == 'Synonymer, motsatsord och andra relationer mellan ord.')) & ((CI['subject'] == 'Modersmål -  utom nationellt minoritetsspråk') | (CI['subject'] == 'Modersmål -  utom nationella minoritetsspråk'))], ignore_index=True)

                if self.audience == 'Grundskola 7-9':
                    if 'Modersmål -  finska som nationellt minoritetsspråk' in self.subject:
                        self.relevant_CI = self.relevant_CI.append(CI[((CI['value'] == 'Skillnader i språkanvändning beroende på syfte, mottagare och sammanhang. Språkets betydelse för att utöva inflytande.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter. Ords och begrepps nyanser och värdeladdning. Bildspråk och idiomatiska uttryck.')) & (CI['subject'] == 'Modersmål -  finska som nationellt minoritetsspråk')], ignore_index=True)
                        self.relevant_CI_inc_titles = self.relevant_CI_inc_titles.append(CI[((CI['value'] == 'Skillnader i språkanvändning beroende på syfte, mottagare och sammanhang. Språkets betydelse för att utöva inflytande.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter. Ords och begrepps nyanser och värdeladdning. Bildspråk och idiomatiska uttryck.')) & (CI['subject'] == 'Modersmål -  finska som nationellt minoritetsspråk')], ignore_index=True)
                    elif 'Modersmål -  jiddish som nationellt minoritetsspråk' in self.subject:
                        self.relevant_CI = self.relevant_CI.append(CI[((CI['value'] == 'Skillnader i språkanvändning beroende på syfte, mottagare och sammanhang. Språkets betydelse för att utöva inflytande.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter. Ords och begrepps nyanser och värdeladdning. Bildspråk och idiomatiska uttryck.')) & (CI['subject'] == 'Modersmål -  jiddish som nationellt minoritetsspråk')], ignore_index=True)
                        self.relevant_CI_inc_titles = self.relevant_CI_inc_titles.append(CI[((CI['value'] == 'Skillnader i språkanvändning beroende på syfte, mottagare och sammanhang. Språkets betydelse för att utöva inflytande.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter. Ords och begrepps nyanser och värdeladdning. Bildspråk och idiomatiska uttryck.')) & (CI['subject'] == 'Modersmål -  jiddish som nationellt minoritetsspråk')], ignore_index=True)
                    elif 'Modersmål -  meänkieli som nationellt minoritetsspråk' in self.subject:
                        self.relevant_CI = self.relevant_CI.append(CI[((CI['value'] == 'Skillnader i språkanvändning beroende på syfte, mottagare och sammanhang. Språkets betydelse för att utöva inflytande.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter. Ords och begrepps nyanser och värdeladdning. Bildspråk och idiomatiska uttryck.')) & (CI['subject'] == 'Modersmål -  meänkieli som nationellt minoritetsspråk')], ignore_index=True)
                        self.relevant_CI_inc_titles = self.relevant_CI_inc_titles.append(CI[((CI['value'] == 'Skillnader i språkanvändning beroende på syfte, mottagare och sammanhang. Språkets betydelse för att utöva inflytande.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter. Ords och begrepps nyanser och värdeladdning. Bildspråk och idiomatiska uttryck.')) & (CI['subject'] == 'Modersmål -  meänkieli som nationellt minoritetsspråk')], ignore_index=True)
                    elif 'Modersmål -  romani chib som nationellt minoritetsspråk' in self.subject:
                        self.relevant_CI = self.relevant_CI.append(CI[((CI['value'] == 'Skillnader i språkanvändning beroende på syfte, mottagare och sammanhang. Språkets betydelse för att utöva inflytande.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter. Ords och begrepps nyanser och värdeladdning. Bildspråk och idiomatiska uttryck.')) & (CI['subject'] == 'Modersmål -  romani chib som nationellt minoritetsspråk')], ignore_index=True)
                        self.relevant_CI_inc_titles = self.relevant_CI_inc_titles.append(CI[((CI['value'] == 'Skillnader i språkanvändning beroende på syfte, mottagare och sammanhang. Språkets betydelse för att utöva inflytande.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter. Ords och begrepps nyanser och värdeladdning. Bildspråk och idiomatiska uttryck.')) & (CI['subject'] == 'Modersmål -  romani chib som nationellt minoritetsspråk')], ignore_index=True)
                    elif 'Modersmål -  utom nationellt minoritetsspråk' in self.subject:
                        self.relevant_CI = self.relevant_CI.append(CI[((CI['value'] == 'Uttal, betoning och satsmelodi i jämförelse med svenskan samt olika talade variationer av modersmålet.') | (CI['value'] == 'Skillnader i språkanvändning beroende på syfte, mottagare och sammanhang. Språkets betydelse för att utöva inflytande.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter. Ords och begrepps nyanser och värdeladdning. Bildspråk och idiomatiska uttryck.')) & ((CI['subject'] == 'Modersmål -  utom nationellt minoritetsspråk') | (CI['subject'] == 'Modersmål -  utom nationella minoritetsspråk'))], ignore_index=True)
                        self.relevant_CI_inc_titles = self.relevant_CI_inc_titles.append(CI[((CI['value'] == 'Uttal, betoning och satsmelodi i jämförelse med svenskan samt olika talade variationer av modersmålet.') | (CI['value'] == 'Skillnader i språkanvändning beroende på syfte, mottagare och sammanhang. Språkets betydelse för att utöva inflytande.') | (CI['value'] == 'Ord och begrepp för att uttrycka känslor, kunskaper och åsikter. Ords och begrepps nyanser och värdeladdning. Bildspråk och idiomatiska uttryck.')) & ((CI['subject'] == 'Modersmål -  utom nationellt minoritetsspråk') | (CI['subject'] == 'Modersmål -  utom nationella minoritetsspråk'))], ignore_index=True)

                # Drop duplicates and "centralt innehåll" with title "Texter" as no content involves reading
                self.relevant_CI = self.relevant_CI.drop_duplicates(subset=['value'])
                #if media_type == 'video' or media_type == 'audio' or isinstance(self.media_type, float):
                self.relevant_CI = self.relevant_CI.drop(self.relevant_CI[self.relevant_CI.title == 'Texter'].index)
                self.relevant_CI_inc_titles = self.relevant_CI_inc_titles.drop(self.relevant_CI_inc_titles[self.relevant_CI_inc_titles.title == 'Texter'].index)

    def preprocess_texts(self, text):
        # Preprocess text. Lowercase, remove punctuation, remove stop words and custom stop words
        stop_words = stopwords.words('swedish')
        lowered_text = text.lower()
        rm_custom_words = ' '.join([self.dictionary.get(i, i) for i in lowered_text.split()])
        rm_punctuation_text = re.sub(r"[^\w\s-]+", '', rm_custom_words)
        text = " ".join([w for w in rm_punctuation_text.split() if w not in stop_words])

        # Change year spans to words that can be compared and used in w2v model
        for word in text.split():
            era = word
            # Common cases
            if word == '800-1500':
                era = 'medeltiden'
            elif word == '1500-1800':
                era = 'renässansen'
            elif '-' in word and len(word) > 1:
                years = word.split('-')
                # Handle other cases where it is year - year. Ex. 1939-1945
                if years[0].isnumeric() and years[1].isnumeric():
                    era = [self.find_era(years[0]), self.find_era(years[1])]
                    era = ' '.join(era)
                # Handle cases where it is year- tal
                elif years[0].isnumeric() and not (years[1].isnumeric()):
                    era = self.find_era(years[0])
            text = text.replace(word, era)
        return text.split(" ")

    def find_era(self, year):
        # Translate years (int) to era (string)
        era = year
        if 1800 <= int(year) <= 1859 and int(year) != 1850:
            era = 'industrialiseringen'
        elif 1914 <= int(year) <= 1918:
            era = 'första världskriget'
        elif 1939 <= int(year) <= 1945:
            era = 'andra världskriget'
        return era  
 
    def jaccard_similarity(self, query, document):
        intersection = set(query).intersection(set(document))
        union = set(query).union(set(document))
        return len(intersection)/len(union)

    def cos_sim(self, keywords, CI_doc):     
        # calculate cos_sim between documents. If word can not be found, remove from document and try cos_sim again   
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
        # calculate wmd between documents. If word can not be found, remove from document and try wmd again    
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

    def format_result_jaccard(self, uid, CI, title, result):
        # Save results for "centralt innehåll" in dictionary
        # Also search for previos instance of current "centralt innehåll" in dict. If found but with worse value, replace with current        
        current_CI = self.jaccard_dict.get(uid)
        if current_CI is None or current_CI.get('value') < result:
            self.jaccard_dict[uid] = {'CI': CI, 'title':  title, 'value': result}
    
    def format_result_cos(self, uid, CI, audience, subject, title, result, result_type):
        # Save results for "centralt innehåll" in dictionary
        # Also search for previos instance of current "centralt innehåll" in dict. If found but with worse value, replace with current        
        current_CI = self.cos_dict.get(uid)
        if current_CI is None or current_CI.get('value') < result:
            self.cos_dict[uid] = {'CI': CI, 'audience': audience, 'subject': subject, 'title': title, 'type': result_type, 'value': result}

    def format_result_wmd(self, uid, CI, audience, subject, title, result, result_type):
        current_CI = self.wmd_dict.get(uid)
        # Normalize results to be able to compare with cos_sim results
        norm_result = (1-((result/1.25)-0.5))/0.9
        # Save results for "centralt innehåll" in dictionary
        # Also search for previos instance of current "centralt innehåll" in dict. If found but with worse value, replace with current
        if current_CI is None or current_CI.get('value') < norm_result:
            self.wmd_dict[uid] = {'CI': CI, 'audience': audience, 'subject': subject, 'title':  title, 'type': result_type, 'value': norm_result}

    def get_results(self, row):
        CI_processed = self.preprocess_texts(row['value'])

        # Apply versions of sub-models and save results in dictionaries
        result_jaccard_CIT_CT = self.jaccard_similarity(self.content_processed_CT, CI_processed)
        result_jaccard_desc = self.jaccard_similarity(self.content_processed_desc, CI_processed)
        result_jaccard_desc_CT = self.jaccard_similarity(self.content_processed_desc_CT, CI_processed)

        result_wmd_CIT_CT = self.wmd(self.content_processed_CT, CI_processed)
        result_wmd_CIT = self.wmd(self.content_processed, CI_processed)
        result_wmd_CIT_desc = self.wmd(self.content_processed_desc, CI_processed)
        result_wmd_CIT_desc_CT = self.wmd(self.content_processed_desc_CT, CI_processed)

        result_cos_CIT_CT = self.cos_sim(self.content_processed_CT, CI_processed)
        result_cos_CIT = self.cos_sim(self.content_processed, CI_processed)
        result_cos_CIT_desc = self.cos_sim(self.content_processed_desc, CI_processed)
        result_cos_CIT_desc_CT = self.cos_sim(self.content_processed_desc_CT, CI_processed)

        self.format_result_jaccard(row['uuid'], row['CI'], row['title'], result_jaccard_CIT_CT)
        self.format_result_jaccard(row['uuid'], row['CI'], row['title'], result_jaccard_desc)
        self.format_result_jaccard(row['uuid'], row['CI'], row['title'], result_jaccard_desc_CT)

        self.format_result_wmd(row['uuid'], row['CI'], row['audience'], row['subject'], row['title'], result_wmd_CIT_CT, 'wmd_CIT_CT')
        self.format_result_wmd(row['uuid'], row['CI'], row['audience'], row['subject'], row['title'], result_wmd_CIT, 'wmd_CIT')
        self.format_result_wmd(row['uuid'], row['CI'], row['audience'], row['subject'], row['title'], result_wmd_CIT_desc, 'wmd_CIT_desc')
        self.format_result_wmd(row['uuid'], row['CI'], row['audience'], row['subject'], row['title'], result_wmd_CIT_desc_CT, 'wmd_CIT_desc_CT')
            
        self.format_result_cos(row['uuid'], row['CI'], row['audience'], row['subject'], row['title'], result_cos_CIT_CT, 'cos_CIT_CT')
        self.format_result_cos(row['uuid'], row['CI'], row['audience'], row['subject'], row['title'], result_cos_CIT, 'cos_CIT')
        self.format_result_cos(row['uuid'], row['CI'], row['audience'], row['subject'], row['title'], result_cos_CIT_desc, 'cos_CIT_desc')
        self.format_result_cos(row['uuid'], row['CI'], row['audience'], row['subject'], row['title'], result_cos_CIT_desc_CT, 'cos_CIT_desc_CT')


    def predict_CI(self, uid):
        # Find relevant CI
        self.find_CI(uid)
        
        # Dictionaries to save results of CI for different sub-models
        self.cos_dict = {}
        self.wmd_dict = {}
        self.jaccard_dict = {}

        # Process metadata using keywords and content title, only keywords, only description and description and content title
        self.content_processed_CT = self.preprocess_texts(self.keywords_titles)
        self.content_processed = self.preprocess_texts(self.keywords)
        self.content_processed_desc = self.preprocess_texts(self.description)
        self.content_processed_desc_CT = self.preprocess_texts(self.desc_titles)

        if (self.versions != '[]') & (len(self.versions_dict) > 1) & (self.primary is not None):
            self.content_processed = self.preprocess_texts(self.primary_keywords)

        # Iterate rows containing "centralt innehåll" with titles and apply sub-models to compare with content metadata
        for i, row in self.relevant_CI_inc_titles.iterrows():
            self.get_results(row)    
            if (self.versions_dict and 'Modersmål' in row['subject']) or (self.surtitle == 'Lilla Aktuellt skola') or (self.surtitle == 'Newsreel'):
                self.cos_dict[row.uuid] = {'CI': row['CI'], 'audience': row['audience'], 'subject': row['subject'], 'title': row['title'], 'type': 'Preset', 'value': 1.0}          
                self.wmd_dict[row.uuid] = {'CI': row['CI'], 'audience': row['audience'], 'subject': row['subject'], 'title': row['title'], 'type': 'Preset', 'value': 1.0}          

        # Iterate rows containing only "centralt innehåll" and apply sub-models to compare with content metadata
        for i, row in self.relevant_CI.iterrows():
            self.get_results(row)
            if self.versions_dict and'Modersmål' in row['subject']:
                self.cos_dict[row.uuid] = {'CI': row['CI'], 'audience': row['audience'], 'subject': row['subject'], 'title': row['title'], 'type': 'Preset', 'value': 1.0}          
                self.wmd_dict[row.uuid] = {'CI': row['CI'], 'audience': row['audience'], 'subject': row['subject'], 'title': row['title'], 'type': 'Preset', 'value': 1.0}          

        # Find duplicates of "centralt innehåll". If duplicate is found, flag it so it is not shown in interface. 
        duplicate_list = []
        to_delete = []
        key_list = list(self.cos_dict.keys())
        val_list = list(self.cos_dict.values())
        v_list = []
        for item in val_list:
            v_list.append(item.get('CI'))

        for key, value in self.cos_dict.items():
            position = v_list.index(value.get('CI'))
            if value.get('CI') in duplicate_list:
                position = v_list.index(value.get('CI'))
                self.cos_dict[key_list[position]]['duplicate'] = key
                self.cos_dict[key]['duplicate'] = 'Yes'
            else:
                self.cos_dict[key]['duplicate'] = False
                duplicate_list.append(value.get('CI'))

            # Calculate a score for each "centralt innehåll"
            matched_wmd = self.wmd_dict.get(key)
            matched_jaccard = self.jaccard_dict.get(key)
            wmd_value = matched_wmd.get('value')
            cos_value = value.get('value')
            jaccard_value = matched_jaccard.get('value')

            # Optimal value is calcualted using the average of cos_sim and wmd and a factor of jaccard value. 
            # Multiply with key_len_factor to adjust for number of keywords of content. Fewer keywords leading to a lower key_len_factor 
            pure_score = self.key_len_factor * ((wmd_value + cos_value) / 2) + (1 - ((wmd_value + cos_value) / 2)) * 3*jaccard_value
            
            # Apply self learning factor.
            if (self.versions != '[]') & (len(self.versions_dict) > 1) & (self.primary is not None):
                self_learn_score = self.self_learn.update_score(key, self.primary_keywords, pure_score)  
            else:
                self_learn_score = self.self_learn.update_score(key, self.keywords, pure_score)

            adjusted_score = pure_score + self_learn_score

            # Format final value to remove unneccesary decimals
            formatted_string = "{:.3f}".format(pure_score)
            pure_score = float(formatted_string)
            formatted_string = "{:.3f}".format(adjusted_score)
            adjusted_score = float(formatted_string)

            # Add new adjusted optimal value to dictionary
            self.cos_dict[key]['value'] = pure_score
            self.cos_dict[key]['adjusted_value'] = adjusted_score


        # Sort dictionary on value to get the best scored "centralt innehåll" first
        sorted_dict = sorted(self.cos_dict.items(), reverse=True, key = lambda x: x[1]['adjusted_value'])       

        return sorted_dict










