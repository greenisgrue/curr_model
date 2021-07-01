import pandas as pd
import re

full_vocab = pd.read_csv('../massive_data/stored_data/vocabularies.csv')
vocab = pd.read_csv('../massive_data/stored_data/vocabularies.csv')
vocab['subject'] = ""
vocab['audience'] = ""
vocab['title'] = ""
vocab['CI'] = ""

def include_CI_titles(vocab, full_vocab):
    substring_list = ['1-3', '4-6', '7-9']
    for index, row in vocab.iterrows():
        target = full_vocab[full_vocab['uuid'] == row['parent']]
        try: 
            CI_title = target.iloc[0]['value']
            if not any(substring in CI_title for substring in substring_list):
                vocab.at[index, 'title'] = CI_title
                vocab.at[index, 'CI'] = vocab.at[index, 'value']
                #vocab.at[index, 'value'] = vocab.at[index, 'title'] + '. ' + vocab.at[index, 'value']
            else:
                vocab = vocab.drop(index, axis=0)
        except:
            continue

    return vocab

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

    elif row['parent'] == 'c59fa0ce-0a2c-11eb-b4ba-0ae95472d63c' or row['parent'] == '9d95d011-0a2e-11eb-b4ba-0ae95472d63c' or row['parent'] == 'a067b695-0a2e-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Moderna språk'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == 'f4e236d4-0a2e-11eb-b4ba-0ae95472d63c' or row['parent'] == 'f84ded72-0a2e-11eb-b4ba-0ae95472d63c' or row['parent'] == 'fd0eb9ee-0a2e-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Moderna språk'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

    elif row['parent'] == 'd3c2ae3c-0ee4-11eb-b4ba-0ae95472d63c' or row['parent'] == 'b3cef3f4-0ee4-11eb-b4ba-0ae95472d63c' or row['parent'] == 'd13a0e28-0ee4-11eb-b4ba-0ae95472d63c' or row['parent'] == 'cc60023c-0ee4-11eb-b4ba-0ae95472d63c' or row['parent'] == 'ced0cc1b-0ee4-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Modersmål -  utom nationella minoritetsspråk'
        vocab.at[i,'audience'] = 'Grundskola 1-3'

    elif row['parent'] == '1ec5c37a-0ee5-11eb-b4ba-0ae95472d63c' or row['parent'] == '1459c8ca-0ee5-11eb-b4ba-0ae95472d63c' or row['parent'] == '1c0463ed-0ee5-11eb-b4ba-0ae95472d63c' or row['parent'] == '16bf89b4-0ee5-11eb-b4ba-0ae95472d63c' or row['parent'] == '197831e3-0ee5-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Modersmål -  utom nationella minoritetsspråk'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == '76bc7ec5-0ee5-11eb-b4ba-0ae95472d63c' or row['parent'] == '641f6d4e-0ee5-11eb-b4ba-0ae95472d63c' or row['parent'] == '70a4f2af-0ee5-11eb-b4ba-0ae95472d63c' or row['parent'] == '6ba85417-0ee5-11eb-b4ba-0ae95472d63c' or row['parent'] == '6df1d438-0ee5-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Modersmål -  utom nationella minoritetsspråk'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

    elif row['parent'] == '9fa44e45-0ee6-11eb-b4ba-0ae95472d63c' or row['parent'] == 'aa316d2d-0ee6-11eb-b4ba-0ae95472d63c' or row['parent'] == 'aca8dad8-0ee6-11eb-b4ba-0ae95472d63c' or row['parent'] == 'a3afaa68-0ee6-11eb-b4ba-0ae95472d63c' or row['parent'] == 'a7429dd4-0ee6-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Modersmål -  finska som nationellt minoritetsspråk'
        vocab.at[i,'audience'] = 'Grundskola 1-3'

    elif row['parent'] == 'f0bda59b-0ee6-11eb-b4ba-0ae95472d63c' or row['parent'] == 'f6ec8448-0ee6-11eb-b4ba-0ae95472d63c' or row['parent'] == 'f920ceed-0ee6-11eb-b4ba-0ae95472d63c' or row['parent'] == 'f1908a6e-0ee6-11eb-b4ba-0ae95472d63c' or row['parent'] == 'f48d6a46-0ee6-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Modersmål -  finska som nationellt minoritetsspråk'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == '3ec0c6a3-0ee7-11eb-b4ba-0ae95472d63c' or row['parent'] == '48a54189-0ee7-11eb-b4ba-0ae95472d63c' or row['parent'] == '4b71fdd0-0ee7-11eb-b4ba-0ae95472d63c' or row['parent'] == '42a8c5d2-0ee7-11eb-b4ba-0ae95472d63c' or row['parent'] == '45c5aa52-0ee7-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Modersmål -  finska som nationellt minoritetsspråk'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

    elif row['parent'] == 'b05aecd7-0eed-11eb-b4ba-0ae95472d63c' or row['parent'] == 'b8705a8c-0eed-11eb-b4ba-0ae95472d63c' or row['parent'] == 'b3796ca9-0eed-11eb-b4ba-0ae95472d63c' or row['parent'] == 'b6156409-0eed-11eb-b4ba-0ae95472d63c' or row['parent'] == 'bc85c977-0eed-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Modersmål -  meänkieli som nationellt minoritetsspråk'
        vocab.at[i,'audience'] = 'Grundskola 1-3'

    elif row['parent'] == '0526f65d-0eee-11eb-b4ba-0ae95472d63c' or row['parent'] == '109dcdbf-0eee-11eb-b4ba-0ae95472d63c' or row['parent'] == '0aeb8cb1-0eee-11eb-b4ba-0ae95472d63c' or row['parent'] == '0dd5fba2-0eee-11eb-b4ba-0ae95472d63c' or row['parent'] == '161be1b2-0eee-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Modersmål -  meänkieli som nationellt minoritetsspråk'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == '5a6f86e8-0eee-11eb-b4ba-0ae95472d63c' or row['parent'] == '627ba476-0eee-11eb-b4ba-0ae95472d63c' or row['parent'] == '5cf49dff-0eee-11eb-b4ba-0ae95472d63c' or row['parent'] == '5f857562-0eee-11eb-b4ba-0ae95472d63c' or row['parent'] == '672a0a26-0eee-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Modersmål -  meänkieli som nationellt minoritetsspråk'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

    elif row['parent'] == '26aeb37b-0f73-11eb-b4ba-0ae95472d63c' or row['parent'] == '31b65fbb-0f73-11eb-b4ba-0ae95472d63c' or row['parent'] == '2f1785d6-0f73-11eb-b4ba-0ae95472d63c' or row['parent'] == 'fa0534f0-0f72-11eb-b4ba-0ae95472d63c' or row['parent'] == '2c45dc2f-0f73-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Modersmål -  romani chib som nationellt minoritetsspråk'
        vocab.at[i,'audience'] = 'Grundskola 1-3'

    elif row['parent'] == '7f1e1468-0f73-11eb-b4ba-0ae95472d63c' or row['parent'] == '8ad42b4c-0f73-11eb-b4ba-0ae95472d63c' or row['parent'] == '88369c31-0f73-11eb-b4ba-0ae95472d63c' or row['parent'] == '82aa9f89-0f73-11eb-b4ba-0ae95472d63c' or row['parent'] == '85f07dd8-0f73-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Modersmål -  romani chib som nationellt minoritetsspråk'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == 'ca0c95e8-0f73-11eb-b4ba-0ae95472d63c' or row['parent'] == 'd5cca42d-0f73-11eb-b4ba-0ae95472d63c' or row['parent'] == 'd18f4606-0f73-11eb-b4ba-0ae95472d63c' or row['parent'] == 'cc818148-0f73-11eb-b4ba-0ae95472d63c' or row['parent'] == 'cf2bd805-0f73-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Modersmål -  romani chib som nationellt minoritetsspråk'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

    elif row['parent'] == '455575e5-0e18-11eb-b4ba-0ae95472d63c' or row['parent'] == '4b14cc44-0e18-11eb-b4ba-0ae95472d63c' or row['parent'] == '48295361-0e18-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Musik'
        vocab.at[i,'audience'] = 'Grundskola 1-3'

    elif row['parent'] == '9a6ed734-0e18-11eb-b4ba-0ae95472d63c' or row['parent'] == 'a056e449-0e18-11eb-b4ba-0ae95472d63c' or row['parent'] == '9ce7a67e-0e18-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Musik'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == 'e786ac3f-0e18-11eb-b4ba-0ae95472d63c' or row['parent'] == 'ee6c7a15-0e18-11eb-b4ba-0ae95472d63c' or row['parent'] == 'eab093b3-0e18-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Musik'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

    elif row['parent'] == 'dab68e7d-0e19-11eb-b4ba-0ae95472d63c' or row['parent'] == 'ddb1a378-0e19-11eb-b4ba-0ae95472d63c' or row['parent'] == 'd7fbc499-0e19-11eb-b4ba-0ae95472d63c' or row['parent'] == 'e57b69ef-0e19-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Religionskunskap'
        vocab.at[i,'audience'] = 'Grundskola 1-3'

    elif row['parent'] == '8e3f3315-0e1a-11eb-b4ba-0ae95472d63c' or row['parent'] == '8a862213-0e1a-11eb-b4ba-0ae95472d63c' or row['parent'] == '8797dab0-0e1a-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Religionskunskap'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == 'd3c7c4ab-0e1a-11eb-b4ba-0ae95472d63c' or row['parent'] == 'd0349ef4-0e1a-11eb-b4ba-0ae95472d63c' or row['parent'] == 'cd73b5b2-0e1a-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Religionskunskap'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

    elif row['parent'] == 'b3193274-0e1c-11eb-b4ba-0ae95472d63c' or row['parent'] == 'b6544df3-0e1c-11eb-b4ba-0ae95472d63c' or row['parent'] == 'b05869cf-0e1c-11eb-b4ba-0ae95472d63c' or row['parent'] == 'b9bcc5f5-0e1c-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Samhällskunskap'
        vocab.at[i,'audience'] = 'Grundskola 1-3'

    elif row['parent'] == '3f3af851-0e1d-11eb-b4ba-0ae95472d63c' or row['parent'] == '498e326f-0e1d-11eb-b4ba-0ae95472d63c' or row['parent'] == '39bec798-0e1d-11eb-b4ba-0ae95472d63c' or row['parent'] == '466e6ba5-0e1d-11eb-b4ba-0ae95472d63c' or row['parent'] == '4342dd47-0e1d-11eb-b4ba-0ae95472d63c' or row['parent'] == '3cb12b08-0e1d-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Samhällskunskap'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == 'b0393927-0e1d-11eb-b4ba-0ae95472d63c' or row['parent'] == 'b933aa15-0e1d-11eb-b4ba-0ae95472d63c' or row['parent'] == 'ab06327c-0e1d-11eb-b4ba-0ae95472d63c' or row['parent'] == 'b69287e3-0e1d-11eb-b4ba-0ae95472d63c' or row['parent'] == 'b322b1e9-0e1d-11eb-b4ba-0ae95472d63c' or row['parent'] == 'adb4fb85-0e1d-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Samhällskunskap'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

    elif row['parent'] == '1a0a1a9a-0e1f-11eb-b4ba-0ae95472d63c' or row['parent'] == '173a3916-0e1f-11eb-b4ba-0ae95472d63c' or row['parent'] == '1db465e6-0e1f-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Slöjd'
        vocab.at[i,'audience'] = 'Grundskola 1-3'

    elif row['parent'] == '297efb67-0e1f-11eb-b4ba-0ae95472d63c' or row['parent'] == '26f35fc2-0e1f-11eb-b4ba-0ae95472d63c' or row['parent'] == '2cae9bd0-0e1f-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Slöjd'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == 'd1a4575b-0e1f-11eb-b4ba-0ae95472d63c' or row['parent'] == 'ce7e9307-0e1f-11eb-b4ba-0ae95472d63c' or row['parent'] == 'd47a4bed-0e1f-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Slöjd'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

    elif row['parent'] == '5f7bc14c-0e26-11eb-b4ba-0ae95472d63c' or row['parent'] == '4f6c1dd5-0e26-11eb-b4ba-0ae95472d63c' or row['parent'] == '5747fa60-0e26-11eb-b4ba-0ae95472d63c' or row['parent'] == '51c059ad-0e26-11eb-b4ba-0ae95472d63c' or row['parent'] == '544b7dbf-0e26-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Svenska'
        vocab.at[i,'audience'] = 'Grundskola 1-3'

    elif row['parent'] == 'ee7b7af3-0e26-11eb-b4ba-0ae95472d63c' or row['parent'] == 'e37c19a5-0e26-11eb-b4ba-0ae95472d63c' or row['parent'] == 'eb86640d-0e26-11eb-b4ba-0ae95472d63c' or row['parent'] == 'e5edfa02-0e26-11eb-b4ba-0ae95472d63c' or row['parent'] == 'e8c78391-0e26-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Svenska'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == '740923e3-0e27-11eb-b4ba-0ae95472d63c' or row['parent'] == '65fc392e-0e27-11eb-b4ba-0ae95472d63c' or row['parent'] == '70365f50-0e27-11eb-b4ba-0ae95472d63c' or row['parent'] == '68f059d5-0e27-11eb-b4ba-0ae95472d63c' or row['parent'] == '6c21b0cb-0e27-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Svenska'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

    elif row['parent'] == 'e34b9196-0e21-11eb-b4ba-0ae95472d63c' or row['parent'] == 'd7ef01a0-0e21-11eb-b4ba-0ae95472d63c' or row['parent'] == 'e05bf563-0e21-11eb-b4ba-0ae95472d63c' or row['parent'] == 'db16a690-0e21-11eb-b4ba-0ae95472d63c' or row['parent'] == 'dda1ce38-0e21-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Svenska som andraspråk'
        vocab.at[i,'audience'] = 'Grundskola 1-3'

    elif row['parent'] == '22c1431d-0e24-11eb-b4ba-0ae95472d63c' or row['parent'] == '15a68290-0e24-11eb-b4ba-0ae95472d63c' or row['parent'] == '1f341e1f-0e24-11eb-b4ba-0ae95472d63c' or row['parent'] == '1803b84f-0e24-11eb-b4ba-0ae95472d63c' or row['parent'] == '1c718b78-0e24-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Svenska som andraspråk'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == 'c35a9d75-0e24-11eb-b4ba-0ae95472d63c' or row['parent'] == 'b73d12c6-0e24-11eb-b4ba-0ae95472d63c' or row['parent'] == 'c043d349-0e24-11eb-b4ba-0ae95472d63c' or row['parent'] == 'ba3a9896-0e24-11eb-b4ba-0ae95472d63c' or row['parent'] == 'bd540582-0e24-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Svenska som andraspråk'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

    elif row['parent'] == 'b49da1ec-0edf-11eb-b4ba-0ae95472d63c' or row['parent'] == 'b148e354-0edf-11eb-b4ba-0ae95472d63c' or row['parent'] == 'b83640bd-0edf-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Teckenspråk för hörande'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == '88854c6f-0ee0-11eb-b4ba-0ae95472d63c' or row['parent'] == '858f437e-0ee0-11eb-b4ba-0ae95472d63c' or row['parent'] == '8c06fb98-0ee0-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Teckenspråk för hörande'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

    elif row['parent'] == 'c632bac1-0ee1-11eb-b4ba-0ae95472d63c' or row['parent'] == 'c0b8b03d-0ee1-11eb-b4ba-0ae95472d63c' or row['parent'] == 'c355d982-0ee1-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Teknik'
        vocab.at[i,'audience'] = 'Grundskola 1-3'

    elif row['parent'] == '09c6b7ff-0ee2-11eb-b4ba-0ae95472d63c' or row['parent'] == '0198c474-0ee2-11eb-b4ba-0ae95472d63c' or row['parent'] == '0637cfc0-0ee2-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Teknik'
        vocab.at[i,'audience'] = 'Grundskola 4-6'

    elif row['parent'] == '57c23cd9-0ee2-11eb-b4ba-0ae95472d63c' or row['parent'] == '50d7ab64-0ee2-11eb-b4ba-0ae95472d63c' or row['parent'] == '53b0c5d1-0ee2-11eb-b4ba-0ae95472d63c':
        vocab.at[i,'subject'] = 'Teknik'
        vocab.at[i,'audience'] = 'Grundskola 7-9'

for i, row in vocab.iterrows():
    if row['subject'] == "":
        vocab = vocab.drop(i, axis=0)


added_vocab = include_CI_titles(vocab, full_vocab)

added_vocab = added_vocab[['uuid', 'parent', 'title', 'subject', 'audience', 'CI', 'value']]
added_vocab.to_csv('../massive_data/stored_data/CI_vocab.csv')
