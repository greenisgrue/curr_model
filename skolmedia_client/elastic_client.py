from elasticsearch import Elasticsearch


class ElasticClient:
    def __init__(self):
        # cloud_id = "09cdf49b0a334cb893535a408fe497a1.eu-central-1.aws.cloud.es.io"
        # user = "simwahl"
        # password = "Rondell3434"

        cloud_id = "4666bf9491bce9cce5b8bb09dc269343.eu-central-1.aws.cloud.es.io"
        user = "elastic"
        password = "aqlO4LwnxAD3yCwhRVEInPcW" 

        self.connection = Elasticsearch(
        [cloud_id],
        http_auth=(user, password),
        scheme="https",
        port=443 
        )
    


