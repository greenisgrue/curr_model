from skolmedia_client.elastic_client import ElasticClient

from gensim.models.keyedvectors import KeyedVectors
from elasticsearch.helpers import scan
import json
import csv
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm
from math import floor
import pickle

from process_data.dictionary import get_dictionary
from process_data import clean_df


class Skolfilm:

    __prod_search_source = [
        "metadata",
        "product.title",
        "product.surtitle",
        "product.summary",
        "product.description",
        "product.language",
        "product.year",
        "product.thumbnail",
        "streaming.format",
        "streaming.mediaid",
        "query",
        "keywords.subject",
        "keywords.freetext",
        "keywords.tags",
        "keywords.barn",
        "keywords.sao",
        "audience.level",
        "relations.versions",
        "metadata.modified"
    ]

    def __init__(self):
        self.es = ElasticClient().connection
        self.word_vectors = KeyedVectors.load('massive_data/word_vector_models/coNLL17_vectors.kv')
        self.dictionary = get_dictionary()


    def __map_products(self, product):
        return {
            "uid": product["_source"]["metadata"]["uid"],
            "modified": product["_source"]["metadata"]["modified"],
            "versions": product["_source"]["relations"]["versions"],
            "subject": ", ".join(product["_source"]["keywords"]["subject"]),
            "audience": ", ".join(product["_source"]["audience"]["level"]),
            "thumbnail": product["_source"]["product"]["thumbnail"]["medium"],
            "summary": product["_source"]["product"]["summary"].replace('\n', ""),
            "surtitle": product["_source"]["product"]["surtitle"],
            "year": product["_source"]["product"]["year"],
            "description": product["_source"]["product"]["description"].replace('\n', ""),
            "title": product["_source"]["product"]["title"],
            "streaming_format": product["_source"]["streaming"]["format"],
            "language": ", ".join(product["_source"]["query"]["language"]),
            "query_freetext": " ".join(product["_source"]["query"]["freetext"].split(",")).replace("\n", ""),
            "keyword_tags": " ".join(product["_source"]["query"]["tags"]).replace("\n", ""),
            "keywords": ", ".join(product["_source"]["query"]["keywords"]).replace("\n", ""),
            "freetext": ", ".join(product["_source"]["keywords"]["freetext"].split(",")).replace("\n", ""),
            "tags": ", ".join(product["_source"]["keywords"]["tags"]).replace("\n", ""),
            "barn": ", ".join(product["_source"]["keywords"]["barn"]).replace("\n", ""),
            "sao": ", ".join(product["_source"]["keywords"]["sao"]).replace("\n", ""),
        }


    def get_data_structures(self, index):
        ur_prod = self.__get_first_ten_from_index(index)
        self.__write_to_json(
            ur_prod, f'info/{index}_data_structure.json')

    def get_all_media(self, index, limit, write_to_json=False, write_to_csv=False):
        results = self.__get_all_from_index(
            index,
            self.__prod_search_source,
            limit,
        )
        data = list(map(self.__map_products, results))
        if write_to_json:
            self.__write_to_json(
                results,
                f'massive_data/stored_data/{index}.json'
            )
        if write_to_csv:
            self.__write_to_csv(
                data,
                f"massive_data/stored_data/{index}.csv",
                data[0].keys(),
            )
        return data

    def get_interval(self, start, end, index, limit, write_to_json=False, write_to_csv=True):
        if start is None and end is None:
            start = datetime.now() - timedelta(1)
            start = start.strftime("%Y-%m-%d %H:%M:%S")

            end = datetime.now()
            end = end.strftime("%Y-%m-%d %H:%M:%S")

        format = "%Y-%m-%d %H:%M:%S"
        try: 
            datetime.strptime(start, format)
            datetime.strptime(end, format)
        except:
            print("Ange tidsstämpel i formatet YYYY-MM-dd HH:mm:ss")
            return

        response = self.es.search(
            index=index,
            scroll="2m",
            size=limit,
            body={"query": {"range": {"metadata.modified": {"gte": start, "lte": end}}}}
        )   
            
        data = list(map(self.__map_products, response["hits"]["hits"]))
        if data:
            if write_to_json:
                self.__write_to_json(
                    response["hits"]["hits"],
                    f'massive_data/stored_data/interval.csv'
                )
            if write_to_csv:
                new_df = self.__write_to_csv(
                    data,
                    f"massive_data/stored_data/interval.csv",
                    data[0].keys(),
                )
        return data

    def merge_df(self, index):
        full_df = pd.read_csv(f"massive_data/stored_data/{index}_cleaned.csv", sep=',', engine='python')
        new_df = pd.read_csv(f"massive_data/stored_data/interval_cleaned.csv", sep=',', engine='python')
        
        complete_df = full_df.merge(new_df, how='outer')
        complete_df.to_csv(f"./massive_data/stored_data/{index}_cleaned.csv", index=False)

    def run_model(self, start, end, index, exists):
        full_df = pd.read_csv(f"massive_data/stored_data/{index}.csv", engine='python')

        if start is None and end is None:
            date_time_start = datetime.now() - timedelta(1)
            date_time_end = datetime.now()
        elif start == "all" and end == "all":
            self.__iterate_model(index, full_df)
            return 
        else:
            date_time_start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
            date_time_end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")

        columns = list(full_df.columns)
        matches_df = pd.DataFrame(columns=columns)

        for i, row in full_df.iterrows():
            date_time_obj = datetime.strptime(row['modified'], "%Y-%m-%d %H:%M:%S")
            if (date_time_obj > date_time_start) and (date_time_obj < date_time_end):
                matches_df.loc[len(matches_df)] = row

        self.__iterate_model(index, matches_df, exists)
        return


    def __iterate_model(self, index, df, exists):
        from models.word2vec import W2v
    
        list_of_uid = df['~uid'].tolist()
        model_results = pd.DataFrame(columns=['uid', 'result', 'title', 'surtitle', 'subject', 'audience', 'keywords', 'thumbnail', 'description'])

        for uid in tqdm(list_of_uid):
            run_model = W2v(index)
            uid = uid.strip('~')
            result = run_model.predict_CI(uid)
            model_results = model_results.append({'uid':uid, 'result':result, 'title':run_model.title, 'surtitle':run_model.surtitle, 'subject':run_model.subject, 'audience':run_model.audience, 'keywords':run_model.keywords, 'keywords':run_model.keywords, 'thumbnail':run_model.thumbnail, 'description':run_model.description}, ignore_index=True)

        if exists == True:
            with open(f'massive_data/stored_data/pickles/model_pickle.pickle', 'rb') as f:
                loaded_main = pickle.load(f)
                f.close() 
                df_concat = pd.concat([model_results, loaded_main])
                merged_df = df_concat.drop_duplicates(subset=['uid'])
 
            with open('massive_data/stored_data/pickles/model_pickle.pickle', 'wb') as f:
                pickle.dump(merged_df, f)  
                f.close()
        else:
            with open('massive_data/stored_data/pickles/model_pickle.pickle', 'wb') as f:
                pickle.dump(model_results, f)  
                f.close()

    def __merge_df(self, to_merge_df, loaded_main):
        with open(f'massive_data/stored_data/pickles/model_pickle.pickle', 'rb') as f:
            loaded_main = pickle.load(f)
            df_concat = pd.concat([to_merge_df, loaded_main])
            df_concat = df_concat.drop_duplicates(subset=['uid'])
            return df_concat


    def __write_to_json(self, data, path):
        with open(path, 'w', encoding="utf8") as f:
            json.dump(data, f)

    def __write_to_csv(self, data, path=None, fnames=None):
        #+["subtitles", "view_count", "mean_engagement",]
        with open(path, "w", encoding="utf8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=list(fnames),
                quotechar='~',
                quoting=csv.QUOTE_ALL
            )
            writer.writeheader()
            for item in data:
                writer.writerow(item)

    def __get_first_ten_from_index(self, index, filter_path=[]):
        if len(index) == 0:
            return
        response = self.es.search(
            index=index, body={"query": {"match_all": {}}}, filter_path=filter_path)
        return response["hits"]["hits"]

    def __get_all_from_index(self, index, source, limit):
        es_response = scan(
            self.es,
            index=index,
            query={
                "query": {
                    "match_all": {},
                },
                "_source": source,
            },
            size=floor(limit/10 + limit/15)
        )

        array = []
        for item in tqdm(es_response, total=limit):
            array.append(item)
            if limit and limit < len(array):
                break
        return array




