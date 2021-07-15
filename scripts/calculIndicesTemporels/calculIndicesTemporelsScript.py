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

listeIndices = ["ND_B2_B3", "SR_B2_B4", "BSI_B1_B2_B3","mSR_B1_B2_B3","indclass_NDVI","indclass_NDI45"]

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

#creation du tableau

legende = ["date","indices","bandes"]
for gid in range(len(TFE.gid)):
       legende.append(TFE.gid[gid])
    
Typo_Veget = ["/","/","/"]
for typoveget in range(len(TFE.Typo_Veget)):
    Typo_Veget.append(TFE.Typo_Veget[typoveget])
    
Id_sitesAS = ["/","/","/"]
for IdsitesAS in range(len(TFE.Id_sitesAS)):
    Id_sitesAS.append(TFE.Id_sitesAS[IdsitesAS])
    
Releve = ["/","/","/"]
for releve in range(len(TFE.Releve)):
    Releve.append(TFE.Releve[releve])
        
   
tab = pd.DataFrame(columns = legende)
tab.loc[1]=Id_sitesAS
tab.loc[2]=Releve
tab.loc[3]=Typo_Veget

index = 4


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
    
    listeBandes = B2+B3+B4+B5+B6+B7+B8+B8A+B11+B12
    
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
    
    
   
    
    
    for indice in range(len(listeIndices)):
        #nomIndice = listeIndices[0].split("_")
        nomIndice = listeIndices[indice].split("_")
        
        
        if len(nomIndice) == 3:
            with rasterio.open(repCourant+"/S2A_"+date+"_T31TFJ_"+nomIndice[1]+"_masque_scaling.tiff", "r") as src:
                ba = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(repCourant+"/S2A_"+date+"_T31TFJ_"+nomIndice[2]+"_masque_scaling.tiff", "r") as src:
                bb = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')



#ND
            if nomIndice[0] == "ND":
            
                ND =  np.divide((1.0*ba - bb), (ba + bb))
                ND[np.isinf(ND)] = np.nan
               
                ind = [date,'ND', "ND_"+nomIndice[1]+"_"+nomIndice[2]]
                       
                val = []
                
    
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(ND[row][col])
                            
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
            
#SD
            if nomIndice[0] == "SR":
              
                SR = np.divide(ba, bb)
                SR[np.isinf(SR)] = np.nan
                ind = [date,'SR', "SR_"+nomIndice[1]+"_"+nomIndice[2]]
                       
                val = []
                
    
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(SR[row][col])
                            
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                
 
# three bands vegetation indices (3BSI / mSR et 3BSI_Tian)
             
        if len(nomIndice) == 4:
            with rasterio.open(repCourant+"/S2A_"+date+"_T31TFJ_"+nomIndice[1]+"_masque_scaling.tiff", "r") as src:
                ba1 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(repCourant+"/S2A_"+date+"_T31TFJ_"+nomIndice[2]+"_masque_scaling.tiff", "r") as src:
                bb1 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(repCourant+"/S2A_"+date+"_T31TFJ_"+nomIndice[3]+"_masque_scaling.tiff", "r") as src:
                bc1 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')

            if nomIndice[0] == "BSI":
                
                BSI =  np.divide((1.0* ba1 - bc1), (bb1 + bc1))
                BSI[np.isinf(BSI)] = np.nan
               
                ind = ['BSI', "BSI_"+bande1+"_"+bande2+"_"+bande3]
            
                val = []
        
        
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
        
                    val.append(SR[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
        
        
                index = index+1
                
            if nomIndice[0] == "mSR":
        

                mSR =  np.divide((1.0* ba1 - bc1), (bb1 - bc1))
                mSR[np.isinf(mSR)] = np.nan
               
                ind = ['mSR', "mSR_"+bande1+"_"+bande2+"_"+bande3]
               
                val = []
        

                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(ND[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            index = index + 1
               
            if nomIndice[0] == "BSITian":

                BSI_Tian =  np.divide((1.0* ba1 - bb1 - bc1), (ba1 + bb1 + bc1))
                BSI_Tian[np.isinf(BSI_Tian)] = np.nan
               
                ind = ['BSITian', "BSITian_"+bande1+"_"+bande2+"_"+bande3]
               
                val = []
        
    
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(ND[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                    
            if nomIndice[0] == "CVI":

                CVI =  np.multiply((ba1 / bc1), (bb1 / bc1))
                CVI[np.isinf(CVI)] = np.nan
                
               
                ind = ['CVI', "CVI_"+bande1+"_"+bande2+"_"+bande3]
               
                val = []
        
    
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(ND[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                        