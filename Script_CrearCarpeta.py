import os
import arcpy

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
        os.makedirs(rutaDefecto + '\\Data\\')
    except:
        pass

    try:
        os.makedirs(rutaDefecto + '\\Imagenes\\')
    except:
        pass


arcpy.AddMessage("*************OK***************")
rutaDefecto = arcpy.GetParameterAsText(0)
arcpy.AddMessage("*************PROCESANDO************")
creacion_carpetas(rutaDefecto)
arcpy.AddMessage("*************PROCESADO************")
