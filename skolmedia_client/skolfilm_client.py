from skolmedia_client.elastic_client import ElasticClient

from elasticsearch.helpers import scan
import json
import csv
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm
from math import floor

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
        "relations.versions"
    ]

    def __init__(self):
        self.es = ElasticClient().connection

    def __map_products(self, product):
        return {
            "uid": product["_source"]["metadata"]["uid"],
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

    def get_interval(self, start, end, index, limit, write_to_json=False, write_to_csv=False):
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
                    f'massive_data/stored_data/interval.json'
                )
            if write_to_csv:
                new_df = self.__write_to_csv(
                    data,
                    f"massive_data/stored_data/interval.csv",
                    data[0].keys(),
                )
        return data

    def merge_new(self, index):
        full_df = pd.read_csv(f"massive_data/stored_data/{index}_cleaned.csv", sep=',', engine='python')
        new_df = pd.read_csv(f"massive_data/stored_data/interval_cleaned.csv", sep=',', engine='python')
        
        complete_df = full_df.merge(new_df, how='outer')
        complete_df.to_csv(f"./massive_data/stored_data/{index}_cleaned.csv", index=False)


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




