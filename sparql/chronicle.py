from sparql.databases import Databases
from sparql.preload import *
from sparql.util4sparql import *
from sparql.fusefactory import *
from SPARQLWrapper import SPARQLWrapper, JSON, RDFXML

base_fzwc_fz_uri = "http://www.fzwc.online/ontologies/bibframe/Work/"
base_ecnu_fz_uri = "http://fangzhi.ecnu.edu.cn/entity/work/"

class Chronicle:
    def __init__(self, output_type = JSON):
        self.ecnu_sparql_server = SPARQLWrapper(Databases.ecnu_server)
        self.fzwc_sparql_server = SPARQLWrapper(Databases.fzwc_server)
        self.fusefactory = FuseFactory(output_type)
        self.output_type = output_type

    @staticmethod
    def fzwc_fz_uri(id):
        uuids = fz_cache.get(id, None)
        if uuids is None:
            return base_fzwc_fz_uri
        return f"{base_fzwc_fz_uri}{uuids[0]}" if uuids[0] else ""

    @staticmethod
    def ecnu_fz_uri(id):
        uuids = fz_cache.get(id, None)
        if uuids is None:
            return base_ecnu_fz_uri
        return f"{base_ecnu_fz_uri}{uuids[1]}" if uuids[1] else ""

    def __query_fzwc_for_property_and_value(self, uri):
        if uri == "":
            raise RuntimeError("uri cannot be empty")

        if self.output_type in {JSON}:
            select = f"SELECT DISTINCT ?property ?value "
        elif self.output_type in {RDFXML}:
            select = f"""CONSTRUCT {{ <{uri}> ?property ?value . }}"""
        else:
            raise RuntimeError("Only support JSON and RDFXML")

        clause = f"""
            {select}
            WHERE {{
                <{uri}> ?property ?value .
            }}
        """
        return query_sparql(self.fzwc_sparql_server, clause, self.output_type, uri)

    def __query_ecnu_for_property_and_value(self, uri, needFilter = False, isBlankNode = 0):
        if uri == "":
            raise RuntimeError("uri cannot be empty")

        if self.output_type in {JSON}:
            select = f"SELECT DISTINCT ?property ?value "
        elif self.output_type in {RDFXML}:
            select = f"""CONSTRUCT {{ <{uri}> ?property ?value . }}"""
        else:
            raise RuntimeError("Only support JSON and RDFXML")

        filter = f"""FILTER (isBlank(?value) = {isBlankNode})""" if needFilter else ""
        clause = f"""
            {select}
            WHERE {{
                <{uri}> ?property ?value {filter} .
            }}
        """
        return query_sparql(self.ecnu_sparql_server, clause, self.output_type, uri)

    def __fuse_append(self, acc, bnode_ids):
        for bnode in bnode_ids:
            bnode_data = self.__query_ecnu_for_property_and_value(bnode)

            inner_bnodes = self.fusefactory.get_blank_nodes(bnode_data)
            self.__fuse_append(acc, inner_bnodes)
            
            self.fusefactory.fuse_append(acc, bnode_data)

    def query_ecnu_fz_data(self, id):
        ecnu_fz_uri = Chronicle.ecnu_fz_uri(id)
        if len(ecnu_fz_uri) > 0:
            json_data = self.__query_ecnu_for_property_and_value(ecnu_fz_uri)
            bnodes = FuseJson.get_blank_nodes(list(json_data.values())[0])
            self.__fuse_append(json_data, bnodes)
            return json_data
        else:
            return {"error" : "no uri found"}

    def query_fzwc_fz_data(self, id):
        fzwc_fz_uri = Chronicle.fzwc_fz_uri(id)
        if len(fzwc_fz_uri) > 0:
            return self.__query_fzwc_for_property_and_value(fzwc_fz_uri)
        else:
            return {"error" : "no uri found"}

    def query_fz_data_from_uuid(self, fz_uuid):
        def find_id(internal_uuid):
            for id, (fz, ecnu) in fz_cache.items():
                if fz == fz_uuid:
                    return id
            return -1

        id = find_id(fz_uuid)
        ecnu_fz_uri = Chronicle.ecnu_fz_uri(id)
        fzwc_fz_uri = Chronicle.fzwc_fz_uri(id)

        return self.__query_fz_data(ecnu_fz_uri, fzwc_fz_uri)

    def query_fz_data_from_id(self, id):
        ecnu_fz_uri = Chronicle.ecnu_fz_uri(id)
        fzwc_fz_uri = Chronicle.fzwc_fz_uri(id)

        return self.__query_fz_data(ecnu_fz_uri, fzwc_fz_uri)

    def __query_fz_data(self, ecnu_fz_uri, fzwc_fz_uri):
        try:
            # 1. Get all nodes
            fz_data_from_fzwc = self.__query_fzwc_for_property_and_value(fzwc_fz_uri)

            if ecnu_fz_uri:
                fz_data_from_ecnu = self.__query_ecnu_for_property_and_value(ecnu_fz_uri)
                if len(fz_data_from_ecnu) > 0:
                    # 2. Fuse ecnu data into fzwc data, consume fzwc first for the samme properties
                    fused_data, bnodes_after_fuse = self.fusefactory.fuse(fz_data_from_fzwc, fz_data_from_ecnu)

                    # 3. Append bnodes
                    self.__fuse_append(fused_data, bnodes_after_fuse)

                    return fused_data
            else:
                # 2. not data from ecnu, just return fzwc data
                return fz_data_from_fzwc

        except RuntimeError as e:
            return {"error" : str(e)}
        except Exception as e:
            return {"error" : f"wrong fz data received. detail msg: {str(e)}"}

if __name__ == "__main__":
    load_sparql_internal_data()

    fz = Chronicle(RDFXML)
    #Printjson(fz.query_fz_data_from_id(39))
    print(fz.query_fz_data_from_id(39))