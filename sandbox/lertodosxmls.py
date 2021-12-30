import xml.etree.ElementTree as ET
import os

path = r'C:\Users\felipe.rosa\Desktop\xmls_fit'
for filename in os.listdir(path):
    if not filename.endswith('.xml'): continue
    fullname = os.path.join(path, filename)
    tree = ET.parse(fullname)
    print(tree.text())
