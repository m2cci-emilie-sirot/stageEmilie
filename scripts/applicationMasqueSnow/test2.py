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

# dico = {'01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'}
dico = {}
dicoPourcentage = {}

#creation liste des sous-répertoires (les différentes dates de la tuile)

listeRep = os.listdir(repDonnees)


for i in range (len(listeRep)):
    repCourant = os.path.join(repDonnees, listeRep[i])#se positionne dans le répertoire d'une date
    fichiersRep = os.listdir(repCourant)#liste les fichiers à savoir les différentes bandes
    
    masque = [f for f in fichiersRep if 'masque' in f]
    
    nomPartiesImage = os.path.basename(masque[0]).split("_")#séparer les parties du fichier en cours de traitement pour les réutiliser pour la sortie
    sat = nomPartiesImage[0]
    date = nomPartiesImage[1]
    tuile = nomPartiesImage[2]
    masqueConverti = nomPartiesImage[3]+"Snow"
    
    
#définir les répertoires en sortie  
    rep = f"{sat}_{date}_{tuile}"
    repSortieDate = os.path.join(repSortie, rep)
    os.makedirs(repSortieDate, exist_ok=True) # création du dossier sur le disque
 
            
#Lire la valeur des points TFE sur les pixels correspondant du masque



    TFEChemin = "TFE/tfe_bio_T31TFJ_WGS84.shp"
    TFE = gpd.read_file(TFEChemin) #ouverture du shp

    
    listePixTFE = []
    
    
    for j in range(len(TFE)):
    
        x = TFE.iloc[j].geometry.centroid.x #récupère les coordonnées d'un point
        y = TFE.iloc[j].geometry.centroid.y
        

        
        masqueSnow = Image.open(repDonnees+'/'+listeRep[i]+'/'+masque[0], 'r')
       
        
        
        pix = masqueSnow.load()
        
        # print(masqueSnow.size)
        # pixel_values = list(masqueSnow.getdata())
        
    
        listePixTFE.append(pix[x,y])
      
              
        nombreNoData = listePixTFE.count(205)
        pourcentage = (100*nombreNoData)/111
        
        dico[date] = listePixTFE
        dicoPourcentage[date] = pourcentage
        






