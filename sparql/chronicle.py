from sparql.databases import Databases
from sparql.preload import *
from sparql.prefix import *
from sparql.util4sparql import *
from sparql.fusefactory import *
from SPARQLWrapper import SPARQLWrapper, JSON, RDFXML

base_fzwc_fz_uri = "http://data.fzwc.online/resource/fz/"
base_ecnu_fz_uri = "http://fangzhi.ecnu.edu.cn/entity/work/"

base_ecnu_instance_uri = "http://fangzhi.ecnu.edu.cn/entity/instance/"
base_ecnu_item_uri = "http://fangzhi.ecnu.edu.cn/entity/item/"

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

    def __query_ecnu_fz_data_from_uri(self, uri, deprecated_props = None):
        def get_rid_of_deprecated_props(dict_data, keys):
            if keys is None:
                return dict_data
            else:
                for k in keys:
                    if k in dict_data:
                        del dict_data[k]
                return dict_data

        json_data = self.__query_ecnu_for_property_and_value(uri)
        updated_data_value = get_rid_of_deprecated_props(list(json_data.values())[0], deprecated_props)
        json_data = {uri: updated_data_value}
        bnodes = FuseJson.get_blank_nodes(updated_data_value)
        self.__fuse_append(json_data, bnodes)
        return json_data

    def query_ecnu_fz_data(self, id):
        ecnu_fz_uri = Chronicle.ecnu_fz_uri(id)
        if len(ecnu_fz_uri) > 0:
            return self.__query_ecnu_fz_data_from_uri(ecnu_fz_uri)
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
        """ During fuse fz work in ecnu and fz in fzwc,
            first get rid of 3 properties including their sub properties in ecnu fz work
        """
        deprecated_prop = {
            f"{bf}title",
            f"{bf}contribution",
            f"{bf}geographicCoverage"
        }
        try:
            # 1. Get all nodes
            fz_data_from_fzwc = self.__query_fzwc_for_property_and_value(fzwc_fz_uri)

            if ecnu_fz_uri:
                fz_data_from_ecnu = self.__query_ecnu_fz_data_from_uri(ecnu_fz_uri, deprecated_prop)
                if len(fz_data_from_ecnu) > 0:
                    # 2. Fuse ecnu data into fzwc data
                    # because we have already get rid of duplicated properties in ecnu,
                    # so we just update fzwc fz data into ecnu fz date, bnodes are at the same level with the fused fz data
                    # (btw, ecnu and fzwc use different system, so their keys will not same)
                    fused_fz_data = list(fz_data_from_fzwc.values())[0]
                    for k, v in fz_data_from_ecnu.items():
                        if k == ecnu_fz_uri:
                            fused_fz_data.update(v)
                            fused_fz_data = {fzwc_fz_uri: fused_fz_data}
                        else:
                            # append bnodes
                            fused_fz_data.update({k: v})

                    return fused_fz_data
            else:
                # 2. not data from ecnu, just return fzwc data
                return fz_data_from_fzwc

        except RuntimeError as e:
            return {"error" : str(e)}
        except Exception as e:
            return {"error" : f"wrong fz data received. detail msg: {str(e)}"}

    def __qurey_inverse_relation_uris(self, property, which_uuid):
        clause = f"""
            select ?uri
            WHERE {{
                ?uri {property} <{base_ecnu_fz_uri}{which_uuid}> .
            }}
        """

        self.ecnu_sparql_server.setQuery(clause)
        self.ecnu_sparql_server.setReturnFormat(JSON)
        results = self.ecnu_sparql_server.query().convert()

        uris = []
        for data in results["results"]["bindings"]:
            uris.append(data["uri"]["value"])
        return uris

    def query_itemOf_uris_of_fz_work(self, which_uuid):
        return [uri.rsplit("/", 1)[-1] for uri in self.__qurey_inverse_relation_uris("bf:itemOf", which_uuid)]

    def query_instanceOf_uris_of_fz_work(self, which_uuid):
        return [uri.rsplit("/", 1)[-1] for uri in self.__qurey_inverse_relation_uris("bf:instanceOf", which_uuid)]

    def query_ecnu_for_instance_data_of_work(self, instance_uuid):
        instance_uri = f"{base_ecnu_instance_uri}{instance_uuid}"
        return self.__query_ecnu_fz_data_from_uri(instance_uri)

    def query_ecnu_for_item_data_of_work(self, item_uuid):
        item_uri = f"{base_ecnu_item_uri}{item_uuid}"
        return self.__query_ecnu_fz_data_from_uri(item_uri)


if __name__ == "__main__":
    load_sparql_internal_data()

    fz = Chronicle(JSON)
    #Printjson(fz.query_fz_data_from_id(17))
    #Printjson(fz.query_instanceOf_uris_of_fz_work("5f5e8d47f16a407281fdd544093f35e2"))
    #Printjson(fz.query_ecnu_for_inverse_relation_data_of_work("http://fangzhi.ecnu.edu.cn/entity/instance/be2c5342aa3742ec99703fdb8972abc4"))
    #Printjson(fz.query_ecnu_for_inverse_relation_data_of_work(fz.query_instanceOf_uris_of_fz_work("5f5e8d47f16a407281fdd544093f35e2")[0]))
    Printjson(fz.query_ecnu_for_instance_data_of_work("7bc468bda6a94729953394213c370507"))


"""
add to product_detail_data/nowiki
prefix fzwc: <http://www.fzwc.online/ontology/>
select ?s
where {
    ?s fzwc:record <http://data.fzwc.online/entity/produce/y4TB3g50o79n4x61> .
}

prefix fzwc: <http://www.fzwc.online/ontology/>
select ?p
where {
    <http://data.fzwc.online/entity/produce/y4TB3g50o79n4x61> fzwc:concept ?p .
}
"""