import pandas as pd
import re


df = pd.read_table("dictionaries/th_sv_SE.dat", encoding='unicode_escape')

new_df = pd.DataFrame({'word':df['ISO-8859-1'].iloc[::2].values, 'synonyms':df['ISO-8859-1'].iloc[1::2].values})

# new_df['synonyms'] = new_df['synonyms'].str.replace('|', ', ')
new_df['synonyms'] = [re.sub(r"[|]+", ', ', str(x)) for x in new_df['synonyms']]
new_df['synonyms'] = new_df['synonyms'].str.lstrip(', ')

new_df['word'] = [re.sub(r"[|1]+", '', str(x)) for x in new_df['word']]

new_df.to_csv('massive_data/synonyms.csv')

        
