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


#fonction qui servira à representer les différentes dates sur le graphique 
def conversionJour(date) : 
    mois1 = 0
    mois2 = 31
    mois3 = 59
    mois4 = 90
    mois5 = 120
    mois6 = 151
    mois7 = 181
    mois8 = 212
    mois9 = 243
    mois10 = 273
    mois11 = 304
    mois12 = 334

    splitDate = []
    for k in range(0, len(date), 2):
        splitDate.append(date[k : k + 2])
        
    if splitDate[2] == '01':
        mois = mois1
    elif splitDate[2] == '02':
        mois = mois2
    elif splitDate[2] == '03':
        mois = mois3
    elif splitDate[2] == '04':
        mois = mois4
    elif splitDate[2] == '05':
        mois = mois5
    elif splitDate[2] == '06':
        mois = mois6
    elif splitDate[2] == '07':
        mois = mois7
    elif splitDate[2] == '08':
        mois = mois8
    elif splitDate[2] == '09':
        mois = mois9
    elif splitDate[2] == '10':
        mois = mois10
    elif splitDate[2] == '11':
        mois = mois11
    elif splitDate[2] == '12':
        mois = mois12


    jour = int(splitDate[3]) + mois
    return jour



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
    

#ouvrir les TFE

    TFEChemin = "TFE/tfe_bio_T31TFJ_WGS84.shp"    
    TFE = gpd.read_file(TFEChemin) #ouverture du shp
     
    listeCoordonnees = []
     
    for j in range(len(TFE)):
        x = TFE.iloc[j].geometry.centroid.x #récupère les coordonnées d'un point
        y = TFE.iloc[j].geometry.centroid.y
     
        listeCoordonnees.append((x,y))
           
#ouverture masque avec GDAL

    masque = gdal.Open(repDonnees+'/'+listeRep[i]+'/'+masqueSnow[0])
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

index = [ind for ind in range(365)]

mois = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 
         'Septembre', 'Octobre', 'Novembre', 'Décembre']


    
conversionTest = conversionJour('20170712')
    

plt.figure()

plt.rcParams['axes.facecolor']='black'


for d in range(len(listeDate)):
    
    indexDate = conversionJour(listeDate[d])
    
    GNoData = np.array(dicoPourcentage[listeDate[d]][0])
    GNeige = np.array(dicoPourcentage[listeDate[d]][1])
    GNuages = np.array(dicoPourcentage[listeDate[d]][2])
    GExploitable = np.array(dicoPourcentage[listeDate[d]][3])
    
   
    
    
    plt.bar(indexDate, GNoData, width=0.8,color='grey', bottom=GNeige+GNuages+GExploitable)
    plt.bar(indexDate, GNeige, width=0.8,color='#6082EF', bottom=GNuages+GExploitable)
    plt.bar(indexDate, GNuages, width=0.8,color='red', bottom=GExploitable)
    plt.bar(indexDate, GExploitable, width=0.8,color='lightgreen')
    
    

plt.xticks([0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334], mois)
plt.ylabel('Pourcentage de points TFE ')
plt.xlabel('Dates')
plt.legend(labels=['NoData','Neige','Nuages','Exploitable'],loc="upper right", facecolor="white")
plt.title("Etat des pixels selon les points de mesure (TFE)")
plt.xlim = (1,365)
plt.ylim = 1.0
    
plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    
plt.tight_layout()

        
plt.savefig('sortie/sortieT31TFJ/graphiqueSnowT31TFJ.png', dpi = 300)

plt.show()

####################
####################
### Tuile 31TFK ####
####################
####################


#Ouverture fichiers

repDonnees = r"../decoupageEmpriseZipSnow/sortie/sortieT31TFK"
repSortie = "sortie/sortieT31TFK"


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
    
    

#ouvrir les TFE

    TFEChemin = "TFE/tfe_bio_T31TFK_WGS84.shp"    
    TFE = gpd.read_file(TFEChemin) #ouverture du shp
     
    listeCoordonnees = []
     
    for j in range(len(TFE)):
        x = TFE.iloc[j].geometry.centroid.x #récupère les coordonnées d'un point
        y = TFE.iloc[j].geometry.centroid.y
     
        listeCoordonnees.append((x,y))
           
#ouverture masque avec GDAL

    masque = gdal.Open(repDonnees+'/'+listeRep[i]+'/'+masqueSnow[0])  
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

index = [ind for ind in range(365)]

mois = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 
         'Septembre', 'Octobre', 'Novembre', 'Décembre']


    
conversionTest = conversionJour('20170712')
    



plt.figure()

plt.rcParams['axes.facecolor']='black'


for d in range(len(listeDate)):
    
    indexDate = conversionJour(listeDate[d])
    
    GNoData = np.array(dicoPourcentage[listeDate[d]][0])
    GNeige = np.array(dicoPourcentage[listeDate[d]][1])
    GNuages = np.array(dicoPourcentage[listeDate[d]][2])
    GExploitable = np.array(dicoPourcentage[listeDate[d]][3])
    
   
    
    
    plt.bar(indexDate, GNoData, width=0.8,color='grey', bottom=GNeige+GNuages+GExploitable)
    plt.bar(indexDate, GNeige, width=0.8,color='#6082EF', bottom=GNuages+GExploitable)
    plt.bar(indexDate, GNuages, width=0.8,color='red', bottom=GExploitable)
    plt.bar(indexDate, GExploitable, width=0.8,color='lightgreen')
    
    

plt.xticks([0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334], mois)
plt.ylabel('Pourcentage de points TFE ')
plt.xlabel('Dates')
plt.legend(labels=['NoData','Neige','Nuages','Exploitable'],loc="upper right", facecolor="white")
plt.title("Etat des pixels selon les points de mesure (TFE)")
plt.xlim = (1,365)
plt.ylim = 1.0
    
plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    
plt.tight_layout()

        
plt.savefig('sortie/sortieT31TFK/graphiqueSnowT31TFK.png', dpi = 300)

plt.show()

####################
####################
### Tuile 31TGK ####
####################
####################


#Ouverture fichiers

repDonnees = r"../decoupageEmpriseZipSnow/sortie/sortieT31TGK"
repSortie = "sortie/sortieT31TGK"


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
    

#ouvrir les TFE

    TFEChemin = "TFE/tfe_bio_T31TGK_WGS84.shp"    
    TFE = gpd.read_file(TFEChemin) #ouverture du shp
     
    listeCoordonnees = []
     
    for j in range(len(TFE)):
        x = TFE.iloc[j].geometry.centroid.x #récupère les coordonnées d'un point
        y = TFE.iloc[j].geometry.centroid.y
     
        listeCoordonnees.append((x,y))
           
#ouverture masque avec GDAL

    masque = gdal.Open(repDonnees+'/'+listeRep[i]+'/'+masqueSnow[0]) 
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

index = [ind for ind in range(365)]

mois = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 
         'Septembre', 'Octobre', 'Novembre', 'Décembre']


    
conversionTest = conversionJour('20170712')
    



plt.figure()

plt.rcParams['axes.facecolor']='black'


for d in range(len(listeDate)):
    
    indexDate = conversionJour(listeDate[d])
    
    GNoData = np.array(dicoPourcentage[listeDate[d]][0])
    GNeige = np.array(dicoPourcentage[listeDate[d]][1])
    GNuages = np.array(dicoPourcentage[listeDate[d]][2])
    GExploitable = np.array(dicoPourcentage[listeDate[d]][3])
    
   
    
    
    plt.bar(indexDate, GNoData, width=0.8,color='grey', bottom=GNeige+GNuages+GExploitable)
    plt.bar(indexDate, GNeige, width=0.8,color='#6082EF', bottom=GNuages+GExploitable)
    plt.bar(indexDate, GNuages, width=0.8,color='red', bottom=GExploitable)
    plt.bar(indexDate, GExploitable, width=0.8,color='lightgreen')
    
    

plt.xticks([0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334], mois)
plt.ylabel('Pourcentage de points TFE ')
plt.xlabel('Dates')
plt.legend(labels=['NoData','Neige','Nuages','Exploitable'],loc="upper right", facecolor="white")
plt.title("Etat des pixels selon les points de mesure (TFE)")
plt.xlim = (1,365)
plt.ylim = 1.0
    
plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    
plt.tight_layout()

        
plt.savefig('sortie/sortieT31TGK/graphiqueSnowT31TGK.png', dpi = 300)

plt.show()

####################
####################
### Tuile 31TGL ####
####################
####################


#Ouverture fichiers

repDonnees = r"../decoupageEmpriseZipSnow/sortie/sortieT31TGL"
repSortie = "sortie/sortieT31TGL"


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
    
#ouvrir les TFE

    TFEChemin = "TFE/tfe_bio_T31TGL_WGS84.shp"    
    TFE = gpd.read_file(TFEChemin) #ouverture du shp
     
    listeCoordonnees = []
     
    for j in range(len(TFE)):
        x = TFE.iloc[j].geometry.centroid.x #récupère les coordonnées d'un point
        y = TFE.iloc[j].geometry.centroid.y
     
        listeCoordonnees.append((x,y))
           
#ouverture masque avec GDAL

    masque = gdal.Open(repDonnees+'/'+listeRep[i]+'/'+masqueSnow[0])  
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

index = [ind for ind in range(365)]

mois = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 
         'Septembre', 'Octobre', 'Novembre', 'Décembre']


    
conversionTest = conversionJour('20170712')
    



plt.figure()

plt.rcParams['axes.facecolor']='black'


for d in range(len(listeDate)):
    
    indexDate = conversionJour(listeDate[d])
    
    GNoData = np.array(dicoPourcentage[listeDate[d]][0])
    GNeige = np.array(dicoPourcentage[listeDate[d]][1])
    GNuages = np.array(dicoPourcentage[listeDate[d]][2])
    GExploitable = np.array(dicoPourcentage[listeDate[d]][3])
    
   
    
    
    plt.bar(indexDate, GNoData, width=0.8,color='grey', bottom=GNeige+GNuages+GExploitable)
    plt.bar(indexDate, GNeige, width=0.8,color='#6082EF', bottom=GNuages+GExploitable)
    plt.bar(indexDate, GNuages, width=0.8,color='red', bottom=GExploitable)
    plt.bar(indexDate, GExploitable, width=0.8,color='lightgreen')
    
    

plt.xticks([0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334], mois)
plt.ylabel('Pourcentage de points TFE ')
plt.xlabel('Dates')
plt.legend(labels=['NoData','Neige','Nuages','Exploitable'],loc="upper right", facecolor="white")
plt.title("Etat des pixels selon les points de mesure (TFE)")
plt.xlim = (1,365)
plt.ylim = 1.0
    
plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    
plt.tight_layout()

        
plt.savefig('sortie/sortieT31TGL/graphiqueSnowT31TGL.png', dpi = 300)

plt.show()

####################
####################
### Tuile 32TLP ####
####################
####################


#Ouverture fichiers

repDonnees = r"../decoupageEmpriseZipSnow/sortie/sortieT32TLP"
repSortie = "sortie/sortieT32TLP"


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

#ouvrir les TFE

    TFEChemin = "TFE/tfe_bio_T32TLP_WGS84.shp"    
    TFE = gpd.read_file(TFEChemin) #ouverture du shp
     
    listeCoordonnees = []
     
    for j in range(len(TFE)):
        x = TFE.iloc[j].geometry.centroid.x #récupère les coordonnées d'un point
        y = TFE.iloc[j].geometry.centroid.y
     
        listeCoordonnees.append((x,y))
           
#ouverture masque avec GDAL

    masque = gdal.Open(repDonnees+'/'+listeRep[i]+'/'+masqueSnow[0]) 
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

index = [ind for ind in range(365)]

mois = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 
         'Septembre', 'Octobre', 'Novembre', 'Décembre']


    
conversionTest = conversionJour('20170712')
    



plt.figure()

plt.rcParams['axes.facecolor']='black'


for d in range(len(listeDate)):
    
    indexDate = conversionJour(listeDate[d])
    
    GNoData = np.array(dicoPourcentage[listeDate[d]][0])
    GNeige = np.array(dicoPourcentage[listeDate[d]][1])
    GNuages = np.array(dicoPourcentage[listeDate[d]][2])
    GExploitable = np.array(dicoPourcentage[listeDate[d]][3])
    
   
    
    
    plt.bar(indexDate, GNoData, width=0.8,color='grey', bottom=GNeige+GNuages+GExploitable)
    plt.bar(indexDate, GNeige, width=0.8,color='#6082EF', bottom=GNuages+GExploitable)
    plt.bar(indexDate, GNuages, width=0.8,color='red', bottom=GExploitable)
    plt.bar(indexDate, GExploitable, width=0.8,color='lightgreen')
    
    

plt.xticks([0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334], mois)
plt.ylabel('Pourcentage de points TFE ')
plt.xlabel('Dates')
plt.legend(labels=['NoData','Neige','Nuages','Exploitable'],loc="upper right", facecolor="white")
plt.title("Etat des pixels selon les points de mesure (TFE)")
plt.xlim = (1,365)
plt.ylim = 1.0
    
plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    
plt.tight_layout()

        
plt.savefig('sortie/sortieT32TLP/graphiqueSnowT32TLP.png', dpi = 300)

plt.show()

####################
####################
### Tuile 32TLQ ####
####################
####################


#Ouverture fichiers

repDonnees = r"../decoupageEmpriseZipSnow/sortie/sortieT32TLQ"
repSortie = "sortie/sortieT32TLQ"


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
       
#ouvrir les TFE

    TFEChemin = "TFE/tfe_bio_T32TLQ_WGS84.shp"    
    TFE = gpd.read_file(TFEChemin) #ouverture du shp
     
    listeCoordonnees = []
     
    for j in range(len(TFE)):
        x = TFE.iloc[j].geometry.centroid.x #récupère les coordonnées d'un point
        y = TFE.iloc[j].geometry.centroid.y
     
        listeCoordonnees.append((x,y))
           
#ouverture masque avec GDAL

    masque = gdal.Open(repDonnees+'/'+listeRep[i]+'/'+masqueSnow[0])  
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

index = [ind for ind in range(365)]

mois = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 
         'Septembre', 'Octobre', 'Novembre', 'Décembre']


    
conversionTest = conversionJour('20170712')
    



plt.figure()

plt.rcParams['axes.facecolor']='black'


for d in range(len(listeDate)):
    
    indexDate = conversionJour(listeDate[d])
    
    GNoData = np.array(dicoPourcentage[listeDate[d]][0])
    GNeige = np.array(dicoPourcentage[listeDate[d]][1])
    GNuages = np.array(dicoPourcentage[listeDate[d]][2])
    GExploitable = np.array(dicoPourcentage[listeDate[d]][3])
    
   
    
    
    plt.bar(indexDate, GNoData, width=0.8,color='grey', bottom=GNeige+GNuages+GExploitable)
    plt.bar(indexDate, GNeige, width=0.8,color='#6082EF', bottom=GNuages+GExploitable)
    plt.bar(indexDate, GNuages, width=0.8,color='red', bottom=GExploitable)
    plt.bar(indexDate, GExploitable, width=0.8,color='lightgreen')
    
    

plt.xticks([0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334], mois)
plt.ylabel('Pourcentage de points TFE ')
plt.xlabel('Dates')
plt.legend(labels=['NoData','Neige','Nuages','Exploitable'],loc="upper right", facecolor="white")
plt.title("Etat des pixels selon les points de mesure (TFE)")
plt.xlim = (1,365)
plt.ylim = 1.0
    
plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    
plt.tight_layout()

        
plt.savefig('sortie/sortieT32TLQ/graphiqueSnowT32TLQ.png', dpi = 300)

plt.show()

####################
####################
### Tuile 32TLR ####
####################
####################


#Ouverture fichiers

repDonnees = r"../decoupageEmpriseZipSnow/sortie/sortieT32TLR"
repSortie = "sortie/sortieT32TLR"


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
       
#ouvrir les TFE

    TFEChemin = "TFE/tfe_bio_T32TLR_WGS84.shp"    
    TFE = gpd.read_file(TFEChemin) #ouverture du shp
     
    listeCoordonnees = []
     
    for j in range(len(TFE)):
        x = TFE.iloc[j].geometry.centroid.x #récupère les coordonnées d'un point
        y = TFE.iloc[j].geometry.centroid.y
     
        listeCoordonnees.append((x,y))
           
#ouverture masque avec GDAL

    masque = gdal.Open(repDonnees+'/'+listeRep[i]+'/'+masqueSnow[0])  
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

index = [ind for ind in range(365)]

mois = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 
         'Septembre', 'Octobre', 'Novembre', 'Décembre']


    
conversionTest = conversionJour('20170712')
    



plt.figure()

plt.rcParams['axes.facecolor']='black'


for d in range(len(listeDate)):
    
    indexDate = conversionJour(listeDate[d])
    
    GNoData = np.array(dicoPourcentage[listeDate[d]][0])
    GNeige = np.array(dicoPourcentage[listeDate[d]][1])
    GNuages = np.array(dicoPourcentage[listeDate[d]][2])
    GExploitable = np.array(dicoPourcentage[listeDate[d]][3])
    
   
    
    
    plt.bar(indexDate, GNoData, width=0.8,color='grey', bottom=GNeige+GNuages+GExploitable)
    plt.bar(indexDate, GNeige, width=0.8,color='#6082EF', bottom=GNuages+GExploitable)
    plt.bar(indexDate, GNuages, width=0.8,color='red', bottom=GExploitable)
    plt.bar(indexDate, GExploitable, width=0.8,color='lightgreen')
    
    

plt.xticks([0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334], mois)
plt.ylabel('Pourcentage de points TFE ')
plt.xlabel('Dates')
plt.legend(labels=['NoData','Neige','Nuages','Exploitable'],loc="upper right", facecolor="white")
plt.title("Etat des pixels selon les points de mesure (TFE)")
plt.xlim = (1,365)
plt.ylim = 1.0
    
plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    
plt.tight_layout()

        
plt.savefig('sortie/sortieT32TLR/graphiqueSnowT32TLR.png', dpi = 300)

plt.show()