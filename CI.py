import pandas as pd

vocab = pd.read_csv('massive_data/vocabularies.csv')
vocab['subject'] = ""
vocab['audience'] = ""

for i, row in vocab.iterrows():

    if row['parent'] == 'b49e3b41-0a08-11eb-b4ba-0ae95472d63c' or row['parent'] == '7dc61678-0a08-11eb-b4ba-0ae95472d63c' or row['parent'] == 'a40dd26d-0a08-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Bild'
        vocab.at[i,'audience'] = 'Grundskola 1-3'

    elif row['parent'] == '079dcad7-0a09-11eb-b4ba-0ae95472d63c' or row['parent'] == 'f872698e-0a08-11eb-b4ba-0ae95472d63c' or row['parent'] == '03ccc7aa-0a09-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Bild'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == '29fa0ee0-0a0a-11eb-b4ba-0ae95472d63c' or row['parent'] == '1cb6ddb2-0a0a-11eb-b4ba-0ae95472d63c' or row['parent'] == '267bf357-0a0a-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Bild'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

    elif row['parent'] == 'fe5a33b2-0a0d-11eb-b4ba-0ae95472d63c' or row['parent'] == '084d72f0-0a0e-11eb-b4ba-0ae95472d63c' or row['parent'] == '01d3ac26-0a0e-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Biologi'
        vocab.at[i,'audience'] = 'Grundskola 1-3'

    elif row['parent'] == '1f0274b5-0a12-11eb-b4ba-0ae95472d63c' or row['parent'] == '22ef3c3e-0a12-11eb-b4ba-0ae95472d63c' or row['parent'] == '27c2f387-0a12-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Biologi'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == '8d75740c-0a12-11eb-b4ba-0ae95472d63c' or row['parent'] == '8a1ee452-0a12-11eb-b4ba-0ae95472d63c' or row['parent'] == '90bfda5d-0a12-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Biologi'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

    elif row['parent'] == 'a4e30191-0a13-11eb-b4ba-0ae95472d63c' or row['parent'] == 'a947a88e-0a13-11eb-b4ba-0ae95472d63c' or row['parent'] == 'ad645c3f-0a13-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Engelska'
        vocab.at[i,'audience'] = 'Grundskola 1-3'

    elif row['parent'] == 'f25cb441-0a13-11eb-b4ba-0ae95472d63c' or row['parent'] == 'f536057b-0a13-11eb-b4ba-0ae95472d63c' or row['parent'] == 'f90e9f77-0a13-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Engelska'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == '810fd5c3-0a14-11eb-b4ba-0ae95472d63c' or row['parent'] == '83abc5a5-0a14-11eb-b4ba-0ae95472d63c' or row['parent'] == '88f0017e-0a14-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Engelska'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

    elif row['parent'] == '1ba2e4ed-0a16-11eb-b4ba-0ae95472d63c' or row['parent'] == '204c7fdd-0a16-11eb-b4ba-0ae95472d63c' or row['parent'] == 'ef240f41-0a15-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Fysik'
        vocab.at[i,'audience'] = 'Grundskola 1-3'

    elif row['parent'] == 'd8d6f9ba-0a17-11eb-b4ba-0ae95472d63c' or row['parent'] == 'dd43376a-0a17-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Fysik'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == '76139e1a-0a18-11eb-b4ba-0ae95472d63c' or row['parent'] == '774f4a12-0a18-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Fysik'
        vocab.at[i,'audience'] = 'Grundskola 7-9'



    elif row['parent'] == '33ee7f31-0a19-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Geografi'

    elif row['parent'] == 'b2288708-0a1c-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Hem- och konsumentkunskap'

    elif row['parent'] == '675651f9-0a1f-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Historia'

    elif row['parent'] == '4ee2d1c6-0a22-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Idrott och hälsa'

    elif row['parent'] == 'dc510969-0ee2-11eb-b4ba-0ae95472d63c':
        row['subject'] == 'Judiska studier'
        vocab.at[i,'subject'] = 'Judiska studier'

    elif row['parent'] == '7e58cb9b-0a25-11eb-b4ba-0ae95472d63c':
        row['subject'] == 'Kemi'
        vocab.at[i,'subject'] = 'Kemi'

    elif row['parent'] == '22869688-0a27-11eb-b4ba-0ae95472d63c':
        row['subject'] == 'Matematik'
        vocab.at[i,'subject'] = 'Matematik'

    elif row['parent'] == '28849010-0a2c-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Moderna språk'

    elif row['parent'] == '25bb3721-0ee4-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Modersmål -  utom nationella minoritetsspråk'

    elif row['parent'] == '0606161a-0ee6-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Modersmål - finska som nationellt minoritetsspråk' 

    elif row['parent'] == 'd905e054-0ee9-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Modersmål - jiddisch som nationellt minoritetsspråk'

    elif row['parent'] == '3204d60e-0eed-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Modersmål - meänkieli som nationellt minoritetsspråk'

    elif row['parent'] == 'a2cf300b-0f72-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Modersmål - romani chib som nationellt minoritetsspråk'

    elif row['parent'] == 'b0edd8d4-0e17-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Musik'

    elif row['parent'] == '5d67982a-0e19-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Religionskunskap'

    elif row['parent'] == '309e1eeb-0e1b-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Samhällskunskap'

    elif row['parent'] == '4dd9fa45-0e1e-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Slöjd'

    elif row['parent'] == 'c2981d82-0e20-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Svenska som andraspråk'

    elif row['parent'] == '978b37aa-0ede-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Teckenspråk för hörande'

    elif row['parent'] == 'f84f4062-0ee0-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Teknik'

for i, row in vocab.iterrows():
    if row['subject'] == "":
        vocab = vocab.drop(i, axis=0)

print(vocab)