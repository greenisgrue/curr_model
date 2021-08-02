import sys
import pickle
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
    # if type(data_limit) != int:
    #     data_limit = int(data_limit)
    client = Skolfilm()
    client.get_all_media(index=index, limit=data_limit, write_to_csv=True)
    clean_df.clean(index)

# Fetch data in a given time interval. Data is cleaned and merged with its main csv-file in stored_data folder.
# If no start or end date is set the last 24 hours will be used as default. 
def fetch_media_time_interval(start_date=None, end_date=None, data_limit=1000, index="search_ur_20210731"):
    from skolmedia_client.skolfilm_client import Skolfilm
    client = Skolfilm()
    client.get_interval(start_date, end_date, index=index, limit=data_limit, write_to_csv=True)
    clean_df.clean('interval')
    client.merge_df(index)

# Run model over media content and save in df as pickle. To run over all content available use parameters "all" "all", for latest 24 hours
# leave parameters blank and for specific dates use format "YYYY-mm-dd HH:MM:SS"
def get_model_data(start_date=None, end_date=None, index="search_ur_20210731_cleaned"):
    from skolmedia_client.skolfilm_client import Skolfilm
    client = Skolfilm()
    client.run_model(start_date, end_date, index)



if __name__ == '__main__':
    globals()[sys.argv[1]](*sys.argv[2:])