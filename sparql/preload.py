from enum import Enum, unique

wc_cache = dict()
fz_cache = dict()

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
    data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")

    def load_wc():
        wc_uuid = os.path.join(data_dir, "wc_uuid.txt")
        with open(wc_uuid, "r", encoding = "utf8") as wc:
            for line in wc.readlines():
                uuid, id, _ = line.split(":", 2)
                wc_cache[int(id)] = uuid

    def load_fz():
        fz_uuid = os.path.join(data_dir, "fz_uuid.txt")
        with open(fz_uuid, "r", encoding = "utf8") as fz:
            for line in fz.readlines():
                id, _, _, _, internal_uuid, external_uuid = line.split(";", 5)
                fz_cache[int(id)] = [internal_uuid, external_uuid]

    load_wc()
    load_fz()

if __name__ == "__main__":
    pass