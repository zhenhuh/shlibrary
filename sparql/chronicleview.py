from sparql.chronicle import *
from sparql.prefix import *

class ChronicleView:
    def __init__(self):
        self.fz = Chronicle(JSON)

    def __find_not_bnode_data(self, json_data):
        for k, v in json_data.items():
            if not str(k).startswith("nodeID"):
                return v.copy()
        return {}

    def __translate_to_view(self, data, view_items, bnode_mappings):
        fz_data = self.__find_not_bnode_data(data)

        work_data = {}
        for k, v in view_items.items():
            curr_data_in_all = []
            curr_data_block = fz_data.get(k, [{"type": "nokey", "value": ""}])
            if isinstance(curr_data_block, list):
                for curr_data in curr_data_block:
                    if curr_data.get("type", "") == "bnode":
                        nodeID = curr_data.get("value", "")
                        node_value = data.get(nodeID, {})
                        # assume only one data in bnode list
                        curr_data = node_value.get(bnode_mappings.get(k, ""), [""])[0]
                    curr_data_in_all.append(curr_data.get("value", ""))

            if isinstance(curr_data_block, dict):
                # get value of the one whose type is literal, now is prepared for uri
                pass
            work_data.update({v: curr_data_in_all})

        return work_data

    def work(self, id):
        fzwc_suffix = "（FZWC）"
        ecnu_suffix = "（ECNU）"
        view_items = {
            f"{dc}abstract": f"摘要{fzwc_suffix}",
            f"{dc}title": f"志书题名{fzwc_suffix}",
            f"{fzwc}catalogOf": f"藏录信息{fzwc_suffix}",
            f"{fzwc}classification": f"分类号{fzwc_suffix}",
            f"{fzwc}dataBase": f"收录库{fzwc_suffix}",
            f"{fzwc}electronicLocator": f"电子书{fzwc_suffix}",
            f"{fzwc}hasCreator": f"责任者{fzwc_suffix}",
            f"{fzwc}modifyDate": f"重印、增补日期{fzwc_suffix}",
            f"{fzwc}stereotypeDate": f"刻板日期{fzwc_suffix}",
            f"{fzwc}typeOfFz": f"方志类型{fzwc_suffix}",
            f"{fzwc}volumeOfFz": f"卷次{fzwc_suffix}",
            f"{fzwc}writeDate": f"纂修日期{fzwc_suffix}",
            f"{shl}place": f"地区{fzwc_suffix}",
            f"{rdfs}label": f"名称{ecnu_suffix}",
            f"{bf}subject": f"主题词{ecnu_suffix}",
            f"{shl}temporal": f"方志年代{ecnu_suffix}",
        }

        bnode_mappings = {
            f"{bf}subject": f"{rdfs}label",
            f"{shl}temporal": f"{shl}dynasty",
        }

        data = self.fz.query_fz_data_from_id(id)
        return self.__translate_to_view(data, view_items, bnode_mappings)

    def instance(self, uuid):
        view_items = {
            f"{bf}title": "方志名称",
            f"{bf}responsibilityStatement": "责任者",
            f"{bf}provisionActivityStatement": "出版社",
            f"{bf}dimensions": "尺寸",
            f"{bf}identifiedBy": "机构书目号", # bf:Local "机构书目号" bf:Isbn "ISBN"
            f"{bf}provisionActivity": "出版时间",
            f"{bf}genreForm": "文献形态",
            f"{bf}adminMetadata": "元数据来源",
            f"{bf}editionStatement": "版本",
            f"{bf}extent": "页码",
            f"{bf}dataSource": "收录库", # 78c3f92a7d284363b557c37e7637660d
        }

        bnode_mappings = {
            f"{bf}title": f"{bf}mainTitle",
            f"{bf}identifiedBy": f"{rdf}value",
            f"{bf}provisionActivity": f"{bf}date",
            f"{bf}dataSource": f"{rdf}value",
            f"{bf}genreForm": f"{rdf}value",
            f"{bf}extent": f"{rdfs}label",
            f"{bf}adminMetadata": f"{bf}source",
        }

        bnode_mappings2 = {
            "元数据来源": f"{bf}code",
        }

        data = self.fz.query_ecnu_for_instance_data_of_work(uuid)
        result = self.__translate_to_view(data, view_items, bnode_mappings)
        for k, v in bnode_mappings2.items():
            curr_data_in_all = []
            for nodeID in result.get(k, []):
                node_value = data.get(nodeID, {})
                curr_data = node_value.get(bnode_mappings2[k], [""])[0]
                curr_data_in_all.append(curr_data.get("value", ""))
            del result[k]
            result[k] = curr_data_in_all

        return result

    def item(self, uuid):
        view_items = {
            f"{bf}electronicLocator": "馆藏目录（电子资源）",
            f"{bf}heldBy": "馆藏地",
            f"{bf}shelfMark": "索书号",
            f"{bf}source": "馆藏目录（OPAC）", # multi - 3c5f0315225146eb81e2ca66b443e5a1
        }

        bnode_mappings = {
            f"{bf}heldBy": f"{rdfs}label",
            f"{bf}shelfMark": f"{rdfs}label",
            f"{bf}source": f"{rdf}value", # multi
        }
        # electronicLocator: http://fangzhi.ecnu.edu.cn/entity/item/338ed4af27054ae4bf7791cb7ac9957d
        # shelfMark: http://fangzhi.ecnu.edu.cn/entity/item/3c5f0315225146eb81e2ca66b443e5a1

        data = self.fz.query_ecnu_for_item_data_of_work(uuid)
        return self.__translate_to_view(data, view_items, bnode_mappings)

if __name__ == "__main__":
    load_sparql_internal_data()

    fz = ChronicleView()
    #fz.work(17)
    fz.instance("3675db6a296f489896103e2f41ff4ca8") # 7bc468bda6a94729953394213c370507
    #fz.item("3c5f0315225146eb81e2ca66b443e5a1") # 6eb680fd38094549b742d764033db3df