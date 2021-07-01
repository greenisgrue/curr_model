import pandas as pd
import math
import numpy
from collections import Counter

from dictionary import get_dictionary

dictionary = get_dictionary()

def clean():
    ur_df = pd.read_csv("../massive_data/stored_data/search_ur.csv", sep='~,~', engine='python')
    ur_df = ur_df[ur_df.audience.str.contains('|'.join(['Grundskola F-3','Grundskola 4-6','Grundskola 7-9']), na=False)]
    ur_df['audience'] = ur_df['audience'].str.replace('Grundskola F-3','Grundskola 1-3')
    ur_df['subject'] = ur_df['subject'].str.replace('Svenska som andraspråk och SFI', 'Svenska som andraspråk')
    ur_df['subject'] = ur_df['subject'].str.replace('Teckenspråk', 'Teckenspråk för hörande')
    ur_df['subject'] = ur_df['subject'].str.replace('Psykologi och filosofi', 'Samhällskunskap, Religionskunskap, Biologi, Hem- konsumentskap, idrott och hälsa, Historia')
    ur_df['subject'] = ur_df['subject'].str.replace('Värdegrund', 'Samhällskunskap, Religionskunskap, Biologi')
    ur_df['subject'] = ur_df['subject'].str.replace('Pedagogiska frågor', 'Samhällskunskap, Religionskunskap, Biologi, Hem- konsumentskap, idrott och hälsa, Historia')
    ur_df['subject'] = ur_df['subject'].str.replace('Information och media', 'Samhällskunskap, Teknik')
    print(len(ur_df.index))
    for index, row in ur_df.iterrows():
        if not isinstance(row['subject'], float):
            if 'Modersmål och minoritetsspråk' in row['subject']:
                ur_df.at[index,'subject'] = row['subject'].replace('Modersmål och minoritetsspråk', translate(row['language']))

            if ('Hem- och konsumentkunskap' in row['subject']) & (row['audience'] != 'Grundskola 7-9'):
                ur_df.at[index,'audience'] = row['audience'] + ', Grundskola 1-6'
            
            ur_df.at[index,'subject'] = remove_duplicates(ur_df.at[index,'subject'])
        else:
            ur_df = ur_df.drop(labels=index, axis=0)

        if row['subject'] == 'Övrigt':
            ur_df = ur_df.drop(labels=index, axis=0)

    print(len(ur_df.index))
    ur_df.to_csv('../massive_data/stored_data/search_ur_cleaned.csv')


def remove_duplicates(input):
    input = input.split(", ")

    for i in range(0, len(input)):
        input[i] = "".join(input[i])
 
    unique_word = Counter(input)
    
    return ", ".join(unique_word.keys())


def translate(language):
    for key in dictionary:
        # print(language)
        
        if not (isinstance(language, float)) and (key in language):
            return dictionary.get(key)
    
    return 'Modersmål -  utom nationella minoritetsspråk'

#print(remove_duplicates('Teknik, Teknik'))
clean()
 