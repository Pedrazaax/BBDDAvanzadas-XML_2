import xml.etree.ElementTree as ET

# Lista con los nombres de los archivos XML
xml_files = ['fondo1.xml', 'fondo2.xml', 'fondo3.xml', 'fondo4.xml', 'fondo5.xml', 'fondo6.xml', 'fondo7.xml', 'fondo8.xml']

# Define un espacio de nombres para los elementos XBRL
ns = {'xbrl': 'http://www.xbrl.org/2003/instance'}

# Iteramos sobre la lista de archivos y los cargamos con ElementTree
for xml_file in xml_files:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Busca todos los elementos con la etiqueta "xbrl:elemento" y extrae su valor
    for elemento in root.findall('.//xbrl:elemento', ns):
        valor = elemento.text
        print(valor)