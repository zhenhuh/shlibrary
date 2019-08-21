from databases import Databases
from preload import *
from util import *
from SPARQLWrapper import SPARQLWrapper, JSON, XML

def fzwc_produce_query(id, output_type = JSON):
    sparql = SPARQLWrapper(Databases.fzwc_server)

    produce_uri = f"http://www.fzwc.online/entity/produce/{wc_cache[id]}"
    clause = """
        SELECT DISTINCT ?property ?value
        WHERE {{
            <{produce_uri}> ?property ?value .
        }}
        #LIMIT 100
        #OFFSET 0
    """.format(produce_uri = produce_uri)

    return {produce_uri: query_sparql(sparql, clause, output_type)}

if __name__ == "__main__":
    load_sparql_internal_data()
    Printjson(fzwc_produce_query(1, JSON))