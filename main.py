import xml.etree.ElementTree as ET
import sqlite3

# Crear una conexión a la base de datos SQLite3
conn = sqlite3.connect('fondos.db')
c = conn.cursor()

# Crear una tabla para almacenar los datos del fondo
c.execute('''
    CREATE TABLE IF NOT EXISTS fondos (
        registro TEXT PRIMARY KEY,
        nombre TEXT
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS cartera (
        descripcion TEXT,
        inversionPorcActual TEXT,
        inversionPorcAnterior TEXT,
        importeValorAct TEXT,
        importeValorAnt TEXT
    )
''')

# Lista con los nombres de los archivos XML
xml_files = ['semestre2_2020.XML']

# Define un espacio de nombres para los elementos XBRL
ns = {'xbrl': 'http://www.xbrl.org/2003/instance'}

# Iteramos sobre la lista de archivos y los cargamos con ElementTree
for xml_file in xml_files:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    elemento = root.find('.//xbrl:identifier', ns)
    valor = elemento.text

    

    # Define un espacio de nombres para los elementos XBRL
    ns1 = {'iic-com': 'http://www.cnmv.es/iic/com/1-2009/2009-03-31'}

    # Busca el primer elemento con la etiqueta "iic-com:RegistroCNMV" y extrae su valor
    registro = root.find('.//iic-com:RegistroCNMV', ns1)
    valorRegistro= registro.text
    c.execute('INSERT INTO fondos VALUES (?,?)', (valorRegistro,valor,))


#Sacar cartera inversion
ns = {'iic-com': 'http://www.cnmv.es/iic/com/1-2009/2009-03-31'}
for xml_file in xml_files:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    elementos = root.findall('.//iic-com:InversionesFinancierasRVCotizada', ns)
    for elemento in elementos:
        nombreFondo = elemento.find('.//iic-com:InversionesFinancierasDescripcion', ns)
        valor = nombreFondo.text
        c.execute(f"INSERT INTO cartera (descripcion) VALUES ('{valor}')")
        print(" ")
        elementosImporte = elemento.findall('.//iic-com:InversionesFinancierasImporte', ns)
        for elementoImporte in elementosImporte:
            
            actualOAnt =elementoImporte.attrib.get('contextRef')
            for e in elementoImporte:
                decimals = e.attrib.get('decimals')
                actualOAnt =e.attrib.get('contextRef')

                if decimals == "0": 
                    if actualOAnt == "FIM_S22020_II0004840_ia":
                        #valorActual
                        c.execute(f"UPDATE cartera SET importeValorAct ='{e.text}' WHERE descripcion = '{valor}'")
                    else:
                        #valorAnterior
                        c.execute(f"UPDATE cartera SET importeValorAnt ='{e.text}' WHERE descripcion = '{valor}'")
                else:
                    if actualOAnt == "FIM_S22020_II0004840_ia":
                        #porcentajeActual
                        c.execute(f"UPDATE cartera SET inversionPorcActual ='{e.text}' WHERE descripcion = '{valor}'")
                    else:
                        #porcentajeAnterior
                        c.execute(f"UPDATE cartera SET inversionPorcAnterior ='{e.text}' WHERE descripcion = '{valor}'")

print("holaaaaaaa")
conn.commit()
conn.close()