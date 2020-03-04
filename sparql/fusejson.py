class FuseJson:
    @staticmethod
    def fuse(to_data, from_data):
        """ deprecated
        """
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

        return {list(to_data.keys())[0] : fuesd_props}, FuseJson.get_blank_nodes(list(from_data.values())[0])

    @staticmethod
    def fuse_append(acc, data):
        acc.update(data)
        return acc

    @staticmethod
    def get_blank_nodes(blank_nodes_data):
        blank_nodes = []
        for k, v in blank_nodes_data.items():
            for k in v:
                if k['type'].lower() == 'bnode':
                    blank_nodes.append(k['value'])

        return blank_nodes