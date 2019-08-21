from SPARQLWrapper import JSON, XML

class Printjson:
    #__debug_flag = "debug"
    def __init__(self, msg, auto_json_format = True):
        import json
        #if os.getenv(self.__debug_flag):
        if auto_json_format and isinstance(msg, dict):
            print("Debug output:" + "\n" + json.dumps(msg, indent = 2) + "\n")
        else:
            print("Debug output:" + "\n" + str(msg) + "\n")

def query_sparql(sparql, clause, output_type):
    sparql.setQuery(clause)
    sparql.setReturnFormat(output_type)
    results = sparql.query().convert()

    return normalize_format(results, output_type)

def normalize_format(raw_data, output_type):
    # dispatchers
    def json_it():
        import os
        property_dict = dict()
        for data in raw_data["results"]["bindings"]:
            key = data["property"]["value"]
            value = {"type" : data["value"]["type"], "value" : data["value"]["value"]}
            print(value)
            os.system("pause")
            if key in property_dict:
                property_dict[key].append(value)
            else:
                property_dict[key] = [value]

        return property_dict

    def xml_it():
        return raw_data

    if output_type == JSON:
        return json_it()
    elif output_type == XML:
        return xml_it()
    else:
        return raw_data