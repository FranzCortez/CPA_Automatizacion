# -*- #################
# ---------------------------------------------------------------------------
# COMANDOS.py
# Authors: Franz Cortez, Julio Cerna
# Description: Automatizacion del analisis de imagenes satelitales del decierto de Atacama
# Version: 1.0.0
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
from datetime import datetime
import os

def current_date_format(date):
    months = ("ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC")
    day = date.day
    month = months[date.month - 1]
    messsage = "{}{}_".format(month, day)

    return messsage

def carpeta_format(date):
    months = ("ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC")
    month = months[date.month - 1]
    year = date.year
    messsage = "{}_{}".format(month, year)

    return messsage

def creacion_carpetas(rutaDefecto):
    try:
        os.makedirs(rutaDefecto + '\\Shapefile')
    except:
        pass

    try:
        os.makedirs(rutaDefecto + '\\Temporal')
    except:
        pass

    try:
        now = datetime.now()
        os.makedirs(rutaDefecto + '\\Data\\' + carpeta_format(now))
    except:
        pass

    try:
        os.makedirs(rutaDefecto + '\\Imagenes\\' + carpeta_format(now))
    except:
        pass

def crear(rutaDefecto):
    creacion_carpetas(str(rutaDefecto))

def rectificarCoordenadas(raster_entrada, ruta_temporal, coordenadas):
    arcpy.ProjectRaster_management(raster_entrada , ruta_temporal, coordenadas, resampling_type="NEAREST", cell_size="30 30", geographic_transform="", Registration_Point="", in_coor_system="", vertical="NO_VERTICAL")

def primer_recorte(raster_entrada, nombre_recorte, extension_salida):
    arcpy.Clip_management(raster_entrada, "626992.524499999 7422179.91 659638.799700004 7457522.4788", nombre_recorte, extension_salida, "-99999999", "ClippingGeometry", "NO_MAINTAIN_EXTENT")

def calculo(formula, ruta_salida):
    arcpy.gp.RasterCalculator_sa(formula, ruta_salida)


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

crear(rutaDefecto)

if( coordenada == '' ):
    coordenada = "PROJCS['WGS_1984_UTM_Zone_19S',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',10000000.0],PARAMETER['Central_Meridian',-69.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"

if(L == ""):
    L = 0

now = datetime.now()
nombreFinal = current_date_format(now) + nombre
nombreFinal2 = current_date_format(now) + nombre2

rutaTemporal = rutaDefecto + '\\Temporal\\' + nombreFinal + ".tif"
rutaTemporal2 = rutaDefecto + '\\Temporal\\' + nombreFinal2 + ".tif"

arcpy.AddMessage("*************PROCESANDO CICLO 1************")

# Process: Proyectar ráster
rectificarCoordenadas(Raster_de_entrada, rutaTemporal, coordenada)
rectificarCoordenadas(Raster_de_entrada2, rutaTemporal2, coordenada)

arcpy.AddMessage("*************INICIANDO CICLO 2************")
######################################################### CICLO 2 ######################################################################
# Local variables:
ruta_temporal_re_1 = rutaDefecto + '\\Temporal\\' + nombreFinal + "_re.tif"
ruta_temporal_re_2 = rutaDefecto + '\\Temporal\\' + nombreFinal2 + "_re.tif"

# Process: Recortar
primer_recorte(rutaTemporal, ruta_temporal_re_1, shapefile)
primer_recorte(rutaTemporal2, ruta_temporal_re_2, shapefile)

# Local variables:
x = ruta_temporal_re_1
y = ruta_temporal_re_2

formula = "( ( Float(",x,") - Float(",y,") ) / ( Float(",x,") + Float(",y,") + ",L," ) ) * ( 1 + ",L,")"
ruta_salida = rutaDefecto + '\\Temporal\\' + nombreFinal + nombre2 + "_cal.tif" # MAY19B3B5_cal.tif

# Process: Calculadora ráster
calculo(formula, ruta_salida)

arcpy.AddMessage("*************PROCESADO CICLO 2************")

#arcpy.AddMessage("*************INICIANDO CICLO 3************")
######################################################### CICLO 3 ######################################################################