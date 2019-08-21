from databases import Databases
from preload import *
from util import *
from SPARQLWrapper import SPARQLWrapper, JSON, XML

def fzwc_produce_query(id, output_type = JSON):
    sparql_server = SPARQLWrapper(Databases.fzwc_server)

    produce_uri = f"http://www.fzwc.online/entity/produce/{wc_cache[id]}"
    clause = """
        SELECT DISTINCT ?property ?value
        WHERE {{
            <{produce_uri}> ?property ?value .
        }}
        #LIMIT 100
        #OFFSET 0
    """.format(produce_uri = produce_uri)

    return query_sparql(sparql_server, clause, output_type, produce_uri)

if __name__ == "__main__":
    load_sparql_internal_data()
    Printjson(fzwc_produce_query(1, JSON))