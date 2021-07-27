from elasticsearch import Elasticsearch


class ElasticClient:
    def __init__(self):
        cloud_id = "09cdf49b0a334cb893535a408fe497a1.eu-central-1.aws.cloud.es.io"
        user = "simwahl"
        password = "Rondell3434"

        self.connection = Elasticsearch(
        [cloud_id],
        http_auth=(user, password),
        scheme="https",
        port=443 
        )
    


