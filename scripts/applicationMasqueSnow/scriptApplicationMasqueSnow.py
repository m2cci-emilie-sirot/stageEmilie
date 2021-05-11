#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 10:01:24 2021

@author: sirote
"""


import os
from pprint import pprint
from osgeo import gdal
from PIL import Image
import numpy

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

#drivers

driverOGROSR = gdal.GetDriverByName('ESRI Shapefile')
driverSRTMHGT = gdal.GetDriverByName('SRTMHGT')
driverSRTMHGT.Register()



#ouverture fichiers

cheminRaster = r"donnees/S2A_20170702_T31TFJ_image_CMP_R2"
cheminMasque = r"donnees/S2A_20170702_T31TFJ_masque_SNW_R2"

masque = gdal.Open(cheminMasque)
raster = gdal.Open(cheminRaster)

type(masque)
type(raster)
raster.GetProjection()
raster.GetSpatialRef()

rasterSrs = raster.GetSpatialRef()
rasterSpatialRef = osr.SpatialReference()

type(rasterSpatialRef)
type(rasterSrs)

rasterSpatialRef.ImportFromWkt(raster.GetProjection())
if not rasterSrs.IsSame(rasterSpatialRef): 
                        print("Warning : invalid layer, wrong SRS" )
                        sys.exit(1)

gt = raster.GetGeoTransform()
pixelSizeX = gt[1]

gtmasque = masque.GetGeoTransform()


cheminTest = r"donnees/testLamb.tif"
rasterTest = gdal.Open(cheminTest)
type(rasterTest)

rasterTestSrs = rasterTest.GetSpatialRef()

rasterSpatialRef.ImportFromWkt(raster.GetProjection())
if not rasterTestSrs.IsSame(rasterSpatialRef): 
                        print("Warning : invalid layer, wrong SRS" )
                        sys.exit(1)


band = raster.GetRasterBand(1)
type(band)

raster.show()

#numpy

raster2 = Image.open(cheminRaster)
type(raster2)
raster2.show()
imarray = numpy.array(raster2)
print(raster2)

#ouverture fichier rasterio

raster3 = rasterio.open(cheminRaster)
raster3.crs


#vérification du système de coordonnées des images et changement de système si besoin

