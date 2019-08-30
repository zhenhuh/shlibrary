from databases import Databases
from preload import *
from util4sparql import *
from SPARQLWrapper import SPARQLWrapper, JSON, XML, RDFXML

class Chronicle:
    def __init__(self):
        self.sparql_server = SPARQLWrapper(Databases.ecnu_server)

    @staticmethod
    def fzwc_fz_uri(id):
        return f"http://www.fzwc.online/ontologies/bibframe/Work/{fz_cache[id][0]}"

    @staticmethod
    def ecnu_fz_uri(id):
        return f"http://fangzhi.ecnu.edu.cn/entity/work/{fz_cache[id][1]}"

    def __query_ecnu_for_property_and_value(self, uri, isBlankNode = 0):
        clause = f"""
            SELECT DISTINCT ?property ?value
            WHERE {{
                <{uri}> ?property ?value FILTER (isBlank(?value) = {isBlankNode}) .
            }}
        """

        return query_sparql(self.sparql_server, clause, JSON, uri)

    def __get_blank_nodes(self, blank_nodes_part):
            blank_nodes = []
            for k, v in list(blank_nodes_part.values())[0].items():
                for k in v:
                    #print(k['value'])
                    blank_nodes.append(k['value'])

            return blank_nodes

    def __fuse(self, to_data, from_data):
        """ fuse dict_value1 and dict_value2 from {key: {dict_value1}} and {key: {dict_value2}}"""
        print("========================================")
        print(to_data)
        print("-----------")
        print(from_data)
        print("========================================")
        import os
        os.system("pause")
        return to_data

    def __query_ecnu_fz_data(self, uri):
        # 1. Get all non-blank node
        fz_data = self.__query_ecnu_for_property_and_value(uri)
        #print(fz_data)

        # 2. Get all blank node
        blank_nodes_part = self.__query_ecnu_for_property_and_value(uri, 1)
        #print(blank_nodes_part)

        # 3. Get all blank node recursively
        blank_nodes = self.__get_blank_nodes(blank_nodes_part)
        for bnode in blank_nodes:
            node_expend_data = self.__query_ecnu_fz_data(bnode)
            self.__fuse(fz_data, node_expend_data)

        return fz_data

    def query_fz_from_ecnu(self, id):
        fz_uri = Chronicle.ecnu_fz_uri(id)
        print(fz_uri)
        return self.__query_ecnu_fz_data(fz_uri)

if __name__ == "__main__":
    load_sparql_internal_data()

    fz = Chronicle()
    fz.query_fz_from_ecnu(0)