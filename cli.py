import sys
import pandas as pd

from process_data import clean_df


# Get data structure of specific index. Is saved in info folder and contains 10 entries in the given index. 
# As default UR production index is used. 
def data_struct(index="search_ur_20210722"):
    from skolmedia_client.skolfilm_client import Skolfilm
    client = Skolfilm()
    client.get_data_structures(index=index)

# Fetch all data in a given index. Data is cleaned and stored as a csv-file in stored_data folder. 
def fetch_all_media(data_limit=25000, index="search_ur_20210722"):
    from skolmedia_client.skolfilm_client import Skolfilm
    if type(data_limit) != int:
        data_limit = int(data_limit)
    client = Skolfilm()
    client.get_all_media(index=index, limit=data_limit, write_to_csv=True)
    clean_df.clean(index)


# Fetch data in a given time interval. Data is cleaned and merged with its main csv-file in stored_data folder. 
def fetch_media_time_interval(start_date=None, end_date=None, data_limit=1000, index="search_ur_20210722"):
    from skolmedia_client.skolfilm_client import Skolfilm
    client = Skolfilm()
    client.get_interval(start_date, end_date, index=index, limit=data_limit, write_to_csv=True)
    clean_df.clean('interval')
    client.merge_new(index)


if __name__ == '__main__':
    globals()[sys.argv[1]](*sys.argv[2:])