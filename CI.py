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

    elif row['parent'] == 'fe5a33b2-0a0d-11eb-b4ba-0ae95472d63c' or row['parent'] == '084d72f0-0a0e-11eb-b4ba-0ae95472d63c' or row['parent'] == '01d3ac26-0a0e-11eb-b4ba-0ae95472d63c' or row['parent'] == 'fb0406ef-0a0d-11eb-b4ba-0ae95472d63c' or row['parent'] == '04ade330-0a0e-11eb-b4ba-0ae95472d63c':
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

    elif row['parent'] == '1ba2e4ed-0a16-11eb-b4ba-0ae95472d63c' or row['parent'] == '204c7fdd-0a16-11eb-b4ba-0ae95472d63c' or row['parent'] == 'ef240f41-0a15-11eb-b4ba-0ae95472d63c' or row['parent'] == '15397ad6-0a16-11eb-b4ba-0ae95472d63c' or row['parent'] == '0e7f4b65-0a16-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Fysik'
        vocab.at[i,'audience'] = 'Grundskola 1-3'

    elif row['parent'] == 'd8d6f9ba-0a17-11eb-b4ba-0ae95472d63c' or row['parent'] == 'dd43376a-0a17-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Fysik'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == '76139e1a-0a18-11eb-b4ba-0ae95472d63c' or row['parent'] == '774f4a12-0a18-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Fysik'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

    elif row['parent'] == '95104b9a-0a19-11eb-b4ba-0ae95472d63c' or row['parent'] == '99cc526e-0a19-11eb-b4ba-0ae95472d63c' or row['parent'] == '914da9e6-0a19-11eb-b4ba-0ae95472d63c' or row['parent'] == '9e089fee-0a19-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Geografi'
        vocab.at[i,'audience'] = 'Grundskola 1-3'

    elif row['parent'] == '5f9cf9b0-0a1b-11eb-b4ba-0ae95472d63c' or row['parent'] == '58b982ec-0a1b-11eb-b4ba-0ae95472d63c' or row['parent'] == '5cededc8-0a1b-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Geografi'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == 'bee090ec-0a1b-11eb-b4ba-0ae95472d63c' or row['parent'] == 'b8e11384-0a1b-11eb-b4ba-0ae95472d63c' or row['parent'] == 'bbb05b55-0a1b-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Geografi'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

    elif row['parent'] == '6f99d94d-0a1d-11eb-b4ba-0ae95472d63c' or row['parent'] == '1a6a67f7-0a1d-11eb-b4ba-0ae95472d63c' or row['parent'] == '6c4361fb-0a1d-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Hem- och konsumentkunskap'
        vocab.at[i,'audience'] = 'Grundskola 1-6'

    elif row['parent'] == 'b9e2aa8f-0a1d-11eb-b4ba-0ae95472d63c' or row['parent'] == 'b39b33c6-0a1d-11eb-b4ba-0ae95472d63c' or row['parent'] == 'b6ee4716-0a1d-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Hem- och konsumentkunskap'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

    elif row['parent'] == '0814d85f-0a20-11eb-b4ba-0ae95472d63c' or row['parent'] == 'fb3deb4c-0a1f-11eb-b4ba-0ae95472d63c' or row['parent'] == 'f8e667bb-0a1f-11eb-b4ba-0ae95472d63c' or row['parent'] == 'f63fde33-0a1f-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Historia'
        vocab.at[i,'audience'] = 'Grundskola 1-3'

    elif row['parent'] == 'fa8dad03-0a20-11eb-b4ba-0ae95472d63c' or row['parent'] == 'f1e8bb98-0a20-11eb-b4ba-0ae95472d63c' or row['parent'] == 'f5cb5778-0a20-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Historia'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == '75cf47c2-0a21-11eb-b4ba-0ae95472d63c' or row['parent'] == '71a988d7-0a21-11eb-b4ba-0ae95472d63c' or row['parent'] == '6be2e918-0a21-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Historia'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

    elif row['parent'] == '318afabc-0a23-11eb-b4ba-0ae95472d63c' or row['parent'] == '363aba3e-0a23-11eb-b4ba-0ae95472d63c' or row['parent'] == '2ec4b88f-0a23-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Idrott och hälsa'
        vocab.at[i,'audience'] = 'Grundskola 1-3'

    elif row['parent'] == '92993c07-0a23-11eb-b4ba-0ae95472d63c' or row['parent'] == '956a4911-0a23-11eb-b4ba-0ae95472d63c' or row['parent'] == '8fdaa70e-0a23-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Idrott och hälsa'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == 'f7f2091c-0a23-11eb-b4ba-0ae95472d63c' or row['parent'] == 'fb951078-0a23-11eb-b4ba-0ae95472d63c' or row['parent'] == 'f4f7341d-0a23-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Idrott och hälsa'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

    elif row['parent'] == '4ab881f6-0ee3-11eb-b4ba-0ae95472d63c' or row['parent'] == '4489ec09-0ee3-11eb-b4ba-0ae95472d63c' or row['parent'] == '4776d9bc-0ee3-11eb-b4ba-0ae95472d63c' or row['parent'] == '41f44cf1-0ee3-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Judiska studier'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

    elif row['parent'] == '187bf3f1-0a26-11eb-b4ba-0ae95472d63c' or row['parent'] == '153c9625-0a26-11eb-b4ba-0ae95472d63c' or row['parent'] == '1b6eb777-0a26-11eb-b4ba-0ae95472d63c' or row['parent'] == '1ebed17a-0a26-11eb-b4ba-0ae95472d63c' or row['parent'] == '117facc5-0a26-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Kemi'
        vocab.at[i,'audience'] = 'Grundskola 1-3'

    elif row['parent'] == '6fd43047-0a26-11eb-b4ba-0ae95472d63c' or row['parent'] == '73c8cc79-0a26-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Kemi'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == 'b5815331-0a26-11eb-b4ba-0ae95472d63c' or row['parent'] == 'b97c0719-0a26-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Kemi'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

    elif row['parent'] == 'befa637a-0a28-11eb-b4ba-0ae95472d63c' or row['parent'] == 'ca22d9de-0a28-11eb-b4ba-0ae95472d63c' or row['parent'] == 'da87e6ee-0a28-11eb-b4ba-0ae95472d63c' or row['parent'] == 'd45a31e4-0a28-11eb-b4ba-0ae95472d63c' or row['parent'] == 'd07e49b4-0a28-11eb-b4ba-0ae95472d63c' or row['parent'] == 'c3c0fb5d-0a28-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Matematik'
        vocab.at[i,'audience'] = 'Grundskola 1-3'

    elif row['parent'] == '9ecc6fe4-0a29-11eb-b4ba-0ae95472d63c' or row['parent'] == 'a24aceac-0a29-11eb-b4ba-0ae95472d63c' or row['parent'] == 'ab01e193-0a29-11eb-b4ba-0ae95472d63c' or row['parent'] == 'ab01e193-0a29-11eb-b4ba-0ae95472d63c' or row['parent'] == 'a5364813-0a29-11eb-b4ba-0ae95472d63c' or row['parent'] == '9b4656cb-0a29-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Matematik'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == '47cde506-0a2a-11eb-b4ba-0ae95472d63c' or row['parent'] == '4bc1d343-0a2a-11eb-b4ba-0ae95472d63c' or row['parent'] == '5554f1a4-0a2a-11eb-b4ba-0ae95472d63c' or row['parent'] == '52d4af09-0a2a-11eb-b4ba-0ae95472d63c' or row['parent'] == '4f7ab135-0a2a-11eb-b4ba-0ae95472d63c' or row['parent'] == '455a29cb-0a2a-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Matematik'
        vocab.at[i,'audience'] = 'Grundskola 7-9'


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