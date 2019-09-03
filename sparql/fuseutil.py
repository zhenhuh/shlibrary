from SPARQLWrapper import JSON, XML, RDFXML

class FuseUtil:
    def __init__(self, fuse_type = JSON):
        self.fuse_type = fuse_type

    def fuse(self, to_data, from_data):
        if self.fuse_type == JSON:
            return FuseUtil.__fuse_json(to_data, from_data)
        else:
            raise RuntimeError("Fuse type not support")

    def fuse_append(self, acc, data):
        if self.fuse_type == JSON:
            return FuseUtil.__fuse_append_json(acc, data)
        else:
            raise RuntimeError("Fuse type not support")

    def get_blank_nodes(self, blank_nodes_data):
        if self.fuse_type == JSON:
            return FuseUtil.__get_blank_nodes(blank_nodes_data)
        else:
            raise RuntimeError("Fuse type not support")

    @staticmethod
    def __fuse_json(to_data, from_data):
        to_props_set = set(list(to_data.values())[0].keys())
        from_props_set = set(list(from_data.values())[0].keys())
        intersection_props = to_props_set.intersection(from_props_set)

        def dropprops(d):
            for prop in intersection_props:
                d.pop(prop)
            return d

        from_data.update({list(from_data.keys())[0] : dropprops(list(from_data.values())[0])})

        fuesd_props = list(to_data.values())[0]
        fuesd_props.update(list(from_data.values())[0])

        return {list(to_data.keys())[0] : fuesd_props}, FuseUtil.__get_blank_nodes(list(from_data.values())[0])

    @staticmethod
    def __fuse_append_json(acc, data):
        acc.update(data)
        return acc

    @staticmethod
    def __get_blank_nodes(blank_nodes_data):
        blank_nodes = []
        for k, v in blank_nodes_data.items():
            for k in v:
                if k['type'].lower() == 'bnode':
                    blank_nodes.append(k['value'])

        return blank_nodes