import xml.etree.ElementTree as ET
import sqlite3

# Crear una conexión a la base de datos SQLite3
conn = sqlite3.connect('fondos.db')
c = conn.cursor()

# Crear una tabla para almacenar los datos del fondo
c.execute('''
    CREATE TABLE IF NOT EXISTS fondos (
        registro INTEGER PRIMARY KEY,
        nombre TEXT,
        correo TEXT,
        direccion TEXT
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS cartera (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT,
        inversionPorcActual TEXT,
        inversionPorcAnterior TEXT,
        importeValorAct TEXT,
        importeValorAnt TEXT,
        periodo TEXT,
        registro INTEGER,
        FOREIGN KEY (registro) REFERENCES fondos(registro)
    )
''')

# Lista con los nombres de los archivos XML
xml_files = ['semestre2_2020.XML','semestre1_2020.XML','semestre1_2019.XML','semestre2_2019.XML']

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
    dgi = {'dgi-est-gen': 'http://www.xbrl.org.es/es/2008/dgi/gp/est-gen/2008-01-30'}

    # Busca el primer elemento con la etiqueta "iic-com:RegistroCNMV" y extrae su valor
    registro = root.find('.//iic-com:RegistroCNMV', ns1)
    valorRegistro= int(registro.text)

    # Cogemos el valor de la direccion
    direccion = root.find('.//dgi-est-gen:AddressLine', dgi)
    valorDir= direccion.text

    # Cogemos el valor del correo
    correo = root.find('.//dgi-est-gen:CommunicationValue', dgi)
    valorCorreo= correo.text
    c.execute('INSERT OR IGNORE INTO fondos VALUES (?,?,?,?)', (valorRegistro,valor,valorDir,valorCorreo))

    

#Sacar cartera inversion
ns = {'iic-com': 'http://www.cnmv.es/iic/com/1-2009/2009-03-31'}
for xml_file in xml_files:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    elementos = root.findall('.//iic-com:InversionesFinancierasRVCotizada', ns)
    
    for elemento in elementos:
        nombreFondo = elemento.find('.//iic-com:InversionesFinancierasDescripcion', ns)
        valor = nombreFondo.text
        periodo = xml_file.split(".")[0] +""
        c.execute("INSERT INTO cartera (descripcion, registro, periodo) VALUES (?, ?, ?)", (valor, valorRegistro, periodo))
        idGenerado = c.execute('SELECT last_insert_rowid()').fetchone()[0]  #Coge el id creado en el insert anterior ya que es autoincremental la primary key
        elementosImporte = elemento.findall('.//iic-com:InversionesFinancierasImporte', ns)
        
        for elementoImporte in elementosImporte:
            actualOAnt =elementoImporte.attrib.get('contextRef')
            for e in elementoImporte:
                decimals = e.attrib.get('decimals')
                actualOAnt = e.attrib.get('contextRef').split("_")[3]

                if decimals == "0": 
                    if actualOAnt == "ia":
                        #valorActual
                        c.execute(f"UPDATE cartera SET importeValorAct ='{e.text}' WHERE id = '{idGenerado}'")
                    else:
                        #valorAnterior
                        c.execute(f"UPDATE cartera SET importeValorAnt ='{e.text}' WHERE id = '{idGenerado}'")
                else:
                    if actualOAnt == "ia":
                        #porcentajeActual
                        c.execute(f"UPDATE cartera SET inversionPorcActual ='{e.text}' WHERE id = '{idGenerado}'")
                    else:
                        #porcentajeAnterior
                        c.execute(f"UPDATE cartera SET inversionPorcAnterior ='{e.text}' WHERE id = '{idGenerado}'")

conn.commit()
conn.close()