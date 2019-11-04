from sparql.databases import Databases
from sparql.preload import *
from sparql.util4sparql import *
from SPARQLWrapper import SPARQLWrapper, JSON, XML, RDFXML

def fzwc_sparql_query(produce_uri, clause, output_type):
    sparql_server = SPARQLWrapper(Databases.fzwc_server)
    return query_sparql(sparql_server, clause, output_type, produce_uri)

def fzwc_produce_data_uri(id):
    base_uri = "http://www.fzwc.online/entity/produce/"
    uuid = wc_cache.get(id, None)
    if uuid is None:
        return f"{base_uri}{id}" # id is uuid
    return f"{base_uri}{wc_cache[id]}"

def fzwc_produce_data_select_from_id(id, output_type = JSON):
    produce_uri = fzwc_produce_data_uri(id)
    return fzwc_produce_data_select(produce_uri, output_type)

def fzwc_produce_data_select_from_uuid(uuid, output_type = JSON):
    produce_uri = fzwc_produce_data_uri(uuid)
    return fzwc_produce_data_select(produce_uri, output_type)

def fzwc_produce_data_construct_from_id(id, output_type = RDFXML):
    produce_uri = fzwc_produce_data_uri(id)
    return fzwc_produce_data_construct(produce_uri, output_type)

def fzwc_produce_data_construct_from_uuid(uuid, output_type = RDFXML):
    produce_uri = fzwc_produce_data_uri(uuid)
    return fzwc_produce_data_construct(produce_uri, output_type)

def fzwc_produce_data_select(produce_uri, output_type = JSON):
    clause = f"""
        SELECT DISTINCT ?property ?value
        WHERE {{
            <{produce_uri}> ?property ?value .
        }}
        #LIMIT 100
        #OFFSET 0
    """

    return fzwc_sparql_query(produce_uri, clause, output_type)

def fzwc_produce_data_construct(produce_uri, output_type = RDFXML):

    produce_uri = fzwc_produce_data_uri(id)
    clause = f"""
        CONSTRUCT {{
            <{produce_uri}> ?p ?o .
        }}
        WHERE {{
            <{produce_uri}> ?p ?o .
        }}"""

    return fzwc_sparql_query(produce_uri, clause, output_type)

if __name__ == "__main__":
    load_sparql_internal_data()
    Printjson(fzwc_produce_data_construct_from_id(1))