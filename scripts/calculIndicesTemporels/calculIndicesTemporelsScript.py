#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 11:38:18 2021

@author: Emilie Sirot
"""


import os
from osgeo import gdal
import itertools
import rasterio
import numpy as np 
import geopandas as gpd
import pandas as pd

####################
####################
### Tuile 31TFJ ####
####################
####################

#Lister les indices souhaités

listeIndices= [ ]

#ouvrir les TFE

TFEChemin = "TFE/tfe_bio_T31TFJ_WGS84.shp"    
TFE = gpd.read_file(TFEChemin) #ouverture du shp
   
listeCoordonnees = []
     
for j in range(len(TFE)):
    x = TFE.iloc[j].geometry.centroid.x #récupère les coordonnées d'un point
    y = TFE.iloc[j].geometry.centroid.y
     
    listeCoordonnees.append((x,y))
        
         

#ouverture des bandes
  
repDonnees = r"../applicationMasque/sortie/sortieT31TFJ"
repSortie = "sortie/sortieT31TFJ"

listeRep = os.listdir(repDonnees)


for i in range (len(listeRep)):
    repCourant = os.path.join(repDonnees, listeRep[i])#se positionne dans le répertoire d'une date
    fichiersRep = os.listdir(repCourant)#liste les fichiers à savoir les différentes bandes

    
    B2 = [f for f in fichiersRep if 'B2' in f]
    B3 = [f for f in fichiersRep if 'B3' in f]
    B4 = [f for f in fichiersRep if 'B4' in f]
    B5 = [f for f in fichiersRep if 'B5' in f]
    B6 = [f for f in fichiersRep if 'B6' in f]
    B7 = [f for f in fichiersRep if 'B7' in f]
    B8 = [f for f in fichiersRep if 'B8' in f]
    B8.sort()
    del B8[0]
    B8A = [f for f in fichiersRep if 'B8A' in f]
    B11 = [f for f in fichiersRep if 'B11' in f]
    B12 = [f for f in fichiersRep if 'B12' in f]
    
    
    #définir le nom des répertoires en sortie
    
    nomParties = os.path.basename(B2[0]).split("_")
    sat = nomParties[0]
    date = nomParties[1]
    tuile = nomParties[2]
    
    nomSortieTab = f"{sat}_{date}_{tuile}_tableau.csv"
    
#caracteristiques de l'image
    
                   
    imageRef = gdal.Open(repCourant+'/'+B2[0])
    cols = imageRef.RasterXSize
    rows = imageRef.RasterYSize
    transform = imageRef.GetGeoTransform()
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = -transform[5]
    
    
    legende = ["date","indices","bandes"]
    for gid in range(len(TFE.gid)):
        legende.append(TFE.gid[gid])
    
     Typo_Veget = ["/","/"]
    for typoveget in range(len(TFE.Typo_Veget)):
        Typo_Veget.append(TFE.Typo_Veget[typoveget])
    
    Id_sitesAS = ["/","/"]
    for IdsitesAS in range(len(TFE.Id_sitesAS)):
        Id_sitesAS.append(TFE.Id_sitesAS[IdsitesAS])
    
    Releve = ["/","/"]
    for releve in range(len(TFE.Releve)):
        Releve.append(TFE.Releve[releve])
        



   #creation du tableau
    
    tab = pd.DataFrame(columns = legende)
    tab.loc[1]=Id_sitesAS
    tab.loc[2]=Releve
    tab.loc[3]=Typo_Veget

    index = 4