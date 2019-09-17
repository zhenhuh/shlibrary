import xml.etree.ElementTree as ET

class FuseXml:
    @staticmethod
    def fuse(to_data, from_data):
        to_ns = FuseXml.__namespace_of(to_data)
        from_ns = FuseXml.__namespace_of(from_data)

        # fuse 2 namespaces, use ecnu as base namespace, means for same url, use namespace in ecnu data
        fused_ns = FuseXml.__fuse_ns(from_ns, to_ns)

        # use fused common namespace
        for prefix, uri in fused_ns.items():
            ET.register_namespace(prefix, uri)

        tree = ET.fromstring(to_data)
        for child in tree.getchildren():
            print(child.tag)
            print(child.attrib)

        #with open('output.xml', 'w') as xml_file:
        #    xml_file.write(ET.tostring(tree).decode("utf-8"))

        # cannot get info from bnode with bnode format like rdf:nodeID="Nb19feb6e24234b3388cbf202518fc50c"

    @staticmethod
    def fuse_append(acc, data):
        pass

    @staticmethod
    def get_blank_nodes(blank_nodes_data):
        pass

    @staticmethod
    def __fuse_ns(base_ns, other_ns):
        reverse_kv = lambda d : {v: k for (k, v) in d.items()}
        base_ns_reverse = reverse_kv(base_ns)
        other_ns_reverse = reverse_kv(other_ns)

        other_ns_reverse.update(base_ns_reverse)

        return reverse_kv(other_ns_reverse)


    @staticmethod
    def __namespace_of(xml_data):
        from lxml import etree

        utf8_parser = etree.XMLParser(encoding = "utf-8")
        tree = etree.fromstring(xml_data.encode("utf-8"), utf8_parser)

        return tree.nsmap

if __name__ == "__main__":
    xml_data = """<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
   xmlns:bf1="http://id.loc.gov/ontologies/bibframe/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:shl="http://www.library.sh.cn/ontology/"
>
  <rdf:Description rdf:about="http://www.fzwc.online/ontologies/bibframe/Work/pvRQ2u4c8S1rnGsB">
    <bf1:geographicCoverage rdf:resource="http://id.loc.gov/ontologies/bibframe/geographicCoverage/云南"/>
    <bf1:classification rdf:resource="http://id.loc.gov/ontologies/bibframe/classification/府厅州县志"/>
    <shl:temporal rdf:resource="http://data.library.sh.cn/authority/temporal/zf1emm85jbscnyqh"/>
    <bf1:contribution rdf:datatype="http://www.w3.org/2001/XMLSchema#String">(清)李炳臣修;(清)李翰香纂</bf1:contribution>
    <bf1:subject rdf:resource="http://id.loc.gov/ontologies/bibframe/subject/府厅州县志"/>
    <bf1:place rdf:resource="http://id.loc.gov/ontologies/bibframe/place/云南"/>
    <bf1:title rdf:datatype="http://www.w3.org/2001/XMLSchema#String">维西县志</bf1:title>
  </rdf:Description>
</rdf:RDF>
"""
    xml_data2 = """<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
   xmlns:bf="http://id.loc.gov/ontologies/bibframe/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
   xmlns:shl="http://www.library.sh.cn/ontology/"
>
  <rdf:Description rdf:about="http://fangzhi.ecnu.edu.cn/entity/work/8013f297634245409de5dcddb0f01813">
    <bf:partOf rdf:resource="http://fangzhi.ecnu.edu.cn/entity/work/74775bd32b4146eaa2e6e612d33aa7fa"/>
    <bf:geographicCoverage rdf:nodeID="N1b58a993a349435687f78aad33bbaca9"/>
    <rdfs:label>维西县志(云南,民国)</rdfs:label>
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Work"/>
    <bf:title rdf:nodeID="N758395ceff12408593d02bb60eaa2417"/>
    <bf:contribution rdf:nodeID="Na0ecf49af34f4acbaf816af2afc9c7ee"/>
    <bf:contribution rdf:nodeID="N1aa0b6f44e374934b826a306e15ab6d3"/>
    <shl:temporal rdf:nodeID="N79ea8b087f9647c197a2ec7726fb2571"/>
    <bf:subject rdf:nodeID="N7f0837f0c1834fba92527e0bc5218780"/>
  </rdf:Description>
</rdf:RDF>
"""

    FuseXml.fuse(xml_data, xml_data2)

    # http://effbot.org/zone/element-namespaces.htm
    #tree = ET.fromstring(xml_data, parser = None)

    from lxml import etree
    # https://stackoverflow.com/questions/3402520/is-there-a-way-to-force-lxml-to-parse-unicode-strings-that-specify-an-encoding-i
    #utf8_parser = etree.XMLParser(encoding='utf-8')
    #tree = etree.fromstring(xml_data.encode('utf-8'), utf8_parser)
    #print(tree.nsmap)


"""<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
   xmlns:bf="http://id.loc.gov/ontologies/bibframe/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
>
  <rdf:Description rdf:about="http://fangzhi.ecnu.edu.cn/entity/work/bc2ac6c1a9bc4094861811d9c87068c2">
    <rdf:type rdf:resource="http://id.loc.gov/ontologies/bibframe/Work"/>
    <bf:subject rdf:nodeID="N4c4d60aae2054a7f805dc76c1aa87096"/>
    <bf:title rdf:nodeID="N6ff156f087344d03a8344978843cec55"/>
    <bf:classification rdf:nodeID="Nbd9d17dc5e69418082d778a31c6068f8"/>
    <bf:geographicCoverage rdf:nodeID="N8bdf0196bb454d2bb868c209f9356fff"/>
    <bf:contribution rdf:nodeID="Nb19feb6e24234b3388cbf202518fc50c"/>
    <rdfs:label>长安志()</rdfs:label>
  </rdf:Description>
</rdf:RDF>"""