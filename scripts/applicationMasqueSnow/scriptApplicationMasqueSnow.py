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
import zipfile
import os.path
from os.path import basename, abspath, dirname, realpath, splitext
import rasterio
import sys
from osgeo.gdalconst import GA_ReadOnly

#drivers
driverOGROSR = ogr.GetDriverByName('ESRI Shapefile')
dataset = driverOGROSR.Open(r'donnees/S2A_20170702_T31TFJ_image_CMP_R2')

rastertest3 = Image.open('donnees/S2A_20170702_T31TFJ_image_CMP_R2')
rastertest3.show()
imarray = numpy.array(rastertest3)

raster = dataset.GetLayer()
rasterSCR = raster.GetSpatialRef()


gdal.AllRegister()
driver = gdal.GetDriverByName('STRMHGT')
driver.Register()

raster = rasterio.open("donnees/S2A_20170702_T31TFJ_image_CMP_R2")

rasterSCR = raster.GetSpatialRef()


ORaster = gdal.Open(raster, gdal.GA_ReadOnly)

repDonnees = "donnees"

#vérification du système de coordonnées des images et changement de système si besoin

