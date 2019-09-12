from SPARQLWrapper import JSON, RDFXML
from sparql.fusejson import *
from sparql.fusexml import *

class FuseFactory:
    def __init__(self, fuse_type = JSON):
        self.fuse_type = fuse_type

    def fuse(self, to_data, from_data):
        if self.fuse_type == JSON:
            return FuseJson.fuse(to_data, from_data)
        elif self.fuse_type == RDFXML:
            return FuseXml.fuse(to_data, from_data)
        else:
            raise RuntimeError("Fuse type not support")

    def fuse_append(self, acc, data):
        if self.fuse_type == JSON:
            return FuseJson.fuse_append(acc, data)
        elif self.fuse_type == RDFXML:
            return FuseXml.fuse_append(acc, data)
        else:
            raise RuntimeError("Fuse type not support")

    def get_blank_nodes(self, blank_nodes_data):
        if self.fuse_type == JSON:
            return FuseJson.get_blank_nodes(list(blank_nodes_data.values())[0])
        elif self.fuse_type == RDFXML:
            return FuseXml.get_blank_nodes(blank_nodes_data)
        else:
            raise RuntimeError("Fuse type not support")