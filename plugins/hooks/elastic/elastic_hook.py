from airflow.plugins_manager import AirflowPlugin
from airflow.hooks.base import BaseHook

from elasticsearch import Elasticsearch

class ElasticHook(BaseHook):
    def __init__(self, conn_id='elastic_default', *args, **kwargs):
        super().__init__(*args, **kwargs) #Initialize the base hook
        conn = self.get_connection(conn_id) #Get the connection corresponding to the connection ID `elastic_default`

        conn_config = {}
        hosts = []

        if conn.host:
            hosts = conn.host.split(',')
        if conn.port:
            conn_config['port'] = int(conn.port)
        if conn.login:
            conn_config['http_auth'] = (conn.login, conn.password)

        #Initialize the ElasticSearch Hook
        self.es = Elasticsearch(hosts, **conn_config)
        self.index = conn.schema

    def info(self):
        #Returns the information about the elastic search instance
        return self.es.info()
    
    def set_index(self, index):
        self.index = index

    def add_doc(self, index, doc_type, doc):
        #Adds the data to elastic search at specific index
        self.set_index(index)
        res = self.es.index(index=index, doc_type=doc_type, doc=doc)
        return res

class AirlfowElasticPlugin(AirflowPlugin):
    name = 'elastic'
    hooks = [ElasticHook]