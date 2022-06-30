# -*- #################
# ---------------------------------------------------------------------------
# COMANDOS.py
# Authors: Franz Cortez, Julio Cerna
# Description: Automatizacion del analisis de imágenes satelitales del desierto de Atacama
# Version: 1.0.0
# ---------------------------------------------------------------------------

# Import arcpy module
from re import X
import arcpy
from arcpy.sa import *
import pandas as pd
import os
import sys
from os import remove
from shutil import rmtree
from collections import OrderedDict

def removeTemporal():
    rmtree(rutaDefecto + '\\Temporal\\')

def current_date_format(day, month,year):
    months = ("ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC")
    month = months[month - 1]
    messsage = "{}{}{}_".format(day,month,year)

    return messsage

def carpeta_format(month, year):
    months = ("ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC")
    month = months[month - 1]
    messsage = "{}_{}".format(month, year)

    return messsage

def creacion_carpetas(rutaDefecto, month, year):
    try:
        os.makedirs(rutaDefecto + '\\Shapefile')
    except:
        pass

    try:
        os.makedirs(rutaDefecto + '\\Temporal')
    except:
        pass

    try:
        os.makedirs(rutaDefecto + '\\Data\\')
    except:
        pass

    try:
        os.makedirs(rutaDefecto + '\\Imagenes\\' + carpeta_format(month,year))
    except:
        pass

def crear(rutaDefecto, month, year):
    creacion_carpetas(str(rutaDefecto), month, year)

def rectificarCoordenadas(raster_entrada, ruta_temporal, coordenadas):
    arcpy.ProjectRaster_management(raster_entrada , ruta_temporal, coordenadas, resampling_type="NEAREST", cell_size="30 30", geographic_transform="", Registration_Point="", in_coor_system="", vertical="NO_VERTICAL")

def primer_recorte(raster_entrada, nombre_recorte, shapefile):

    desc = arcpy.Describe(shapefile)

    xMin = desc.extent.XMin
    xMax = desc.extent.XMax
    yMin = desc.extent.YMin
    yMax = desc.extent.YMax

    pos = str(xMin) + " " + str(yMin) + " " + str(xMax) + " " + str(yMax)

    arcpy.Clip_management(raster_entrada, pos, nombre_recorte, shapefile, "-99999999", "ClippingGeometry", "NO_MAINTAIN_EXTENT")

def calculo(formula, ruta_salida):
    arcpy.gp.RasterCalculator_sa(formula, ruta_salida)
    
def retornar_fecha(day, month, year):
    months = ("ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC")
    month = months[month - 1]
    return "{}_{}_{}".format(day, month, year)


# Script arguments
arcpy.AddMessage("*************INICIO**************")
rutaDefecto = arcpy.GetParameterAsText(0)
nombre = arcpy.GetParameterAsText(1).upper()
Raster_de_entrada = arcpy.GetParameterAsText(2)
nombre2 = arcpy.GetParameterAsText(3).upper()
Raster_de_entrada2 = arcpy.GetParameterAsText(4)
coordenada = arcpy.GetParameterAsText(5)
shapefile = arcpy.GetParameterAsText(6)
L =  arcpy.GetParameterAsText(7)
limite_exclusion = arcpy.GetParameterAsText(8)
mostrar_dataset = str(arcpy.GetParameterAsText(9))
opcion = arcpy.GetParameterAsText(10)
nombreOtro = arcpy.GetParameterAsText(11)
fecha = arcpy.GetParameterAsText(12)

#restructura

try:   
    prueba = float(L)
except ValueError:
    arcpy.AddMessage("Error: L deberia ser un NUMERO")
    exit()

try:
    prueba = float(limite_exclusion)
except ValueError:
    arcpy.AddMessage("Error: El LIMITE DE EXCLUSION deberia ser un NUMERO")
    exit()


day = ""
month = ""
year = ""

infoSatelite = ''

if(opcion == 'LANDSAT'):
    

    firstSplit = Raster_de_entrada.split("\\")
    info = firstSplit[len(firstSplit)-1].split("_")

    day = int(info[3][6:8])
    month = int(info[3][4:6])
    year = int(info[3][0:4])

    infoSatelite = info[0] + "_" + info[1] + "_" + info[5] + "_" + info[6]

elif(opcion == 'SENTINEL'):

    firstSplit = Raster_de_entrada.split("\\")
    info = firstSplit[len(firstSplit)-1].split("_")

    day = int(info[3][6:8])
    month = int(info[3][4:6])
    year = int(info[3][0:4])

    infoSatelite = "SENTINEL"

else:
    fechaSinHora = fecha.split(" ")
    info = fechaSinHora[0].split("-")


    if(len(info[0]) == 4):
        year = int(info[0])
        month = int(info[1])
        day = int(info[2])
    else:
        day = int(info[0])
        month = int(info[1])
        year = int(info[2])

    infoSatelite = nombreOtro


crear(rutaDefecto, month, year)

if( coordenada == '' ):
    coordenada = "PROJCS['WGS_1984_UTM_Zone_19S',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',10000000.0],PARAMETER['Central_Meridian',-69.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"

if(L == ""):
    L = '0'

nombreFinal = current_date_format(day, month, year) + nombre
nombreFinal2 = current_date_format(day, month, year) + nombre2
fechaNombre = current_date_format(day, month, year)

rutaTemporal = rutaDefecto + '\\Temporal\\' + nombreFinal + ".tif"
rutaTemporal2 = rutaDefecto + '\\Temporal\\' + nombreFinal2 + ".tif"

############################## CICLO 1 ##############################

arcpy.AddMessage("************* INICIO CICLO 1 *************")

# Process: Proyectar ráster

try:
    rectificarCoordenadas(Raster_de_entrada, rutaTemporal, coordenada)
    rectificarCoordenadas(Raster_de_entrada2, rutaTemporal2, coordenada)
except :
    e = sys.exc_info()[1]
    arcpy.AddMessage(e.args[0])
    removeTemporal()
    exit()

arcpy.AddMessage("************* FIN CICLO 1 *************")

############################## CICLO 2 ##############################

arcpy.AddMessage("************* INICIANDO CICLO 2 *************")

# Local variables:
ruta_temporal_re_1 = rutaDefecto + '\\Temporal\\' + nombreFinal + "_re.tif"
ruta_temporal_re_2 = rutaDefecto + '\\Temporal\\' + nombreFinal2 + "_re.tif"

# Process: Recortar
try:
    primer_recorte(rutaTemporal, ruta_temporal_re_1, shapefile)
    primer_recorte(rutaTemporal2, ruta_temporal_re_2, shapefile)
except :
    e = sys.exc_info()[1]
    arcpy.AddMessage(e.args[0])
    removeTemporal()
    exit()


# Local variables:
x = ruta_temporal_re_1
y = ruta_temporal_re_2

formula = '( ( (Float("' + x + '")) - (Float("' + y + '")) ) / ( (Float("' + x + '")) + (Float("' + y + '")) + ' + L + ' ) ) * ( 1 + ' + L + ' )'

ruta_salida = rutaDefecto + '\\Temporal\\' + nombreFinal + nombre2 + "_cal.tif"

# Process: Calculadora ráster
try:
    calculo(formula, ruta_salida)
except :
    e = sys.exc_info()[1]
    arcpy.AddMessage(e.args[0])
    removeTemporal()
    exit()


arcpy.AddMessage("************* FIN CICLO 2 *************")

arcpy.AddMessage("************* INICIANDO CICLO 3 ************")
################################### CICLO 3 #########################################

# # Get Raster Properties
maxvalue = arcpy.GetRasterProperties_management(ruta_salida, "MAXIMUM")

shapefile = shapefile.replace(" ", "_")
ruta_final = rutaDefecto + '\\Imagenes\\' + carpeta_format(month, year) + '\\' + nombre + nombre2 + "_" + fechaNombre + "[" + limite_exclusion + "]_" + shapefile + ".tif"

#Reclass
try:
    myRemapRange = RemapRange([[limite_exclusion, maxvalue, 1]])
    outReclass = Reclassify(ruta_salida, "Value", myRemapRange)
    outReclass.save(ruta_final)
except :
    e = sys.exc_info()[1]
    arcpy.AddMessage(e.args[0])
    removeTemporal()
    exit()


arcpy.AddMessage("************* FIN CICLO 3 *************")

arcpy.AddMessage("************* INICIANDO CICLO 4 ************")

#Crea tabla
ruta_data = rutaDefecto + '\\Temporal\\' + nombre + nombre2 + "_" + fechaNombre + "Tabla"

try:
    arcpy.gp.ZonalStatisticsAsTable_sa(ruta_final, "VALUE", ruta_final, ruta_data, "DATA", "ALL")
except :
    e = sys.exc_info()[1]
    arcpy.AddMessage(e.args[0])
    removeTemporal()
    exit()

# crea archivo excel XLS
ruta_excel = rutaDefecto + '\\Data\\' + shapefile + '_' + nombre + nombre2 + '.xls'
archivo_existe = os.path.isfile(ruta_excel)
# datos para el excel
fecha = retornar_fecha(day, month, year)
columnas = ["ID", "FECHA", "CLASE 0 AREA (m^2)", "CLASE 1 AREA (m^2)", "SENSOR"]
exclusion = "EXCLUSION (-1," + limite_exclusion + ")"

if month < 10:
    month = '0' + str(month)
if day < 10:
    day = '0' + str(day)

id = int(str(year)+str(month)+str(day))

month = int(month)


if archivo_existe:
    arcpy.AddMessage("************* EXCEL EXISTENTE, MODIFICANDO... ************")
    # excel auxiliar para los nuevos datos
    ruta_excel_nuevo = rutaDefecto + '\\Temporal\\' + shapefile + '_' + nombre + nombre2 +'.xls'
    arcpy.TableToExcel_conversion(ruta_data, ruta_excel_nuevo, Use_field_alias_as_column_header="ALIAS", Use_domain_and_subtype_description="CODE")
    ############################################################################
    existente = pd.read_excel(ruta_excel, sheet_name=None)
    
    lista_keys = []
    lista_datas = []

    for key, hoja in existente.items():
        lista_keys.append(key)
        lista_datas.append(pd.DataFrame(hoja))
        
    df2 = pd.read_excel(ruta_excel_nuevo)['AREA']
    df_n = pd.DataFrame([[id, fecha, df2[0], df2[1], infoSatelite]], columns=columnas)
    
    # se eliminan los excel
    remove(ruta_excel_nuevo)
    remove(ruta_excel)

    writer = pd.ExcelWriter(ruta_excel)

    if exclusion in lista_keys:
        arcpy.AddMessage("************* LA EXCLUSION ESTA ************")
        existente[exclusion] = pd.concat([existente[exclusion],df_n], sort=False)
        existente[exclusion] = existente[exclusion].sort_values(by=["ID"])
        
    for key, hoja in existente.items():
        hoja.to_excel(writer, index=False, sheet_name=key)

    if exclusion not in lista_keys:
        arcpy.AddMessage("************* NO HAY EXCLUSION, CREANDO UNA HOJA NUEVA ************")       
        df_n.to_excel(writer, index=False, sheet_name=exclusion)

    writer.save()
    writer.close()

    writer = pd.ExcelWriter(ruta_excel)
    #ordenamiento por nombre de las hojas
    existente = OrderedDict(sorted(pd.read_excel(ruta_excel, sheet_name=None).items()))
        
    for key, hoja in existente.items():
        hoja.to_excel(writer, index=False, sheet_name=key)
        
    writer.save()
    writer.close()
    
    arcpy.AddMessage("************* MODIFICADO ************")
    ############################################################################

else:    
    # nuevo excel
    arcpy.AddMessage("************* CREANDO NUEVO EXCEL ************")
    arcpy.TableToExcel_conversion(ruta_data, ruta_excel, Use_field_alias_as_column_header="ALIAS", Use_domain_and_subtype_description="CODE")
    arcpy.AddMessage("************* CREANDO NUEVO FORMATO ************")
    df = pd.read_excel(ruta_excel)['AREA']
    nuevo_df = pd.DataFrame([[id, fecha, df[0], df[1], infoSatelite]], columns=columnas)
    arcpy.AddMessage("************* FORMATO CREADO ************")
    nuevo_df = nuevo_df.sort_values(by=["ID"])
    nuevo_df.to_excel(ruta_excel, index=False, sheet_name=exclusion)
    arcpy.AddMessage("************* EXCEL ACTUALIZADO ************")

arcpy.AddMessage("************* FIN CICLO 4 *************")

# ESTA AL FINAL PORQUE AL CREAR EL EXCEL SE "REINICIA" LOS ARCHIVOS Y SE QUITA
if mostrar_dataset == "true":
    md = arcpy.mapping.MapDocument('CURRENT')
    df = arcpy.mapping.ListDataFrames(md)[0]
    final = rutaDefecto + '\\Imagenes\\' + carpeta_format(month, year) + '\\' + nombreFinal + nombre2 + "_Layer"
    result = arcpy.MakeRasterLayer_management(ruta_final, final)
    layer = result.getOutput(0)
    pt = arcpy.mapping.AddLayer(df, layer, 'AUTO_ARRANGE')

removeTemporal()