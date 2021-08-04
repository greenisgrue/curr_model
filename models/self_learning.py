import pandas as pd
import numpy as np
from tqdm import tqdm

import pickle
import pymongo
import statistics


class SelfLearning:
    def __init__(self, matrix_exist):
        self.CI = pd.read_csv("./massive_data/stored_data/CI_vocab_including_titles.csv")
        self.content = pd.read_csv("./massive_data/stored_data/search_ur_20210731_cleaned.csv")
        if matrix_exist:
            self.weights_matrix = pd.read_csv("./massive_data/stored_data/self_learning_matrix.csv")

    # Function that creates a matrix with keywords as columns and "centralt innehåll" as rows. The values in each cell is set to 1.
    def create_matrix(self):
        rows = [] 
        cols = ['CI']
        for i, row in self.CI.iterrows():
            rows.append([row['uuid']]) 

        for i, row in self.content.iterrows():
            for k in row['keywords'].split(', '):
                if k not in cols:
                    k = k.lower()
                    k = k.strip()
                    cols.append(k)

        df = pd.DataFrame(1, index=np.arange(len(rows)), columns=cols)
        df = df.astype(float)
        df = df.astype({"CI": str})
        for i, row in df.iterrows():
            df.at[i,'CI'] = rows[i][0]
        df.to_csv("./massive_data/stored_data/self_learning_matrix.csv", index=False)

    # Function for adjusting the weights in the self learning matrix. If a user rates a "centralt innehåll" point positively the keywords
    # associated with its contents metadata gains some score. For negative ratings a corresponding negative score is added to associated keywords. 
    def adjust_weights(self):
        from datetime import datetime, timedelta
        self.create_matrix()
        connection_url = 'mongodb+srv://dbUser:dbUserPassword@cluster0.ifjkb.mongodb.net/CI_ratings?retryWrites=true&w=majority'
        client = pymongo.MongoClient(connection_url)
        db = client.get_database('CI_ratings')
        ratings = db.ratings_opti
        for item in tqdm(ratings.find()):
            for i in item.get('ratings'):
                if type(i.get('rating')) != type(None):
                    # Determine how much each rating affects content keywords weight in self learning matrix
                    weight = (i.get('rating'))/10
                    keywords = item.get('keywords').split(', ')
                    for k in keywords:
                        k = k.lower()
                        k = k.strip()
                        index = self.weights_matrix.index[self.weights_matrix['CI'] == i.get('uid')].tolist()
                        self.weights_matrix.at[index[0], k] += weight

        self.weights_matrix.to_csv("./massive_data/stored_data/self_learning_matrix.csv", index=False)
                        

    # A function that applies a formula caluclating how much the self learning factor should affect a given "centralt innehåll"
    def update_score(self, uuid, keywords, current_score):
        current_weights = []
        index = self.weights_matrix.index[self.weights_matrix['CI'] == uuid].tolist()
        keywords = keywords.split(', ')
        keywords = [i for i in keywords if i]
        for k in keywords:
            k = k.lower()
            k = k.strip()
            current_weights.append(self.weights_matrix.at[index[0], k])

        avg_weigths = statistics.fmean(current_weights)
        if avg_weigths < 1.0:
            return -(current_score*(2-avg_weigths)-current_score)
        elif 1.0 <= avg_weigths < 2.0:
            return (1-current_score)*avg_weigths-(1-current_score)
        elif avg_weigths >= 2.0:
            return (1-current_score)

    # A function that uses update_score function on all content.
    def update_all_score(self):
        with open(f'massive_data/stored_data/pickles/model_pickle.pickle', 'rb') as f:
            loaded_main = pickle.load(f)

        for i, row in tqdm(loaded_main.iterrows()):
            for key, value in row['result']:
                self_learn_score = self.update_score(key, row['keywords'], value.get('value'))
                adjusted_score = value.get('value') + self_learn_score
                formatted_string = "{:.3f}".format(adjusted_score)
                adjusted_score = float(formatted_string)
                value['adjusted_value'] = adjusted_score

            sorted_dict = sorted(row['result'], reverse=True, key = lambda x: x[1]['adjusted_value'])
            row['result'] = sorted_dict    
        
        with open('massive_data/stored_data/pickles/model_pickle.pickle', 'wb') as f:
            pickle.dump(loaded_main, f)  
            f.close()


