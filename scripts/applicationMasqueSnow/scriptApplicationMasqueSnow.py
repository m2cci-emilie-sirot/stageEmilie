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
import PIL
import numpy
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

#drivers

driverOGROSR = gdal.GetDriverByName('ESRI Shapefile')
driverSRTMHGT = gdal.GetDriverByName('SRTMHGT')
driverSRTMHGT.Register()
driverGTiff = gdal.GetDriverByName('GTiff')
driverGTiff.Register()
driverGeoTIFF = gdal.GetDriverByName('GeoTIFF')
driverGTiff.Register()

gdal.AllRegister()



####################
####################
### Tuile 31TFJ ####
####################
####################


#Ouverture fichiers

#se placer dans le répertoire "sortie" de la tuile

repDonnees = r"sortie31TFJ"
repSortie = "/home/sirote/Documents/stageEmilie/scripts/decoupageEmpriseZip/sortie"

#creation liste des sous-répertoires

listeRep = os.listdir(repDonnees)

print(listeRep[1])

for i in range (len(listeRep)):
    repCourant = os.path.join(repDonnees, listeRep[1])
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
    
    listeBandes = B2+B3+B4+B5+B6+B7+B8+B8A+B11+B12
    
    nomPartiesImage = os.path.basename(fichiersRep[1]).split("_")
    sat = nomPartiesImage[0]
    date = nomPartiesImage[1]
    tuile = nomPartiesImage[2]
    bande = nomPartiesImage[3]
    
    

#test mask earthpy 

#B2rasterio = Image.open(repCourant+'/'+B2[0])

B2ouverture = gdal.Open(repCourant+'/'+B2[0])

#masqueRasterio = Image.open(repCourant+'/'+masqueCLM[0])

masqueRasterio = gdal.Open(repCourant+'/'+masqueCLM[0])

B2array = numpy.array(B2rasterio)
masqueArray = numpy.array(masqueRasterio)

print(B2array)


B2masque = mask_pixels(B2array,masqueArray, vals=[0])

print(B2masque)

nrows, ncols = np.shape(B2masque)


outputRaster = gdal.GetDriverByName('GTiff').Create('sortieRaster.tiff',ncols, nrows, 1, gdal.GDT_Float32)

srs = osr.SpatialReference()
srs.ImportFromEPSG(32631)

outputRaster.SetProjection(srs.ExportToWkt())
outputRaster.GetRasterBand(1).WriteArray(B2masque)
outputRaster.FlushCache()

####

sortieTest = os.path.join(repSortie, "maskTest.tif")
with rasterio.open(repCourant+'/'+masqueCLM[0], "r") as src:
                                mask_cld1=src.read(1)
                                listb = np.where(mask_cld1==0,1,np.nan)
                                with rasterio.open(sortieTest,"w",**src.profile) as dest :
                                    dest.write(listb.astype(rasterio.uint8),1)


 with rasterio.open(sortieTest, "r") as src:
                                mask_cld = src.read(1)
                                profile = src.profile
                                profile.update(dtype=rasterio.float64,
                                       count=1,
                                       compress='lzw',
                                       nodata=np.nan)
                                msk_name = nomPartiesImage[0]
                        if not os.path.exists(os.path.join(repSortie, msk_name+"_msk_scaling.tif")):
                            img = (repCourant+'/'+B2[0])
                            with rasterio.open(img, "r") as src:
                                band = src.read(1)
                                band = band.astype(np.float64)
                                band /= 10000 # band = band / 10000
                                #band[band == 0] = np.nan
                                profile = src.profile
                                profile.update(
                                        dtype=rasterio.float64,
                                        count=1,
                                        compress='lzw',
                                        nodata=np.nan)
                                msk2 = np.multiply(mask_cld, band)
                                msk2[msk2 == 0] = np.nan
                                with rasterio.open(os.path.join(repSortie, msk_name+"_msk_scaling.tif"), "w", **profile) as dst:
                                    dst.write(msk2.astype(rasterio.float64), 1)


                                x=msk2.shape
                                y=x[0]*x[1]
                                it=0
                                for i in msk2:
                                    if(i=="nan"):
                                        it+=1

                                mon_fichier = "open(os.path.join(rep,"liste_images.txt"), "a")"
                                mon_fichier.write(msk_name + " " + str(it/y) + "\n")
                                mon_fichier.close()


####


B2masqueTif = Image.fromarray(B2masque)
type(B2masqueTif)
type(B2rasterio)


spatialRefsortie = B2masqueTif.GetSpatialRef()
sortieTif = B2masqueTif.save("test.tiff")



nomBande = f"{sat}_{date}_{tuile}_{bande}"
fichierSortie = os.path.join(repSortie, nomBande)
sortieTif = gdal.Warp(fichierSortie,
                      "/home/sirote/Documents/stageEmilie/applicationMasqueSnow/donnees/S2A_20170702_T31TFJ_B2",
                       creationOptions=['COMPRESS=LZW', 'PREDICTOR=2'], # compression du tif
                       dstNodata=-10000, # valeur de nodata
                       xRes=10, yRes=-10, # résolution de sortie
                       targetAlignedPixels=True, # on garde le même emplacement des pixels que l'image de départ
                       cropToCutline=True 
                       )

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

