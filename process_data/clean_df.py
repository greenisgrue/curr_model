import pandas as pd
import math
import numpy
from collections import Counter

from process_data.dictionary import get_dictionary

dictionary = get_dictionary()

def clean(index):
    ur_df = pd.read_csv(f"./massive_data/stored_data/{index}.csv", sep='~,~', engine='python')
    ur_df = ur_df[ur_df.audience.str.contains('|'.join(['Grundskola F-3','Grundskola 4-6','Grundskola 7-9']), na=False)]
    ur_df['audience'] = ur_df['audience'].str.replace('Grundskola F-3','Grundskola 1-3')
    ur_df['subject'] = ur_df['subject'].str.replace('Svenska som andraspråk och SFI', 'Svenska som andraspråk')
    ur_df['subject'] = ur_df['subject'].str.replace('Teckenspråk', 'Teckenspråk för hörande')
    ur_df['subject'] = ur_df['subject'].str.replace('Psykologi och filosofi', 'Samhällskunskap, Religionskunskap, Biologi, Hem- konsumentskap, idrott och hälsa, Historia')
    ur_df['subject'] = ur_df['subject'].str.replace('Värdegrund', 'Samhällskunskap, Religionskunskap, Biologi')
    ur_df['subject'] = ur_df['subject'].str.replace('Pedagogiska frågor', 'Samhällskunskap, Religionskunskap, Biologi, Hem- konsumentskap, idrott och hälsa, Historia')
    ur_df['subject'] = ur_df['subject'].str.replace('Information och media', 'Samhällskunskap, Teknik')
    for i, row in ur_df.iterrows():
        if not isinstance(row['subject'], float):
            if 'Modersmål och minoritetsspråk' in row['subject']:
                ur_df.at[i,'subject'] = row['subject'].replace('Modersmål och minoritetsspråk', translate(row['language']))

            if 'Miljö' in row['subject']:
                ur_df.at[i,'subject'] = ur_df.at[i,'subject'].replace('Miljö', 'Biologi, Kemi, Teknik, Geografi')

            if ('Hem- och konsumentkunskap' in row['subject']) & (row['audience'] != 'Grundskola 7-9'):
                ur_df.at[i,'audience'] = row['audience'] + ', Grundskola 1-6'

            if row['subject'] == 'Övrigt' or row['surtitle'] == 'Orka plugga':
                ur_df = ur_df.drop(labels=i, axis=0)
            
            #ur_df.at[i,'subject'] = remove_duplicates(ur_df.at[i,'subject'])
        else:
            ur_df = ur_df.drop(labels=i, axis=0)
        


    ur_df.to_csv(f'./massive_data/stored_data/{index}_cleaned.csv', index=False)

    CI = pd.read_csv("./massive_data/stored_data/CI_vocab.csv")
    CI_titles = pd.read_csv("./massive_data/stored_data/CI_vocab_including_titles.csv")
    
    CI['title'] = CI['title'].str.replace('–', '-')
    CI_titles['title'] = CI_titles['title'].str.replace('–', '-')
    CI_titles['value'] = CI_titles['value'].str.replace('–', '-')


    CI.to_csv("./massive_data/stored_data/CI_vocab.csv", index=False)
    CI_titles.to_csv("./massive_data/stored_data/CI_vocab_including_titles.csv", index=False)

    return ur_df


def remove_duplicates(input):
    input = input.split(", ")

    for i in range(0, len(input)):
        input[i] = "".join(input[i])
 
    unique_word = Counter(input)
    
    return ", ".join(unique_word.keys())


def translate(language):
    for key in dictionary:
        # key = key.lower()        
        if not (isinstance(language, float)) and (key in language):
            return dictionary.get(key)
    
    return 'Modersmål -  utom nationella minoritetsspråk'


