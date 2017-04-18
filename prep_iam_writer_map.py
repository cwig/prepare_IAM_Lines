import sys



import xml.etree.ElementTree
from os import listdir
from os.path import isfile, join
import re
import json
import numpy as np

def get_mapping(xml_folder):
    onlyfiles = [join(xml_folder, f) for f in listdir(xml_folder) if isfile(join(xml_folder, f))]

    all_line_gts = {}
    mapping = {}
    for f in onlyfiles:
        form_id, writer_id, avg_line, avg_full, line_gts = get_key_value(f)
        mapping[form_id] = writer_id, avg_line, avg_full
        all_line_gts.update(line_gts)

    return mapping, all_line_gts

def get_namespace(element):
    m = re.match('\{.*\}', element.tag)
    return m.group(0) if m else ''

def get_key_value(xml_file):
    root = xml.etree.ElementTree.parse(xml_file).getroot()
    namespace = get_namespace(root)

    handwritten_part = root.find('handwritten-part')
    lbys = []
    dys = []
    line_gts = {}
    for lines in handwritten_part:
        lby = float(lines.attrib['lby'])
        uby = float(lines.attrib['uby'])

        asy = float(lines.attrib['asy'])
        dsy = float(lines.attrib['dsy'])

        dys.append(dsy - asy)
        lbys.append(lby - uby)

        line_gts[lines.attrib['id']] = lines.attrib['text']

    return root.attrib['id'], root.attrib['writer-id'], np.median(lbys), np.median(dys), line_gts


if __name__ == "__main__":
    xml_folder = sys.argv[1]
    output_file = sys.argv[2]

    mapping = get_mapping(xml_folder)

    with open(output_file, "w") as f:
        json.dump(mapping, f)