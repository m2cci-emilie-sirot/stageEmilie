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
    
    nomPartiesImage = os.path.basename(masqueSnow[0]).split("_")#séparer les parties du fichier en cours de traitement pour les réutiliser pour la sortie
    sat = nomPartiesImage[0]
    date = nomPartiesImage[1]
    tuile = nomPartiesImage[2]
    masque = nomPartiesImage[3]+"Snow"
    
    
# #définir les répertoires en sortie  
#     rep = f"{sat}_{date}_{tuile}"
#     repSortieDate = os.path.join(repSortie, rep)
#     os.makedirs(repSortieDate, exist_ok=True) # création du dossier sur le disque
    
#ouvrir les TFE

    TFEChemin = "TFE/tfe_bio_T31TFJ_WGS84.shp"    
    # TFE = ogr.Open(TFEChemin)
    TFE = gpd.read_file(TFEChemin) #ouverture du shp
     
    listeCoordonnees = []
     
    for j in range(len(TFE)):
        x = TFE.iloc[j].geometry.centroid.x #récupère les coordonnées d'un point
        y = TFE.iloc[j].geometry.centroid.y
     
        listeCoordonnees.append((x,y))
           
#ouverture masque avec GDAL

    masque = gdal.Open(repDonnees+'/'+listeRep[i]+'/'+masqueSnow[0])
    # TFELayer = TFEGDAL.GetLayer()  
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

    listePixTFE = []
    
    for point in listeCoordonnees:
        col = int((point[0] - xOrigin) / pixelWidth)
        row = int((yOrigin - point[1] ) / pixelHeight)
        
        listePixTFE.append(masqueArray[row][col])
        
        print(row,col, masqueArray[row][col])

#creer dictionnaire des valeurs des pixels rangés par date

    
    dico[date] = listePixTFE
    
    
    NoData = (100*(listePixTFE.count(254)))/111
    Neige = (100*(listePixTFE.count(100)))/111
    Nuages = (100*(listePixTFE.count(205)))/111
    Rien = (100*(listePixTFE.count(0)))/111
    
    listePourcentage = [NoData, Neige, Nuages, Rien]

    dicoPourcentage[date] = listePourcentage


#graphique


listeDate = list(dicoPourcentage)
ind = [x for x, _ in enumerate(listeDate)]#taille

plt.figure()

plt.rcParams['axes.facecolor']='black'


for d in range(len(listeDate)):
    

    
    GNoData = np.array(dicoPourcentage[listeDate[d]][0])
    GNeige = np.array(dicoPourcentage[listeDate[d]][1])
    GNuages = np.array(dicoPourcentage[listeDate[d]][2])
    GExploitable = np.array(dicoPourcentage[listeDate[d]][3])
    
   
    
    
    plt.bar(d, GNoData, width=0.8,color='#4B4847', bottom=GNeige+GNuages+GExploitable)
    plt.bar(d, GNeige, width=0.8,color='white', bottom=GNuages+GExploitable)
    plt.bar(d, GNuages, width=0.8,color='darkgrey', bottom=GExploitable)
    plt.bar(d, GExploitable, width=0.8,color='lightgreen')
    
    

plt.xticks(ind, listeDate)
plt.ylabel('Pourcentage de points TFE ')
plt.xlabel('Dates')
plt.legend(labels=['NoData','Neige','Nuages','Exploitable'],loc="upper right", facecolor="white")
plt.title("Etat des pixels selon les points de mesure (TFE)")
    
plt.ylim = 1.0
    
plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    
    

        
plt.savefig('sortie/sortieT31TFJ/graphiqueT31TFJ.png', dpi = 300)

plt.show()


