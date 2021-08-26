import sys
import pickle
import pymongo
import pandas as pd
from tqdm import tqdm

from process_data import clean_df


# Get data structure of specific index. Is saved in info folder and contains 10 entries in the given index. 
# As default UR production index is used. 
def data_struct(index="search_ur_20210731"):
    from skolmedia_client.skolfilm_client import Skolfilm
    client = Skolfilm()
    client.get_data_structures(index=index)

# Fetch all data in a given index. Data is cleaned and stored as a csv-file in stored_data folder. 
def fetch_all_media(data_limit=25000, index="search_ur_20210731"):
    from skolmedia_client.skolfilm_client import Skolfilm
    if type(data_limit) != int: 
        data_limit = int(data_limit)
    client = Skolfilm()
    client.get_all_media(index=index, limit=data_limit, write_to_json=True)
    print("Fetch all media: completed")
    clean_df.clean(index)
    print("Content is cleaned")

# Fetch data in a given time interval. Data is cleaned and merged with its main csv-file in stored_data folder.
# If no start or end date is set the last 24 hours will be used as default. 
def fetch_media(start_date=None, end_date=None, data_limit=10000, index="search_ur_20210731"):
    from skolmedia_client.skolfilm_client import Skolfilm
    if type(data_limit) != int: 
        data_limit = int(data_limit)
    client = Skolfilm()
    data = client.get_interval(start_date, end_date, index=index, limit=data_limit, write_to_csv=True)
    if start_date == None and end_date == None:
        print(f"Fetch media in interval last 24 hours completed")
    elif start_date == 'all' and end_date == 'all':
        print(f"Fetch media in full interval completed")
    else:
        print(f"Fetch media in interval {start_date} to {end_date} completed")
    if data:
        clean_df.clean(index)
        client.merge_df(index)
        print("Content is cleaned")


# Run model over media content and save in df as pickle. To run over all content available use parameters "all" "all", for latest 24 hours
# leave parameters blank and for specific dates use format "YYYY-mm-dd HH:MM:SS"
def get_model_data(start_date=None, end_date=None, exists=True, index="search_ur_20210731_cleaned"):
    from skolmedia_client.skolfilm_client import Skolfilm
    client = Skolfilm()
    client.run_model(start_date, end_date, index, exists)


# Run to update self learning matrix with feedback from database. This is needed for new feedback to be considered when adjusting weights
# for "centralt innehåll" based on user feedback. 
def update_self_learning_matrix():
    from models.self_learning import SelfLearning
    self_learn = SelfLearning(False)
    self_learn.adjust_weights()


# When self learning matrix is updated all content also needs to get the updated weights. update_all_score runs update_score for all 
# available content. 
def get_recalculated_values():
    from models.self_learning import SelfLearning
    self_learn = SelfLearning(True)
    self_learn.update_all_score()
 
def reset_matrix():
    from models.self_learning import SelfLearning
    client = SelfLearning(False)
    client.create_matrix()
    print('Self learning matrix has been created')


if __name__ == '__main__':
    globals()[sys.argv[1]](*sys.argv[2:])