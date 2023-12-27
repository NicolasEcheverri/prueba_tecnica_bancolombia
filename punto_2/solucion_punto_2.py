


#Archivo Python para extraer del archivo json creado por AWS Textract la información
#del número de matrícula, fecha, departamento, municipio,veredad

#recibe la ruta del archivo analizado
#devuelve un diccionario con la información previamente descrita

#para ejecutarlo: python solucion_punto_2.py --path arhivo.json
#e.g python solucion_punto_2.py --path files/040-464031-220204640254303951_pag1.json
#respuesta: {'numero_matricula': '040-464031', 'fecha': '2022-02-04', 'departamento': 'ATLANTICO', 'municipio': 'BARRANQUILLA', 'vereda': 'BARRANQUILLA'}

#fecha último cambio 23/12/23


import json
import re
import argparse

def convert_date_to_format(fecha):
    '''
    Función para convertir fecha en formato día de mes de año
    a formato YYYY-MM-DD
    '''
    match = re.search(r"(\d+) de ([\w]+) de (\d+)", fecha)
    if match:
        day, month_name, year = match.groups()
        
        #Añadiendo 0 si al inicio si la fecha es de un solo dígito
        if len(day)==1:
            day = '0'+day
        # Convirtiendo meses a números
        months = {
            "Enero": '01',
            "Febrero": '02',
            "Marzo": '03',
            "Abril": '04',
            "Mayo": '05',
            "Junio": '06',
            "Julio": '07',
            "Agosto": '08',
            "Septiembre": '09',
            "Octubre": '10',
            "Noviembre": '11',
            "Diciembre": '12',
        }
        month = months[month_name.title()]  # Handle potential capitalization inconsistencies
        return f'{year}-{month}-{day}'
    else:
        return 'match failed'


def extraccion_informacion_documento(path_archivo):
    '''
    Función para extraer del json creada por AWS Textract la información
    del número de matrícula, fecha, departamento, municipio,veredad

    recibe la ruta del archivo analizado
    devuelve un diccionario con la información previamente descrita
    '''

    #cargando el archivo
    f    = open(path_archivo)
    data = json.load(f)   

    #posición de la lista que contiene la ubicacion de la matricula
    ubicacion_matricula = data['Blocks'][11]['Text']
    #el numero se encuentra en la tercera posición de este string
    nro_matricula = ubicacion_matricula.split(" ")[2]

    #posición de la lista que contiene la ubicacion de la fecha
    ubicacion_fecha = data['Blocks'][13]['Text']
    #extrayendo la fecha mediante regex
    fecha           = convert_date_to_format(ubicacion_fecha)

    #posición de la lista que contiene la ubicacion física
    lista_ubicacion_fisica = data['Blocks'][17]['Text'].split(" ")
    departamento           = lista_ubicacion_fisica[lista_ubicacion_fisica.index('DEPTO:')+1]
    municipio              = lista_ubicacion_fisica[lista_ubicacion_fisica.index('MUNICIPIO:')+1]
    vereda                 =  lista_ubicacion_fisica[lista_ubicacion_fisica.index('VEREDA:')+1]

    diccionario_datos = {'numero_matricula':nro_matricula,
                         'fecha':fecha,
                         'departamento':departamento,
                         'municipio':municipio,
                         'vereda':vereda}
    return diccionario_datos



###################################
###################################
###################################


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", required=True)
    args = parser.parse_args()
    path_archivo = args.path 

    diccionario_datos = extraccion_informacion_documento(path_archivo)
    print(diccionario_datos)
