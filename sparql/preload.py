from enum import Enum, unique

wc_cache = dict()

@unique
class LoadType(Enum):
    txt = "txt"

def load_sparql_internal_data(type = LoadType.txt):
    if type == LoadType.txt:
        return load_from_txt()
    else:
        raise Exception(r"Unknown data type during preload")


def load_from_txt():
    import os.path
    current_dir = os.path.abspath(os.path.dirname(__file__))
    # txt data lists
    wc_uuid = os.path.join(current_dir, "wc_uuid.txt")
    # data lists end

    with open(wc_uuid, "r", encoding = "utf8") as wc:
        for line in wc.readlines():
            uuid, key, _ = line.split(":", 2)
            wc_cache[int(key)] = uuid

if __name__ == "__main__":
    pass