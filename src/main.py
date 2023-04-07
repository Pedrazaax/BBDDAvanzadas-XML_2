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
        importe TEXT,
        inversionPorcActual,
        inversionPorcAnterior,
        importeValorAct,
        importeValorAnt
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
        print("   ")
        nombreFondo = elemento.find('.//iic-com:InversionesFinancierasDescripcion', ns)
        valor = nombreFondo.text
        elementosImporte = elemento.findall('.//iic-com:InversionesFinancierasImporte', ns)
        for elementoImporte in elementosImporte:
            elementoValor = elementoImporte.findall('.//iic-com:InversionesFinancierasValor', ns)
            elementoPorcentaje = elementoImporte.findall('.//iic-com:InversionesFinancierasPorcentaje', ns)
            for importePorcentaje in elementoPorcentaje:
                    #valorFondo = elementoImporte.find('.//iic-com:InversionesFinancierasValor', ns)
                    #valorFondotext= valorFondo.text
                    porcentajeFondo = elementoImporte.find('.//iic-com:InversionesFinancierasPorcentaje', ns)
                    porcentajeFondoText = porcentajeFondo.text
                    print(porcentajeFondoText)
            for importeValor in elementoValor:
                    valorFondo = elementoImporte.find('.//iic-com:InversionesFinancierasValor', ns)
                    valorFondotext= valorFondo.text
                    print(valorFondotext)


                   


conn.commit()
conn.close()