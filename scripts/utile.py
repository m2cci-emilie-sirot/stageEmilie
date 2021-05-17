#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 12 09:18:15 2021

@author: Emilie Sirot
"""

from osgeo import gdal

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

