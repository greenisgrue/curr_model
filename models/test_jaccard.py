import pandas as pd
from nltk.corpus import stopwords
from nltk import download
import re

download('stopwords')  # Download stopwords list.
stop_words = stopwords.words('swedish')


CI = "Exempel på hur forntiden, medeltiden, 1500-talet, 1600-talet och 1700-talet kan avläsas i våra dagar genom traditioner, namn, språkliga uttryck, byggnader, städer och gränser."
ur_df = pd.read_csv("../massive_data/search_ur.csv", sep='~,~', engine='python')

chosen_uid = '~208949'
chosen_content = ur_df[ur_df['~uid'] == chosen_uid]
keywords = chosen_content.iloc[0]['keywords~']
keywords = keywords.strip('~')
subject = chosen_content.iloc[0]['subject']
subject = subject.split()
subject = subject[0]
audience = chosen_content.iloc[0]['audience']

print(keywords)
print(subject)
print(audience)

def preprocess_texts(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = " ".join([w for w in text.split() if w not in stop_words])
    return text

def jaccard_similarity(query, document):
    query = query.split()
    document = document.split()
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))
    return len(intersection)/len(union)

text1_processed = preprocess_texts(CI)
text2_processed = preprocess_texts(keywords)


result = jaccard_similarity(text1_processed, text2_processed)
print(result)