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
driverGTiff = gdal.GetDriverByName('GTiff')
driverGTiff.Register()
driverGeoTIFF = gdal.GetDriverByName('GeoTIFF')
driverGTiff.Register()


####################
####################
### Tuile 31TFJ ####
####################
####################


#Ouverture fichiers

#se placer dans le répertoire 

repDonnees = r"sortie31TFJ"

#creation liste des sous-répertoires

listeRep = os.listdir(repDonnees)

print(listeRep[0])

for i in range (len(listeRep)):
    repCourant = os.path.join(repDonnees, listeRep[0])
    fichiersRep = os.listdir(repCourant)
    B2 = [f for f in fichiersRep if 'B2' in f]
    B3 = [f for f in fichiersRep if 'B3' in f]
    B4 = [f for f in fichiersRep if 'B4' in f]
    B5 = [f for f in fichiersRep if 'B5' in f]
    B6 = [f for f in fichiersRep if 'B6' in f]
    B7 = [f for f in fichiersRep if 'B7' in f]
    B8 = [f for f in fichiersRep if 'B8' in f]
    del B8[1]
    B8A = [f for f in fichiersRep if 'B8A' in f]
    B11 = [f for f in fichiersRep if 'B11' in f]
    B12 = [f for f in fichiersRep if 'B12' in f]
    masqueCLM = [f for f in fichiersRep if 'CLM' in f]
    
    nomPartiesImage = os.path.basename(fichiersRep[0]).split("_")
    sat = nomPartiesImage[0]
    date = nomPartiesImage[1]
    tuile = nomPartiesImage[2]
    bande = nomPartiesImage[3]
    
 
    
print(B8A)





masque = gdal.Open(cheminMasque)
raster = gdal.Open(cheminRaster)

type(masque)
type(raster)


#Vérification Systeme de projection

rasterSrs = raster.GetSpatialRef()
rasterSpatialRef = osr.SpatialReference()

type(rasterSpatialRef)
type(rasterSrs)

bandesR = raster.RasterCount()


rasterSpatialRef.ImportFromWkt(raster.GetProjection())
if not rasterSrs.IsSame(rasterSpatialRef): 
                        print("Warning : invalid layer, wrong SRS" )
                        sys.exit(1)
#Bandes
                        
bande1 = raster.GetRasterBand(1)
bande2 = raster.GetRasterBand(2)
bande3 = raster.GetRasterBand(3)
bande4 = raster.GetRasterBand(4)
bande5 = raster.GetRasterBand(5)
bande6 = raster.GetRasterBand(6)
bande7 = raster.GetRasterBand(7)
bande8 = raster.GetRasterBand(8)
bande8a = raster.GetRasterBand(9)
bande11 = raster.GetRasterBand(12)
bande12 = raster.GetRasterBand(13)


test = raster.BandReadAsArray()
print(test)
type(test)

band = raster.GetRasterBand(1)
type(band)
test2 = bande1.BandReadAsArray()
print(test2)


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

