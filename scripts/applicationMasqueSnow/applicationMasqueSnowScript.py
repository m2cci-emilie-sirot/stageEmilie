#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 14:15:37 2021

@author: Emilie sirot
"""
import os
from osgeo import gdal
from osgeo import ogr
import numpy
import numpy as np
import rasterio
from PIL import Image
import geopandas as gpd
from pyproj import Proj, transform
import matplotlib.pyplot as plt

#drivers

gdal.AllRegister()

#se placer dans le répertoire "applicationMasqueSnow"

#traitements des images(par bande) par tuile
  
####################
####################
### Tuile 31TFJ ####
####################
####################


#Ouverture fichiers

repDonnees = r"../decoupageEmpriseZipSnow/sortie/sortieT31TFJ"
repSortie = "sortie/sortieT31TFJ"


dico = {} #dico qui va contenir les valeurs des pixels
dicoPourcentage = {}

#creation liste des sous-répertoires (les différentes dates de la tuile)

listeRep = os.listdir(repDonnees)


for i in range (len(listeRep)):
    repCourant = os.path.join(repDonnees, listeRep[i])#se positionne dans le répertoire d'une date
    fichiersRep = os.listdir(repCourant)#liste les fichiers à savoir les différentes bandes
    
    masqueSnow = [f for f in fichiersRep if 'masque' in f]
    
#     nomPartiesImage = os.path.basename(masque[0]).split("_")#séparer les parties du fichier en cours de traitement pour les réutiliser pour la sortie
#     sat = nomPartiesImage[0]
#     date = nomPartiesImage[1]
#     tuile = nomPartiesImage[2]
#     masque = nomPartiesImage[3]+"Snow"
    
    
# #définir les répertoires en sortie  
#     rep = f"{sat}_{date}_{tuile}"
#     repSortieDate = os.path.join(repSortie, rep)
#     os.makedirs(repSortieDate, exist_ok=True) # création du dossier sur le disque
    
#ouvrir les TFE

     TFEChemin = "TFE/tfe_bio_T31TFJ.shp"    
     TFE = ogr.Open(TFEChemin)
     
#ouverture masque avec GDAL

     masque = gdal.Open(repDonnees+'/'+listeRep[i]+'/'+masqueSnow[0])
     TFELayer = TFEGDAL.GetLayer()  
     band = masque.GetRasterBand(1)       
     cols = masque.RasterXSize
     rows = masque.RasterYSize
     transform = masque.GetGeoTransform()
     xOrigin = transform[0]
     yOrigin = transform[3]
     pixelWidth = transform[1]
     pixelHeight = -transform[5]
     masqueArray = band.ReadAsArray(0, 0, cols, rows)
     
#lire la valeur des points TFE sur les pixels correspondant du masque

   
 
   
    
    
    
    
    
    # points_list = [ (x, y) ] #list of X,Y coordinates
    
    # for point in listeC:
    #     col = int((point[0] - xOrigin) / pixelWidth)
    #     row = int((yOrigin - point[1] ) / pixelHeight)
    
    
     for point in listeC:
        col = int((point[0] - xOrigin) / pixelWidth)
        row = int((yOrigin - point[1] ) / pixelHeight)
        
        
       
        print(row,col, masqueArray[row][col])


     
    
       

####



   
    TFE = gpd.read_file(TFEChemin) #ouverture du shp
    listePixTFE = []
    
    for j in range(len(TFE)):
    
        x = TFE.iloc[j].geometry.centroid.x #récupère les coordonnées d'un point
        y = TFE.iloc[j].geometry.centroid.y
        
        #conversion des coordonnées (ESPG 3827 vers ESPG 4326)
        p = Proj("+proj=merc +lon_0=0 +k=1 +x_0=0 +y_0=0 +a=6378137 +b=6378137 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs")
        lon, lat = p(x, y, inverse=True)
        print(lat, lon)
        
        masqueSnow = Image.open(repSortieDate+'/'+masqueSnowConverti[0])
        pix = masqueSnow.load()
        listePixTFE.append(pix[lon,lat])
        
        splitDate = []
        
        for k in range(0, len(date), 2):
            splitDate.append(date[k : k + 2])
        
            
        nombreNoData = listePixTFE.count(0)
        pourcentage = (100*nombreNoData)/111
        
        dico[date] = listePixTFE
        dicoPourcentage[date] = pourcentage
        
        
        
        
        
        
        
        # plt.bar(range(len(dico)), list(dico.values()), align='center')
        # plt.xticks(range(len(dico)), list(dico.keys()))







