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

listeIndices = ["indclass_NDVI","indclass_GNDVI","indclass_NDI45","indclass_NDVIre","indclass_NDII","indclass_NREDI1","indclass_NREDI2","indclass_NREDI3","indclass_PSRI","indclass_MSI","indclass_IRECI","indclass_MTCI","indclass_MCARI"]

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
    
    nomSortieTab = f"{sat}_{tuile}_tableau.csv"
    
  
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
               
                ind = [date,'BSI', "BSI_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
            
                val = []
        
        
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
        
                    val.append(BSI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
        
        
                index = index+1
                
            if nomIndice[0] == "mSR":
        

                mSR =  np.divide((1.0* ba1 - bc1), (bb1 - bc1))
                mSR[np.isinf(mSR)] = np.nan
               
                ind = [date,'mSR', "mSR_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
               
                val = []
        

                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(mSR[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
                index = index + 1
               
            if nomIndice[0] == "BSITian":

                BSI_Tian =  np.divide((1.0* ba1 - bb1 - bc1), (ba1 + bb1 + bc1))
                BSI_Tian[np.isinf(BSI_Tian)] = np.nan
               
                ind = [date,'BSITian', "BSITian_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
               
                val = []
        
    
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(BSI_Tian[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                    
            if nomIndice[0] == "CVI":

                CVI =  np.multiply((ba1 / bc1), (bb1 / bc1))
                CVI[np.isinf(CVI)] = np.nan
                
               
                ind = [date,'CVI', "CVI_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
               
                val = []
        
    
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(CVI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                

                
###Création des indices usuels:
    
        if len(nomIndice) == 2:    

            with rasterio.open(repCourant+"/"+listeBandes[0], "r") as src:
                bandeB2 = src.read(1)
                profile = src.profile
                profile.update(
                     dtype=rasterio.float64,
                     count=1,
                     compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[1], "r") as src:
                bandeB3 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[2], "r") as src:
                bandeB4 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[3], "r") as src:
                bandeB5 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[4], "r") as src:
                bandeB6 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[5], "r") as src:
                bandeB7 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[6], "r") as src:
                bandeB8 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[7], "r") as src:
                bandeB8a = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[8], "r") as src:
                bandeB11 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')


            if nomIndice[1] == "NDVI":
   
                NDVI = np.divide((1.0*bandeB8 - bandeB4), (bandeB8 + bandeB4))
                NDVI[np.isinf(NDVI)]=np.nan
                
                ind = [date,'indclass', "indclass_NDVI"]
                 
                val = []
                 
                
                for point in listeCoordonnees:
                     col = int((point[0] - xOrigin) / pixelWidth)
                     row = int((yOrigin - point[1] ) / pixelHeight)
                     val.append(NDVI[row][col])
                 
                concat = ind + val
                 
                tab.loc[index]=concat


                index = index+1
                
            if nomIndice[1] == "GNDVI":


                GNDVI = np.divide((1.0*bandeB8 - bandeB3), (bandeB8 + bandeB3))
                GNDVI[np.isinf(GNDVI)]=np.nan
                
                ind = [date,'indclass', "indclass_GNDVI"]
                
                val = []
                
                
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(GNDVI[row][col])
                 
                concat = ind + val
                 
                tab.loc[index]=concat
            
                index = index+1

            if nomIndice[1] == "NDVIre":
                NDVIre = np.divide((1.0*bandeB8a - bandeB4), (bandeB8a + bandeB4))
                NDVIre[np.isinf(NDVIre)]=np.nan
               
                ind = [date,'indclass', "indclass_NDVIre"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(NDVIre[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1

            if nomIndice[1] == "NDVI":
                NDI45 = np.divide((1.0*bandeB5 - bandeB4), (bandeB5 + bandeB4))
                NDI45[np.isinf(NDI45)]=np.nan
               
                ind = [date,'indclass', "indclass_NDI45"]
                
                val = []
                
                
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(NDI45[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat

                index = index+1

            if nomIndice[1] == "NDII":
                NDII = np.divide((1.0*bandeB8 - bandeB11), (bandeB8 + bandeB11))
                NDII[np.isinf(NDII)]=np.nan
                
                ind = [date,'indclass', "indclass_NDII"]
                
                val = []
                
                
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(NDII[row][col])
                 
                concat = ind + val
                     
                tab.loc[index]=concat
            
            
                index = index+1

            if nomIndice[1] == "NDREDI1":
                NREDI1 = np.divide((1.0*bandeB6 - bandeB5), (bandeB6 + bandeB5))
                NREDI1[np.isinf(NREDI1)]=np.nan
                 
                ind = [date,'indclass', "indclass_NREDI1"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(NREDI1[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "NDREDI2":

                NREDI2 = np.divide((1.0*bandeB7 - bandeB5), (bandeB7 + bandeB5))
                NREDI2[np.isinf(NREDI2)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_NREDI2"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(NREDI2[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1



            if nomIndice[1] == "NDREDI3":

                NREDI3 = np.divide((1.0*bandeB7 - bandeB6), (bandeB7 + bandeB6))
                NREDI3[np.isinf(NREDI3)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_NREDI3"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(NREDI3[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1

 

            if nomIndice[1] == "PSRI":

                PSRI = np.divide((1.0*bandeB4 - bandeB3), (bandeB5))
                PSRI[np.isinf(PSRI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_PSRI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(PSRI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1

            if nomIndice[1] == "MSI":
                MSI = np.divide((1.0*bandeB11), (bandeB8))
                MSI[np.isinf(MSI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_MSI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(MSI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "IRECI":
                IRECI = np.divide((1.0*bandeB7 - bandeB4), (np.divide(1.0*bandeB5 , bandeB6)))
                IRECI[np.isinf(IRECI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_IRECI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(IRECI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "MTCI":
                MTCI = np.divide((1.0*bandeB8 - bandeB5), (bandeB5 - bandeB4))
                MTCI[np.isinf(MTCI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_MTCI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(MTCI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "MCARI":
                MCARI = np.multiply(((bandeB5 - bandeB4) - (0.2*(bandeB5 - bandeB3))), (bandeB5 - bandeB4))
                MCARI[np.isinf(MCARI)]=np.nan
               
                 
                ind = [date,'indclass', "indclass_MCARI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(MCARI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1
     

   
tab[tab == -0.0] = np.nan
tab[tab == 1.0] = np.nan
tab.to_csv(os.path.join(repSortie,nomSortieTab), index=False)
    

####################
####################
### Tuile 31TFK ####
####################
####################

#Lister les indices souhaités

listeIndices = ["indclass_NDVI","indclass_GNDVI","indclass_NDI45","indclass_NDVIre","indclass_NDII","indclass_NREDI1","indclass_NREDI2","indclass_NREDI3","indclass_PSRI","indclass_MSI","indclass_IRECI","indclass_MTCI","indclass_MCARI"]

#ouvrir les TFE

TFEChemin = "TFE/tfe_bio_T31TFK_WGS84.shp"    
TFE = gpd.read_file(TFEChemin) #ouverture du shp
   
listeCoordonnees = []
     
for j in range(len(TFE)):
    x = TFE.iloc[j].geometry.centroid.x #récupère les coordonnées d'un point
    y = TFE.iloc[j].geometry.centroid.y
     
    listeCoordonnees.append((x,y))
        
         

#ouverture des bandes
  
repDonnees = r"../applicationMasque/sortie/sortieT31TFK"
repSortie = "sortie/sortieT31TFK"

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
    
    nomSortieTab = f"{sat}_{tuile}_tableau.csv"
    
  
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
            with rasterio.open(repCourant+"/S2A_"+date+"_T31TFK_"+nomIndice[1]+"_masque_scaling.tiff", "r") as src:
                ba = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(repCourant+"/S2A_"+date+"_T31TFK_"+nomIndice[2]+"_masque_scaling.tiff", "r") as src:
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
            with rasterio.open(repCourant+"/S2A_"+date+"_T31TFK_"+nomIndice[1]+"_masque_scaling.tiff", "r") as src:
                ba1 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(repCourant+"/S2A_"+date+"_T31TFK_"+nomIndice[2]+"_masque_scaling.tiff", "r") as src:
                bb1 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(repCourant+"/S2A_"+date+"_T31TFK_"+nomIndice[3]+"_masque_scaling.tiff", "r") as src:
                bc1 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')

            if nomIndice[0] == "BSI":
                
                BSI =  np.divide((1.0* ba1 - bc1), (bb1 + bc1))
                BSI[np.isinf(BSI)] = np.nan
               
                ind = [date,'BSI', "BSI_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
            
                val = []
        
        
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
        
                    val.append(BSI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
        
        
                index = index+1
                
            if nomIndice[0] == "mSR":
        

                mSR =  np.divide((1.0* ba1 - bc1), (bb1 - bc1))
                mSR[np.isinf(mSR)] = np.nan
               
                ind = [date,'mSR', "mSR_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
               
                val = []
        

                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(mSR[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
                index = index + 1
               
            if nomIndice[0] == "BSITian":

                BSI_Tian =  np.divide((1.0* ba1 - bb1 - bc1), (ba1 + bb1 + bc1))
                BSI_Tian[np.isinf(BSI_Tian)] = np.nan
               
                ind = [date,'BSITian', "BSITian_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
               
                val = []
        
    
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(BSI_Tian[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                    
            if nomIndice[0] == "CVI":

                CVI =  np.multiply((ba1 / bc1), (bb1 / bc1))
                CVI[np.isinf(CVI)] = np.nan
                
               
                ind = [date,'CVI', "CVI_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
               
                val = []
        
    
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(CVI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                

                
###Création des indices usuels:
    
        if len(nomIndice) == 2:    

            with rasterio.open(repCourant+"/"+listeBandes[0], "r") as src:
                bandeB2 = src.read(1)
                profile = src.profile
                profile.update(
                     dtype=rasterio.float64,
                     count=1,
                     compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[1], "r") as src:
                bandeB3 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[2], "r") as src:
                bandeB4 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[3], "r") as src:
                bandeB5 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[4], "r") as src:
                bandeB6 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[5], "r") as src:
                bandeB7 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[6], "r") as src:
                bandeB8 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[7], "r") as src:
                bandeB8a = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[8], "r") as src:
                bandeB11 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')


            if nomIndice[1] == "NDVI":
   
                NDVI = np.divide((1.0*bandeB8 - bandeB4), (bandeB8 + bandeB4))
                NDVI[np.isinf(NDVI)]=np.nan
                
                ind = [date,'indclass', "indclass_NDVI"]
                 
                val = []
                 
                
                for point in listeCoordonnees:
                     col = int((point[0] - xOrigin) / pixelWidth)
                     row = int((yOrigin - point[1] ) / pixelHeight)
                     val.append(NDVI[row][col])
                 
                concat = ind + val
                 
                tab.loc[index]=concat


                index = index+1
                
            if nomIndice[1] == "GNDVI":


                GNDVI = np.divide((1.0*bandeB8 - bandeB3), (bandeB8 + bandeB3))
                GNDVI[np.isinf(GNDVI)]=np.nan
                
                ind = [date,'indclass', "indclass_GNDVI"]
                
                val = []
                
                
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(GNDVI[row][col])
                 
                concat = ind + val
                 
                tab.loc[index]=concat
            
                index = index+1

            if nomIndice[1] == "NDVIre":
                NDVIre = np.divide((1.0*bandeB8a - bandeB4), (bandeB8a + bandeB4))
                NDVIre[np.isinf(NDVIre)]=np.nan
               
                ind = [date,'indclass', "indclass_NDVIre"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(NDVIre[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1

            if nomIndice[1] == "NDVI":
                NDI45 = np.divide((1.0*bandeB5 - bandeB4), (bandeB5 + bandeB4))
                NDI45[np.isinf(NDI45)]=np.nan
               
                ind = [date,'indclass', "indclass_NDI45"]
                
                val = []
                
                
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(NDI45[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat

                index = index+1

            if nomIndice[1] == "NDII":
                NDII = np.divide((1.0*bandeB8 - bandeB11), (bandeB8 + bandeB11))
                NDII[np.isinf(NDII)]=np.nan
                
                ind = [date,'indclass', "indclass_NDII"]
                
                val = []
                
                
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(NDII[row][col])
                 
                concat = ind + val
                     
                tab.loc[index]=concat
            
            
                index = index+1

            if nomIndice[1] == "NDREDI1":
                NREDI1 = np.divide((1.0*bandeB6 - bandeB5), (bandeB6 + bandeB5))
                NREDI1[np.isinf(NREDI1)]=np.nan
                 
                ind = [date,'indclass', "indclass_NREDI1"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(NREDI1[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "NDREDI2":

                NREDI2 = np.divide((1.0*bandeB7 - bandeB5), (bandeB7 + bandeB5))
                NREDI2[np.isinf(NREDI2)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_NREDI2"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(NREDI2[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1



            if nomIndice[1] == "NDREDI3":

                NREDI3 = np.divide((1.0*bandeB7 - bandeB6), (bandeB7 + bandeB6))
                NREDI3[np.isinf(NREDI3)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_NREDI3"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(NREDI3[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1

 

            if nomIndice[1] == "PSRI":

                PSRI = np.divide((1.0*bandeB4 - bandeB3), (bandeB5))
                PSRI[np.isinf(PSRI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_PSRI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(PSRI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1

            if nomIndice[1] == "MSI":
                MSI = np.divide((1.0*bandeB11), (bandeB8))
                MSI[np.isinf(MSI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_MSI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(MSI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "IRECI":
                IRECI = np.divide((1.0*bandeB7 - bandeB4), (np.divide(1.0*bandeB5 , bandeB6)))
                IRECI[np.isinf(IRECI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_IRECI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(IRECI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "MTCI":
                MTCI = np.divide((1.0*bandeB8 - bandeB5), (bandeB5 - bandeB4))
                MTCI[np.isinf(MTCI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_MTCI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(MTCI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "MCARI":
                MCARI = np.multiply(((bandeB5 - bandeB4) - (0.2*(bandeB5 - bandeB3))), (bandeB5 - bandeB4))
                MCARI[np.isinf(MCARI)]=np.nan
               
                 
                ind = [date,'indclass', "indclass_MCARI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(MCARI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1
     

   
tab[tab == -0.0] = np.nan
tab[tab == 1.0] = np.nan
tab.to_csv(os.path.join(repSortie,nomSortieTab), index=False)
    



####################
####################
### Tuile 31TGK ####
####################
####################

#Lister les indices souhaités

listeIndices = ["indclass_NDVI","indclass_GNDVI","indclass_NDI45","indclass_NDVIre","indclass_NDII","indclass_NREDI1","indclass_NREDI2","indclass_NREDI3","indclass_PSRI","indclass_MSI","indclass_IRECI","indclass_MTCI","indclass_MCARI"]

#ouvrir les TFE

TFEChemin = "TFE/tfe_bio_T31TGK_WGS84.shp"    
TFE = gpd.read_file(TFEChemin) #ouverture du shp
   
listeCoordonnees = []
     
for j in range(len(TFE)):
    x = TFE.iloc[j].geometry.centroid.x #récupère les coordonnées d'un point
    y = TFE.iloc[j].geometry.centroid.y
     
    listeCoordonnees.append((x,y))
        
         

#ouverture des bandes
  
repDonnees = r"../applicationMasque/sortie/sortieT31TGK"
repSortie = "sortie/sortieT31TGK"

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
    
    nomSortieTab = f"{sat}_{tuile}_tableau.csv"
    
  
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
            with rasterio.open(repCourant+"/S2A_"+date+"_T31TGK_"+nomIndice[1]+"_masque_scaling.tiff", "r") as src:
                ba = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(repCourant+"/S2A_"+date+"_T31TGK_"+nomIndice[2]+"_masque_scaling.tiff", "r") as src:
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
            with rasterio.open(repCourant+"/S2A_"+date+"_T31TGK_"+nomIndice[1]+"_masque_scaling.tiff", "r") as src:
                ba1 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(repCourant+"/S2A_"+date+"_T31TGK_"+nomIndice[2]+"_masque_scaling.tiff", "r") as src:
                bb1 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(repCourant+"/S2A_"+date+"_T31TGK_"+nomIndice[3]+"_masque_scaling.tiff", "r") as src:
                bc1 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')

            if nomIndice[0] == "BSI":
                
                BSI =  np.divide((1.0* ba1 - bc1), (bb1 + bc1))
                BSI[np.isinf(BSI)] = np.nan
               
                ind = [date,'BSI', "BSI_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
            
                val = []
        
        
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
        
                    val.append(BSI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
        
        
                index = index+1
                
            if nomIndice[0] == "mSR":
        

                mSR =  np.divide((1.0* ba1 - bc1), (bb1 - bc1))
                mSR[np.isinf(mSR)] = np.nan
               
                ind = [date,'mSR', "mSR_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
               
                val = []
        

                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(mSR[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
                index = index + 1
               
            if nomIndice[0] == "BSITian":

                BSI_Tian =  np.divide((1.0* ba1 - bb1 - bc1), (ba1 + bb1 + bc1))
                BSI_Tian[np.isinf(BSI_Tian)] = np.nan
               
                ind = [date,'BSITian', "BSITian_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
               
                val = []
        
    
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(BSI_Tian[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                    
            if nomIndice[0] == "CVI":

                CVI =  np.multiply((ba1 / bc1), (bb1 / bc1))
                CVI[np.isinf(CVI)] = np.nan
                
               
                ind = [date,'CVI', "CVI_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
               
                val = []
        
    
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(CVI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                

                
###Création des indices usuels:
    
        if len(nomIndice) == 2:    

            with rasterio.open(repCourant+"/"+listeBandes[0], "r") as src:
                bandeB2 = src.read(1)
                profile = src.profile
                profile.update(
                     dtype=rasterio.float64,
                     count=1,
                     compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[1], "r") as src:
                bandeB3 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[2], "r") as src:
                bandeB4 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[3], "r") as src:
                bandeB5 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[4], "r") as src:
                bandeB6 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[5], "r") as src:
                bandeB7 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[6], "r") as src:
                bandeB8 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[7], "r") as src:
                bandeB8a = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[8], "r") as src:
                bandeB11 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')


            if nomIndice[1] == "NDVI":
   
                NDVI = np.divide((1.0*bandeB8 - bandeB4), (bandeB8 + bandeB4))
                NDVI[np.isinf(NDVI)]=np.nan
                
                ind = [date,'indclass', "indclass_NDVI"]
                 
                val = []
                 
                
                for point in listeCoordonnees:
                     col = int((point[0] - xOrigin) / pixelWidth)
                     row = int((yOrigin - point[1] ) / pixelHeight)
                     val.append(NDVI[row][col])
                 
                concat = ind + val
                 
                tab.loc[index]=concat


                index = index+1
                
            if nomIndice[1] == "GNDVI":


                GNDVI = np.divide((1.0*bandeB8 - bandeB3), (bandeB8 + bandeB3))
                GNDVI[np.isinf(GNDVI)]=np.nan
                
                ind = [date,'indclass', "indclass_GNDVI"]
                
                val = []
                
                
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(GNDVI[row][col])
                 
                concat = ind + val
                 
                tab.loc[index]=concat
            
                index = index+1

            if nomIndice[1] == "NDVIre":
                NDVIre = np.divide((1.0*bandeB8a - bandeB4), (bandeB8a + bandeB4))
                NDVIre[np.isinf(NDVIre)]=np.nan
               
                ind = [date,'indclass', "indclass_NDVIre"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(NDVIre[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1

            if nomIndice[1] == "NDVI":
                NDI45 = np.divide((1.0*bandeB5 - bandeB4), (bandeB5 + bandeB4))
                NDI45[np.isinf(NDI45)]=np.nan
               
                ind = [date,'indclass', "indclass_NDI45"]
                
                val = []
                
                
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(NDI45[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat

                index = index+1

            if nomIndice[1] == "NDII":
                NDII = np.divide((1.0*bandeB8 - bandeB11), (bandeB8 + bandeB11))
                NDII[np.isinf(NDII)]=np.nan
                
                ind = [date,'indclass', "indclass_NDII"]
                
                val = []
                
                
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(NDII[row][col])
                 
                concat = ind + val
                     
                tab.loc[index]=concat
            
            
                index = index+1

            if nomIndice[1] == "NDREDI1":
                NREDI1 = np.divide((1.0*bandeB6 - bandeB5), (bandeB6 + bandeB5))
                NREDI1[np.isinf(NREDI1)]=np.nan
                 
                ind = [date,'indclass', "indclass_NREDI1"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(NREDI1[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "NDREDI2":

                NREDI2 = np.divide((1.0*bandeB7 - bandeB5), (bandeB7 + bandeB5))
                NREDI2[np.isinf(NREDI2)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_NREDI2"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(NREDI2[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1



            if nomIndice[1] == "NDREDI3":

                NREDI3 = np.divide((1.0*bandeB7 - bandeB6), (bandeB7 + bandeB6))
                NREDI3[np.isinf(NREDI3)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_NREDI3"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(NREDI3[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1

 

            if nomIndice[1] == "PSRI":

                PSRI = np.divide((1.0*bandeB4 - bandeB3), (bandeB5))
                PSRI[np.isinf(PSRI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_PSRI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(PSRI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1

            if nomIndice[1] == "MSI":
                MSI = np.divide((1.0*bandeB11), (bandeB8))
                MSI[np.isinf(MSI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_MSI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(MSI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "IRECI":
                IRECI = np.divide((1.0*bandeB7 - bandeB4), (np.divide(1.0*bandeB5 , bandeB6)))
                IRECI[np.isinf(IRECI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_IRECI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(IRECI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "MTCI":
                MTCI = np.divide((1.0*bandeB8 - bandeB5), (bandeB5 - bandeB4))
                MTCI[np.isinf(MTCI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_MTCI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(MTCI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "MCARI":
                MCARI = np.multiply(((bandeB5 - bandeB4) - (0.2*(bandeB5 - bandeB3))), (bandeB5 - bandeB4))
                MCARI[np.isinf(MCARI)]=np.nan
               
                 
                ind = [date,'indclass', "indclass_MCARI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(MCARI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1
     

   
tab[tab == -0.0] = np.nan
tab[tab == 1.0] = np.nan
tab.to_csv(os.path.join(repSortie,nomSortieTab), index=False)
    


####################
####################
### Tuile 31TGL ####
####################
####################

#Lister les indices souhaités

listeIndices = ["indclass_NDVI","indclass_GNDVI","indclass_NDI45","indclass_NDVIre","indclass_NDII","indclass_NREDI1","indclass_NREDI2","indclass_NREDI3","indclass_PSRI","indclass_MSI","indclass_IRECI","indclass_MTCI","indclass_MCARI"]

#ouvrir les TFE

TFEChemin = "TFE/tfe_bio_T31TGL_WGS84.shp"    
TFE = gpd.read_file(TFEChemin) #ouverture du shp
   
listeCoordonnees = []
     
for j in range(len(TFE)):
    x = TFE.iloc[j].geometry.centroid.x #récupère les coordonnées d'un point
    y = TFE.iloc[j].geometry.centroid.y
     
    listeCoordonnees.append((x,y))
        
         

#ouverture des bandes
  
repDonnees = r"../applicationMasque/sortie/sortieT31TGL"
repSortie = "sortie/sortieT31TGL"

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
    
    nomSortieTab = f"{sat}_{tuile}_tableau.csv"
    
  
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
            with rasterio.open(repCourant+"/S2A_"+date+"_T31TGL_"+nomIndice[1]+"_masque_scaling.tiff", "r") as src:
                ba = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(repCourant+"/S2A_"+date+"_T31TGL_"+nomIndice[2]+"_masque_scaling.tiff", "r") as src:
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
            with rasterio.open(repCourant+"/S2A_"+date+"_T31TGL_"+nomIndice[1]+"_masque_scaling.tiff", "r") as src:
                ba1 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(repCourant+"/S2A_"+date+"_T31TGL_"+nomIndice[2]+"_masque_scaling.tiff", "r") as src:
                bb1 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(repCourant+"/S2A_"+date+"_T31TGL_"+nomIndice[3]+"_masque_scaling.tiff", "r") as src:
                bc1 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')

            if nomIndice[0] == "BSI":
                
                BSI =  np.divide((1.0* ba1 - bc1), (bb1 + bc1))
                BSI[np.isinf(BSI)] = np.nan
               
                ind = [date,'BSI', "BSI_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
            
                val = []
        
        
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
        
                    val.append(BSI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
        
        
                index = index+1
                
            if nomIndice[0] == "mSR":
        

                mSR =  np.divide((1.0* ba1 - bc1), (bb1 - bc1))
                mSR[np.isinf(mSR)] = np.nan
               
                ind = [date,'mSR', "mSR_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
               
                val = []
        

                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(mSR[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
                index = index + 1
               
            if nomIndice[0] == "BSITian":

                BSI_Tian =  np.divide((1.0* ba1 - bb1 - bc1), (ba1 + bb1 + bc1))
                BSI_Tian[np.isinf(BSI_Tian)] = np.nan
               
                ind = [date,'BSITian', "BSITian_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
               
                val = []
        
    
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(BSI_Tian[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                    
            if nomIndice[0] == "CVI":

                CVI =  np.multiply((ba1 / bc1), (bb1 / bc1))
                CVI[np.isinf(CVI)] = np.nan
                
               
                ind = [date,'CVI', "CVI_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
               
                val = []
        
    
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(CVI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                

                
###Création des indices usuels:
    
        if len(nomIndice) == 2:    

            with rasterio.open(repCourant+"/"+listeBandes[0], "r") as src:
                bandeB2 = src.read(1)
                profile = src.profile
                profile.update(
                     dtype=rasterio.float64,
                     count=1,
                     compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[1], "r") as src:
                bandeB3 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[2], "r") as src:
                bandeB4 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[3], "r") as src:
                bandeB5 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[4], "r") as src:
                bandeB6 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[5], "r") as src:
                bandeB7 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[6], "r") as src:
                bandeB8 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[7], "r") as src:
                bandeB8a = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[8], "r") as src:
                bandeB11 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')


            if nomIndice[1] == "NDVI":
   
                NDVI = np.divide((1.0*bandeB8 - bandeB4), (bandeB8 + bandeB4))
                NDVI[np.isinf(NDVI)]=np.nan
                
                ind = [date,'indclass', "indclass_NDVI"]
                 
                val = []
                 
                
                for point in listeCoordonnees:
                     col = int((point[0] - xOrigin) / pixelWidth)
                     row = int((yOrigin - point[1] ) / pixelHeight)
                     val.append(NDVI[row][col])
                 
                concat = ind + val
                 
                tab.loc[index]=concat


                index = index+1
                
            if nomIndice[1] == "GNDVI":


                GNDVI = np.divide((1.0*bandeB8 - bandeB3), (bandeB8 + bandeB3))
                GNDVI[np.isinf(GNDVI)]=np.nan
                
                ind = [date,'indclass', "indclass_GNDVI"]
                
                val = []
                
                
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(GNDVI[row][col])
                 
                concat = ind + val
                 
                tab.loc[index]=concat
            
                index = index+1

            if nomIndice[1] == "NDVIre":
                NDVIre = np.divide((1.0*bandeB8a - bandeB4), (bandeB8a + bandeB4))
                NDVIre[np.isinf(NDVIre)]=np.nan
               
                ind = [date,'indclass', "indclass_NDVIre"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(NDVIre[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1

            if nomIndice[1] == "NDVI":
                NDI45 = np.divide((1.0*bandeB5 - bandeB4), (bandeB5 + bandeB4))
                NDI45[np.isinf(NDI45)]=np.nan
               
                ind = [date,'indclass', "indclass_NDI45"]
                
                val = []
                
                
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(NDI45[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat

                index = index+1

            if nomIndice[1] == "NDII":
                NDII = np.divide((1.0*bandeB8 - bandeB11), (bandeB8 + bandeB11))
                NDII[np.isinf(NDII)]=np.nan
                
                ind = [date,'indclass', "indclass_NDII"]
                
                val = []
                
                
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(NDII[row][col])
                 
                concat = ind + val
                     
                tab.loc[index]=concat
            
            
                index = index+1

            if nomIndice[1] == "NDREDI1":
                NREDI1 = np.divide((1.0*bandeB6 - bandeB5), (bandeB6 + bandeB5))
                NREDI1[np.isinf(NREDI1)]=np.nan
                 
                ind = [date,'indclass', "indclass_NREDI1"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(NREDI1[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "NDREDI2":

                NREDI2 = np.divide((1.0*bandeB7 - bandeB5), (bandeB7 + bandeB5))
                NREDI2[np.isinf(NREDI2)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_NREDI2"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(NREDI2[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1



            if nomIndice[1] == "NDREDI3":

                NREDI3 = np.divide((1.0*bandeB7 - bandeB6), (bandeB7 + bandeB6))
                NREDI3[np.isinf(NREDI3)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_NREDI3"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(NREDI3[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1

 

            if nomIndice[1] == "PSRI":

                PSRI = np.divide((1.0*bandeB4 - bandeB3), (bandeB5))
                PSRI[np.isinf(PSRI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_PSRI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(PSRI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1

            if nomIndice[1] == "MSI":
                MSI = np.divide((1.0*bandeB11), (bandeB8))
                MSI[np.isinf(MSI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_MSI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(MSI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "IRECI":
                IRECI = np.divide((1.0*bandeB7 - bandeB4), (np.divide(1.0*bandeB5 , bandeB6)))
                IRECI[np.isinf(IRECI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_IRECI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(IRECI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "MTCI":
                MTCI = np.divide((1.0*bandeB8 - bandeB5), (bandeB5 - bandeB4))
                MTCI[np.isinf(MTCI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_MTCI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(MTCI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "MCARI":
                MCARI = np.multiply(((bandeB5 - bandeB4) - (0.2*(bandeB5 - bandeB3))), (bandeB5 - bandeB4))
                MCARI[np.isinf(MCARI)]=np.nan
               
                 
                ind = [date,'indclass', "indclass_MCARI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(MCARI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1
     

   
tab[tab == -0.0] = np.nan
tab[tab == 1.0] = np.nan
tab.to_csv(os.path.join(repSortie,nomSortieTab), index=False)
    


####################
####################
### Tuile 32TLP ####
####################
####################

#Lister les indices souhaités

listeIndices = ["indclass_NDVI","indclass_GNDVI","indclass_NDI45","indclass_NDVIre","indclass_NDII","indclass_NREDI1","indclass_NREDI2","indclass_NREDI3","indclass_PSRI","indclass_MSI","indclass_IRECI","indclass_MTCI","indclass_MCARI"]

#ouvrir les TFE

TFEChemin = "TFE/tfe_bio_T32TLP_WGS84.shp"    
TFE = gpd.read_file(TFEChemin) #ouverture du shp
   
listeCoordonnees = []
     
for j in range(len(TFE)):
    x = TFE.iloc[j].geometry.centroid.x #récupère les coordonnées d'un point
    y = TFE.iloc[j].geometry.centroid.y
     
    listeCoordonnees.append((x,y))
        
         

#ouverture des bandes
  
repDonnees = r"../applicationMasque/sortie/sortieT32TLP"
repSortie = "sortie/sortieT32TLP"

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
    
    nomSortieTab = f"{sat}_{tuile}_tableau.csv"
    
  
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
            with rasterio.open(repCourant+"/S2A_"+date+"_T32TLP_"+nomIndice[1]+"_masque_scaling.tiff", "r") as src:
                ba = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(repCourant+"/S2A_"+date+"_T32TLP_"+nomIndice[2]+"_masque_scaling.tiff", "r") as src:
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
            with rasterio.open(repCourant+"/S2A_"+date+"_T32TLP_"+nomIndice[1]+"_masque_scaling.tiff", "r") as src:
                ba1 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(repCourant+"/S2A_"+date+"_T32TLP_"+nomIndice[2]+"_masque_scaling.tiff", "r") as src:
                bb1 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(repCourant+"/S2A_"+date+"_T32TLP_"+nomIndice[3]+"_masque_scaling.tiff", "r") as src:
                bc1 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')

            if nomIndice[0] == "BSI":
                
                BSI =  np.divide((1.0* ba1 - bc1), (bb1 + bc1))
                BSI[np.isinf(BSI)] = np.nan
               
                ind = [date,'BSI', "BSI_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
            
                val = []
        
        
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
        
                    val.append(BSI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
        
        
                index = index+1
                
            if nomIndice[0] == "mSR":
        

                mSR =  np.divide((1.0* ba1 - bc1), (bb1 - bc1))
                mSR[np.isinf(mSR)] = np.nan
               
                ind = [date,'mSR', "mSR_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
               
                val = []
        

                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(mSR[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
                index = index + 1
               
            if nomIndice[0] == "BSITian":

                BSI_Tian =  np.divide((1.0* ba1 - bb1 - bc1), (ba1 + bb1 + bc1))
                BSI_Tian[np.isinf(BSI_Tian)] = np.nan
               
                ind = [date,'BSITian', "BSITian_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
               
                val = []
        
    
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(BSI_Tian[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                    
            if nomIndice[0] == "CVI":

                CVI =  np.multiply((ba1 / bc1), (bb1 / bc1))
                CVI[np.isinf(CVI)] = np.nan
                
               
                ind = [date,'CVI', "CVI_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
               
                val = []
        
    
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(CVI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                

                
###Création des indices usuels:
    
        if len(nomIndice) == 2:    

            with rasterio.open(repCourant+"/"+listeBandes[0], "r") as src:
                bandeB2 = src.read(1)
                profile = src.profile
                profile.update(
                     dtype=rasterio.float64,
                     count=1,
                     compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[1], "r") as src:
                bandeB3 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[2], "r") as src:
                bandeB4 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[3], "r") as src:
                bandeB5 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[4], "r") as src:
                bandeB6 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[5], "r") as src:
                bandeB7 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[6], "r") as src:
                bandeB8 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[7], "r") as src:
                bandeB8a = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[8], "r") as src:
                bandeB11 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')


            if nomIndice[1] == "NDVI":
   
                NDVI = np.divide((1.0*bandeB8 - bandeB4), (bandeB8 + bandeB4))
                NDVI[np.isinf(NDVI)]=np.nan
                
                ind = [date,'indclass', "indclass_NDVI"]
                 
                val = []
                 
                
                for point in listeCoordonnees:
                     col = int((point[0] - xOrigin) / pixelWidth)
                     row = int((yOrigin - point[1] ) / pixelHeight)
                     val.append(NDVI[row][col])
                 
                concat = ind + val
                 
                tab.loc[index]=concat


                index = index+1
                
            if nomIndice[1] == "GNDVI":


                GNDVI = np.divide((1.0*bandeB8 - bandeB3), (bandeB8 + bandeB3))
                GNDVI[np.isinf(GNDVI)]=np.nan
                
                ind = [date,'indclass', "indclass_GNDVI"]
                
                val = []
                
                
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(GNDVI[row][col])
                 
                concat = ind + val
                 
                tab.loc[index]=concat
            
                index = index+1

            if nomIndice[1] == "NDVIre":
                NDVIre = np.divide((1.0*bandeB8a - bandeB4), (bandeB8a + bandeB4))
                NDVIre[np.isinf(NDVIre)]=np.nan
               
                ind = [date,'indclass', "indclass_NDVIre"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(NDVIre[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1

            if nomIndice[1] == "NDVI":
                NDI45 = np.divide((1.0*bandeB5 - bandeB4), (bandeB5 + bandeB4))
                NDI45[np.isinf(NDI45)]=np.nan
               
                ind = [date,'indclass', "indclass_NDI45"]
                
                val = []
                
                
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(NDI45[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat

                index = index+1

            if nomIndice[1] == "NDII":
                NDII = np.divide((1.0*bandeB8 - bandeB11), (bandeB8 + bandeB11))
                NDII[np.isinf(NDII)]=np.nan
                
                ind = [date,'indclass', "indclass_NDII"]
                
                val = []
                
                
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(NDII[row][col])
                 
                concat = ind + val
                     
                tab.loc[index]=concat
            
            
                index = index+1

            if nomIndice[1] == "NDREDI1":
                NREDI1 = np.divide((1.0*bandeB6 - bandeB5), (bandeB6 + bandeB5))
                NREDI1[np.isinf(NREDI1)]=np.nan
                 
                ind = [date,'indclass', "indclass_NREDI1"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(NREDI1[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "NDREDI2":

                NREDI2 = np.divide((1.0*bandeB7 - bandeB5), (bandeB7 + bandeB5))
                NREDI2[np.isinf(NREDI2)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_NREDI2"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(NREDI2[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1



            if nomIndice[1] == "NDREDI3":

                NREDI3 = np.divide((1.0*bandeB7 - bandeB6), (bandeB7 + bandeB6))
                NREDI3[np.isinf(NREDI3)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_NREDI3"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(NREDI3[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1

 

            if nomIndice[1] == "PSRI":

                PSRI = np.divide((1.0*bandeB4 - bandeB3), (bandeB5))
                PSRI[np.isinf(PSRI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_PSRI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(PSRI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1

            if nomIndice[1] == "MSI":
                MSI = np.divide((1.0*bandeB11), (bandeB8))
                MSI[np.isinf(MSI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_MSI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(MSI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "IRECI":
                IRECI = np.divide((1.0*bandeB7 - bandeB4), (np.divide(1.0*bandeB5 , bandeB6)))
                IRECI[np.isinf(IRECI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_IRECI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(IRECI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "MTCI":
                MTCI = np.divide((1.0*bandeB8 - bandeB5), (bandeB5 - bandeB4))
                MTCI[np.isinf(MTCI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_MTCI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(MTCI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "MCARI":
                MCARI = np.multiply(((bandeB5 - bandeB4) - (0.2*(bandeB5 - bandeB3))), (bandeB5 - bandeB4))
                MCARI[np.isinf(MCARI)]=np.nan
               
                 
                ind = [date,'indclass', "indclass_MCARI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(MCARI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1
     

   
tab[tab == -0.0] = np.nan
tab[tab == 1.0] = np.nan
tab.to_csv(os.path.join(repSortie,nomSortieTab), index=False)
    

####################
####################
### Tuile 32TLQ ####
####################
####################

#Lister les indices souhaités

listeIndices = ["indclass_NDVI","indclass_GNDVI","indclass_NDI45","indclass_NDVIre","indclass_NDII","indclass_NREDI1","indclass_NREDI2","indclass_NREDI3","indclass_PSRI","indclass_MSI","indclass_IRECI","indclass_MTCI","indclass_MCARI"]

#ouvrir les TFE

TFEChemin = "TFE/tfe_bio_T32TLQ_WGS84.shp"    
TFE = gpd.read_file(TFEChemin) #ouverture du shp
   
listeCoordonnees = []
     
for j in range(len(TFE)):
    x = TFE.iloc[j].geometry.centroid.x #récupère les coordonnées d'un point
    y = TFE.iloc[j].geometry.centroid.y
     
    listeCoordonnees.append((x,y))
        
         

#ouverture des bandes
  
repDonnees = r"../applicationMasque/sortie/sortieT32TLQ"
repSortie = "sortie/sortieT32TLQ"

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
    
    nomSortieTab = f"{sat}_{tuile}_tableau.csv"
    
  
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
            with rasterio.open(repCourant+"/S2A_"+date+"_T32TLQ_"+nomIndice[1]+"_masque_scaling.tiff", "r") as src:
                ba = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(repCourant+"/S2A_"+date+"_T32TLQ_"+nomIndice[2]+"_masque_scaling.tiff", "r") as src:
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
            with rasterio.open(repCourant+"/S2A_"+date+"_T32TLQ_"+nomIndice[1]+"_masque_scaling.tiff", "r") as src:
                ba1 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(repCourant+"/S2A_"+date+"_T32TLQ_"+nomIndice[2]+"_masque_scaling.tiff", "r") as src:
                bb1 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(repCourant+"/S2A_"+date+"_T32TLQ_"+nomIndice[3]+"_masque_scaling.tiff", "r") as src:
                bc1 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')

            if nomIndice[0] == "BSI":
                
                BSI =  np.divide((1.0* ba1 - bc1), (bb1 + bc1))
                BSI[np.isinf(BSI)] = np.nan
               
                ind = [date,'BSI', "BSI_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
            
                val = []
        
        
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
        
                    val.append(BSI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
        
        
                index = index+1
                
            if nomIndice[0] == "mSR":
        

                mSR =  np.divide((1.0* ba1 - bc1), (bb1 - bc1))
                mSR[np.isinf(mSR)] = np.nan
               
                ind = [date,'mSR', "mSR_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
               
                val = []
        

                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(mSR[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
                index = index + 1
               
            if nomIndice[0] == "BSITian":

                BSI_Tian =  np.divide((1.0* ba1 - bb1 - bc1), (ba1 + bb1 + bc1))
                BSI_Tian[np.isinf(BSI_Tian)] = np.nan
               
                ind = [date,'BSITian', "BSITian_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
               
                val = []
        
    
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(BSI_Tian[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                    
            if nomIndice[0] == "CVI":

                CVI =  np.multiply((ba1 / bc1), (bb1 / bc1))
                CVI[np.isinf(CVI)] = np.nan
                
               
                ind = [date,'CVI', "CVI_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
               
                val = []
        
    
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(CVI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                

                
###Création des indices usuels:
    
        if len(nomIndice) == 2:    

            with rasterio.open(repCourant+"/"+listeBandes[0], "r") as src:
                bandeB2 = src.read(1)
                profile = src.profile
                profile.update(
                     dtype=rasterio.float64,
                     count=1,
                     compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[1], "r") as src:
                bandeB3 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[2], "r") as src:
                bandeB4 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[3], "r") as src:
                bandeB5 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[4], "r") as src:
                bandeB6 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[5], "r") as src:
                bandeB7 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[6], "r") as src:
                bandeB8 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[7], "r") as src:
                bandeB8a = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[8], "r") as src:
                bandeB11 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')


            if nomIndice[1] == "NDVI":
   
                NDVI = np.divide((1.0*bandeB8 - bandeB4), (bandeB8 + bandeB4))
                NDVI[np.isinf(NDVI)]=np.nan
                
                ind = [date,'indclass', "indclass_NDVI"]
                 
                val = []
                 
                
                for point in listeCoordonnees:
                     col = int((point[0] - xOrigin) / pixelWidth)
                     row = int((yOrigin - point[1] ) / pixelHeight)
                     val.append(NDVI[row][col])
                 
                concat = ind + val
                 
                tab.loc[index]=concat


                index = index+1
                
            if nomIndice[1] == "GNDVI":


                GNDVI = np.divide((1.0*bandeB8 - bandeB3), (bandeB8 + bandeB3))
                GNDVI[np.isinf(GNDVI)]=np.nan
                
                ind = [date,'indclass', "indclass_GNDVI"]
                
                val = []
                
                
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(GNDVI[row][col])
                 
                concat = ind + val
                 
                tab.loc[index]=concat
            
                index = index+1

            if nomIndice[1] == "NDVIre":
                NDVIre = np.divide((1.0*bandeB8a - bandeB4), (bandeB8a + bandeB4))
                NDVIre[np.isinf(NDVIre)]=np.nan
               
                ind = [date,'indclass', "indclass_NDVIre"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(NDVIre[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1

            if nomIndice[1] == "NDVI":
                NDI45 = np.divide((1.0*bandeB5 - bandeB4), (bandeB5 + bandeB4))
                NDI45[np.isinf(NDI45)]=np.nan
               
                ind = [date,'indclass', "indclass_NDI45"]
                
                val = []
                
                
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(NDI45[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat

                index = index+1

            if nomIndice[1] == "NDII":
                NDII = np.divide((1.0*bandeB8 - bandeB11), (bandeB8 + bandeB11))
                NDII[np.isinf(NDII)]=np.nan
                
                ind = [date,'indclass', "indclass_NDII"]
                
                val = []
                
                
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(NDII[row][col])
                 
                concat = ind + val
                     
                tab.loc[index]=concat
            
            
                index = index+1

            if nomIndice[1] == "NDREDI1":
                NREDI1 = np.divide((1.0*bandeB6 - bandeB5), (bandeB6 + bandeB5))
                NREDI1[np.isinf(NREDI1)]=np.nan
                 
                ind = [date,'indclass', "indclass_NREDI1"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(NREDI1[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "NDREDI2":

                NREDI2 = np.divide((1.0*bandeB7 - bandeB5), (bandeB7 + bandeB5))
                NREDI2[np.isinf(NREDI2)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_NREDI2"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(NREDI2[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1



            if nomIndice[1] == "NDREDI3":

                NREDI3 = np.divide((1.0*bandeB7 - bandeB6), (bandeB7 + bandeB6))
                NREDI3[np.isinf(NREDI3)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_NREDI3"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(NREDI3[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1

 

            if nomIndice[1] == "PSRI":

                PSRI = np.divide((1.0*bandeB4 - bandeB3), (bandeB5))
                PSRI[np.isinf(PSRI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_PSRI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(PSRI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1

            if nomIndice[1] == "MSI":
                MSI = np.divide((1.0*bandeB11), (bandeB8))
                MSI[np.isinf(MSI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_MSI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(MSI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "IRECI":
                IRECI = np.divide((1.0*bandeB7 - bandeB4), (np.divide(1.0*bandeB5 , bandeB6)))
                IRECI[np.isinf(IRECI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_IRECI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(IRECI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "MTCI":
                MTCI = np.divide((1.0*bandeB8 - bandeB5), (bandeB5 - bandeB4))
                MTCI[np.isinf(MTCI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_MTCI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(MTCI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "MCARI":
                MCARI = np.multiply(((bandeB5 - bandeB4) - (0.2*(bandeB5 - bandeB3))), (bandeB5 - bandeB4))
                MCARI[np.isinf(MCARI)]=np.nan
               
                 
                ind = [date,'indclass', "indclass_MCARI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(MCARI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1
     

   
tab[tab == -0.0] = np.nan
tab[tab == 1.0] = np.nan
tab.to_csv(os.path.join(repSortie,nomSortieTab), index=False)
    


####################
####################
### Tuile 32TLR ####
####################
####################

#Lister les indices souhaités

listeIndices = ["indclass_NDVI","indclass_GNDVI","indclass_NDI45","indclass_NDVIre","indclass_NDII","indclass_NREDI1","indclass_NREDI2","indclass_NREDI3","indclass_PSRI","indclass_MSI","indclass_IRECI","indclass_MTCI","indclass_MCARI"]

#ouvrir les TFE

TFEChemin = "TFE/tfe_bio_T32TLR_WGS84.shp"    
TFE = gpd.read_file(TFEChemin) #ouverture du shp
   
listeCoordonnees = []
     
for j in range(len(TFE)):
    x = TFE.iloc[j].geometry.centroid.x #récupère les coordonnées d'un point
    y = TFE.iloc[j].geometry.centroid.y
     
    listeCoordonnees.append((x,y))
        
         

#ouverture des bandes
  
repDonnees = r"../applicationMasque/sortie/sortieT32TLR"
repSortie = "sortie/sortieT32TLR"

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
    
    nomSortieTab = f"{sat}_{tuile}_tableau.csv"
    
  
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
            with rasterio.open(repCourant+"/S2A_"+date+"_T32TLR_"+nomIndice[1]+"_masque_scaling.tiff", "r") as src:
                ba = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(repCourant+"/S2A_"+date+"_T32TLR_"+nomIndice[2]+"_masque_scaling.tiff", "r") as src:
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
            with rasterio.open(repCourant+"/S2A_"+date+"_T32TLR_"+nomIndice[1]+"_masque_scaling.tiff", "r") as src:
                ba1 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(repCourant+"/S2A_"+date+"_T32TLR_"+nomIndice[2]+"_masque_scaling.tiff", "r") as src:
                bb1 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(repCourant+"/S2A_"+date+"_T32TLR_"+nomIndice[3]+"_masque_scaling.tiff", "r") as src:
                bc1 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')

            if nomIndice[0] == "BSI":
                
                BSI =  np.divide((1.0* ba1 - bc1), (bb1 + bc1))
                BSI[np.isinf(BSI)] = np.nan
               
                ind = [date,'BSI', "BSI_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
            
                val = []
        
        
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
        
                    val.append(BSI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
        
        
                index = index+1
                
            if nomIndice[0] == "mSR":
        

                mSR =  np.divide((1.0* ba1 - bc1), (bb1 - bc1))
                mSR[np.isinf(mSR)] = np.nan
               
                ind = [date,'mSR', "mSR_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
               
                val = []
        

                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(mSR[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
                index = index + 1
               
            if nomIndice[0] == "BSITian":

                BSI_Tian =  np.divide((1.0* ba1 - bb1 - bc1), (ba1 + bb1 + bc1))
                BSI_Tian[np.isinf(BSI_Tian)] = np.nan
               
                ind = [date,'BSITian', "BSITian_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
               
                val = []
        
    
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(BSI_Tian[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                    
            if nomIndice[0] == "CVI":

                CVI =  np.multiply((ba1 / bc1), (bb1 / bc1))
                CVI[np.isinf(CVI)] = np.nan
                
               
                ind = [date,'CVI', "CVI_"+nomIndice[1]+"_"+nomIndice[2]+"_"+nomIndice[3]]
               
                val = []
        
    
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
    
                    val.append(CVI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                

                
###Création des indices usuels:
    
        if len(nomIndice) == 2:    

            with rasterio.open(repCourant+"/"+listeBandes[0], "r") as src:
                bandeB2 = src.read(1)
                profile = src.profile
                profile.update(
                     dtype=rasterio.float64,
                     count=1,
                     compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[1], "r") as src:
                bandeB3 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[2], "r") as src:
                bandeB4 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[3], "r") as src:
                bandeB5 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[4], "r") as src:
                bandeB6 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[5], "r") as src:
                bandeB7 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[6], "r") as src:
                bandeB8 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[7], "r") as src:
                bandeB8a = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')
            with rasterio.open(repCourant+"/"+listeBandes[8], "r") as src:
                bandeB11 = src.read(1)
                profile = src.profile
                profile.update(
                      dtype=rasterio.float64,
                      count=1,
                      compress='lzw')


            if nomIndice[1] == "NDVI":
   
                NDVI = np.divide((1.0*bandeB8 - bandeB4), (bandeB8 + bandeB4))
                NDVI[np.isinf(NDVI)]=np.nan
                
                ind = [date,'indclass', "indclass_NDVI"]
                 
                val = []
                 
                
                for point in listeCoordonnees:
                     col = int((point[0] - xOrigin) / pixelWidth)
                     row = int((yOrigin - point[1] ) / pixelHeight)
                     val.append(NDVI[row][col])
                 
                concat = ind + val
                 
                tab.loc[index]=concat


                index = index+1
                
            if nomIndice[1] == "GNDVI":


                GNDVI = np.divide((1.0*bandeB8 - bandeB3), (bandeB8 + bandeB3))
                GNDVI[np.isinf(GNDVI)]=np.nan
                
                ind = [date,'indclass', "indclass_GNDVI"]
                
                val = []
                
                
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(GNDVI[row][col])
                 
                concat = ind + val
                 
                tab.loc[index]=concat
            
                index = index+1

            if nomIndice[1] == "NDVIre":
                NDVIre = np.divide((1.0*bandeB8a - bandeB4), (bandeB8a + bandeB4))
                NDVIre[np.isinf(NDVIre)]=np.nan
               
                ind = [date,'indclass', "indclass_NDVIre"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(NDVIre[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1

            if nomIndice[1] == "NDVI":
                NDI45 = np.divide((1.0*bandeB5 - bandeB4), (bandeB5 + bandeB4))
                NDI45[np.isinf(NDI45)]=np.nan
               
                ind = [date,'indclass', "indclass_NDI45"]
                
                val = []
                
                
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(NDI45[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat

                index = index+1

            if nomIndice[1] == "NDII":
                NDII = np.divide((1.0*bandeB8 - bandeB11), (bandeB8 + bandeB11))
                NDII[np.isinf(NDII)]=np.nan
                
                ind = [date,'indclass', "indclass_NDII"]
                
                val = []
                
                
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
                    val.append(NDII[row][col])
                 
                concat = ind + val
                     
                tab.loc[index]=concat
            
            
                index = index+1

            if nomIndice[1] == "NDREDI1":
                NREDI1 = np.divide((1.0*bandeB6 - bandeB5), (bandeB6 + bandeB5))
                NREDI1[np.isinf(NREDI1)]=np.nan
                 
                ind = [date,'indclass', "indclass_NREDI1"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(NREDI1[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "NDREDI2":

                NREDI2 = np.divide((1.0*bandeB7 - bandeB5), (bandeB7 + bandeB5))
                NREDI2[np.isinf(NREDI2)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_NREDI2"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(NREDI2[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1



            if nomIndice[1] == "NDREDI3":

                NREDI3 = np.divide((1.0*bandeB7 - bandeB6), (bandeB7 + bandeB6))
                NREDI3[np.isinf(NREDI3)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_NREDI3"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(NREDI3[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1

 

            if nomIndice[1] == "PSRI":

                PSRI = np.divide((1.0*bandeB4 - bandeB3), (bandeB5))
                PSRI[np.isinf(PSRI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_PSRI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(PSRI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1

            if nomIndice[1] == "MSI":
                MSI = np.divide((1.0*bandeB11), (bandeB8))
                MSI[np.isinf(MSI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_MSI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(MSI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "IRECI":
                IRECI = np.divide((1.0*bandeB7 - bandeB4), (np.divide(1.0*bandeB5 , bandeB6)))
                IRECI[np.isinf(IRECI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_IRECI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(IRECI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "MTCI":
                MTCI = np.divide((1.0*bandeB8 - bandeB5), (bandeB5 - bandeB4))
                MTCI[np.isinf(MTCI)]=np.nan
                
                 
                ind = [date,'indclass', "indclass_MTCI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(MTCI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1


            if nomIndice[1] == "MCARI":
                MCARI = np.multiply(((bandeB5 - bandeB4) - (0.2*(bandeB5 - bandeB3))), (bandeB5 - bandeB4))
                MCARI[np.isinf(MCARI)]=np.nan
               
                 
                ind = [date,'indclass', "indclass_MCARI"]
            
                val = []
            
            
                for point in listeCoordonnees:
                    col = int((point[0] - xOrigin) / pixelWidth)
                    row = int((yOrigin - point[1] ) / pixelHeight)
            
                    val.append(MCARI[row][col])
                    
                concat = ind + val
                    
                tab.loc[index]=concat
            
            
                index = index+1
     

   
tab[tab == -0.0] = np.nan
tab[tab == 1.0] = np.nan
tab.to_csv(os.path.join(repSortie,nomSortieTab), index=False)
    