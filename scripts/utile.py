#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 12 09:18:15 2021

@author: Emilie Sirot
"""

#Librairies
import os
from pprint import pprint
from osgeo import gdal
from PIL import Image
import PIL
import numpy
import numpy as np
from osgeo.gdalconst import *
import matplotlib.pyplot as plt
from matplotlib import patches as mpatches, colors
import earthpy as et
import earthpy.plot as ep
import earthpy.mask as em
from earthpy.mask import mask_pixels 
from __future__ import absolute_import, print_function, division
import itertools
import os
from osgeo import gdal, gdal_array, gdalnumeric, ogr, osr
import glob
import numpy as np
import os.path
from os.path import basename, abspath, dirname, realpath, splitext
import rasterio
import sys
from osgeo.gdalconst import GA_ReadOnly
from osgeo import gdal


#drivers 

driverOGROSR = gdal.GetDriverByName('ESRI Shapefile')
driverSRTMHGT = gdal.GetDriverByName('SRTMHGT')
driverSRTMHGT.Register()
driverGTiff = gdal.GetDriverByName('GTiff')
driverGTiff.Register()
driverGeoTIFF = gdal.GetDriverByName('GeoTIFF')
driverGTiff.Register()

#ouvrir un fichier

rasterPIL = Image.open(chemin)
rastereGdal = gdal.Open(chemin)
rasterRasterio = rasterio.open(chemin])

#transformer en Array

rasterToArrayRasterio = raster.read(1) #le paramètre est le numéro de bande
rasterToArrayNumpy = numpy.array(raster)

#Color interpretation

profile = src.profile
profile['photometric'] = "RGB"
with rasterio.open("/tmp/rgb.tif", 'w', **profile) as dst:
    dst.write(src.read())

#Vérification Systeme de projection

rasterSrs = raster.GetSpatialRef()
rasterSpatialRef = osr.SpatialReference()

type(rasterSpatialRef)
type(rasterSrs)

bandesR = raster.RasterCount()


rasterSpatialRef.ImportFromWkt(raster.GetProjection())
if not rasterSrs.IsSame(rasterSpatialRef): 
                        print("Warning : invalid layer, wrong SRS" )


#Vérifier résolution spatiale

cheminRaster = r"donnees/S2A_20170702_T31TFJ_image_CMP_R2"
raster = gdal.Open(cheminRaster) #Ouvrir le fichier
gt = raster.GetGeoTransform()

print("Origin = ({}, {})".format(gt[0], gt[3]))
print("Pixel Size = ({}, {})".format(gt[1], gt[5]))

#Informations raster

print(raster.GetMetadata)

print("Driver: {}/{}".format(raster.GetDriver().ShortName,
                            raster.GetDriver().LongName)) #Drivers nécessaires ?
print("Size is {} x {} x {}".format(raster.RasterXSize,
                                    raster.RasterYSize,
                                    raster.RasterCount)) #Taille du raster

print("Projection is {}".format(raster.GetProjection())) #Information systeme de projection
print("Band Type={}".format(gdal.GetDataTypeName(bande1.DataType))) #information type bande

#Shapefile


point = "TFE/test.shp"

testPoint = ogr.Open(point, update = 0) #ouvrir le shp
testPointRef = testPoint.GetLayer()

print(testPointRef.GetFeatureCount())#compter le nombre d'objet

#Sélection sur un shapefile
query='SURFACE > 1000'
Layer_ref.SetAttributeFilter(query)