# -*- #################
# ---------------------------------------------------------------------------
# COMANDOS.py
# Authors: Franz Cortez, Julio Cerna
# Usage: COMANDOS <Ráster_de_entrada> 
# Description: 
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

# Script arguments
arcpy.AddMessage("*************OK***************")

nombre = arcpy.GetParameterAsText(0).upper()
rutaDefecto = arcpy.GetParameterAsText(1)
Raster_de_entrada = arcpy.GetParameterAsText(2)
nombre2 = arcpy.GetParameterAsText(3).upper()
Raster_de_entrada2 = arcpy.GetParameterAsText(4)

crear(rutaDefecto)

now = datetime.now()
nombreFinal = current_date_format(now) + nombre
nombreFinal2 = current_date_format(now) + nombre2

rutaTemporal = rutaDefecto + '\\Temporal\\' + nombreFinal
rutaTemporal2 = rutaDefecto + '\\Temporal\\' + nombreFinal2

arcpy.AddMessage("*************PROCESANDO************")
# Process: Proyectar ráster
arcpy.ProjectRaster_management(str(Raster_de_entrada) , str(rutaTemporal), out_coor_system="PROJCS['WGS_1984_UTM_Zone_19S',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',10000000.0],PARAMETER['Central_Meridian',-69.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]", resampling_type="NEAREST", cell_size="30 30", geographic_transform="", Registration_Point="", in_coor_system="PROJCS['WGS_1984_UTM_Zone_19N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-69.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]", vertical="NO_VERTICAL")

arcpy.ProjectRaster_management(str(Raster_de_entrada2) , str(rutaTemporal2), out_coor_system="PROJCS['WGS_1984_UTM_Zone_19S',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',10000000.0],PARAMETER['Central_Meridian',-69.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]", resampling_type="NEAREST", cell_size="30 30", geographic_transform="", Registration_Point="", in_coor_system="PROJCS['WGS_1984_UTM_Zone_19N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-69.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]", vertical="NO_VERTICAL")

arcpy.AddMessage("*************PROCESADO************")
