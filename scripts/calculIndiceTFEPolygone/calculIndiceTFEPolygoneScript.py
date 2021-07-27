#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 11:49:07 2021

@author: Emilie SIROT
"""


import os
from osgeo import gdal
import itertools
import rasterio
from rasterstats import zonal_stats, point_query
import numpy as np 
import geopandas as gpd
import pandas as pd



####################
####################
### Tuile 31TFJ ####
####################
####################

 
 
repDonnees = r"../applicationMasque/sortie/sortieT31TFJ"
repSortie = "sortie/sortieT31TFJ"


listeRep = os.listdir(repDonnees)

#ouvrir les TFE

TFEChemin = "TFE/polygones_T31TFJ.shp"    
TFE = gpd.read_file(TFEChemin)


#stats = zonal_stats(TFE2,repCourant+"/"+B2[0], stats = 'mean')
        
        
for i in range (len(listeRep)):
    repCourant = os.path.join(repDonnees, listeRep[i])#se positionner dans le répertoire d'une date
    fichiersRep = os.listdir(repCourant)#lister les fichiers à savoir les différentes bandes
    
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
    
    repSortieDate = os.path.join(repSortie, listeRep[i]) 
    if not os.path.exists(repSortieDate):
        os.makedirs(repSortieDate)
    
     

    legende = ["indices","bandes"]
    entites = len(TFE)
    for entite in range(1,entites+1):
        legende.append(entite)
 
    
    Typo_AS = ["/","/"]
    for typoas in range(len(TFE.typo_AS)):
        Typo_AS.append(TFE.typo_AS[typoas])
    
    Territoire = ["/","/"]
    for territoire in range(len(TFE.territoire)):
        Territoire.append(TFE.territoire[territoire])

   #creation du tableau
    
    tab = pd.DataFrame(columns = legende)
    tab.loc[1]=Typo_AS
    tab.loc[2]=Territoire
    

    index = 3

        
    #calcul des indices
        
  
    print(index)
    
            #two bands vegetation indices (normalized difference et simple ratio)
    
    for elt in itertools.permutations(listeBandes,2):
        bande1 = elt[0].split("_")[3]
        bande2 = elt[1].split("_")[3]
        
     
        with rasterio.open(repCourant+"/"+elt[0], "r") as src:
            ba = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
        with rasterio.open(repCourant+"/"+elt[1], "r") as src:
            bb = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')


        affine = src.transform

        ND =  np.divide((1.0*ba - bb), (ba + bb))
        ND[np.isinf(ND)] = np.nan
        double = tab['bandes']=="ND_"+bande1+"_"+bande2
        doubleInv = tab['bandes']=="ND_"+bande2+"_"+bande1
        if any(double) == False :
            if any(doubleInv)== False :
        #if not os.path.exists(dst_ND):
            #if not os.path.exists(dst_ND_inv): #on observe que a/b = 1/(b/a)
                ind = ['ND', "ND_"+bande1+"_"+bande2]
               
                
                
                stats = zonal_stats(TFEChemin, ND, stats = 'mean', affine=affine)
          
                val = []
                
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                
    

        SR = np.divide(ba, bb)
        SR[np.isinf(SR)] = np.nan
        double = tab['bandes']=="SR_"+bande1+"_"+bande2
        if any(double) == False:
                #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
         
            ind = ['SR', "SR_"+bande1+"_"+bande2]
        
            stats = zonal_stats(TFEChemin, SR, stats = 'mean', affine=affine)
          
            val = []
                
            for stat in range(len(stats)):
                val.append(stats[stat].get('mean'))
                
            concat = ind + val
                
            tab.loc[index]=concat
            
            index = index + 1
 
    print(index)

              # three bands vegetation indices (3BSI / mSR et 3BSI_Tian)
    for elt in itertools.permutations(listeBandes,3):
        bande1 = elt[0].split("_")[3]
        bande2 = elt[1].split("_")[3]
        bande3 = elt[2].split("_")[3]
 
        with rasterio.open(repCourant+"/"+elt[0], "r") as src:
            ba1 = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
        with rasterio.open(repCourant+"/"+elt[1], "r") as src:
            bb1 = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
        with rasterio.open(repCourant+"/"+elt[2], "r") as src:
            bc1 = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
            
        affine = src.transform
            
        BSI =  np.divide((1.0* ba1 - bc1), (bb1 + bc1))
        BSI[np.isinf(BSI)] = np.nan
        double = tab['bandes']=="BSI_"+bande1+"_"+bande2+"_"+bande3
        if any(double) == False:
                #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
         
            ind = ['BSI', "BSI_"+bande1+"_"+bande2+"_"+bande3]
        

            stats = zonal_stats(TFEChemin, BSI, stats = 'mean', affine=affine)
              
            val = []
                
            for stat in range(len(stats)):
                val.append(stats[stat].get('mean'))
                
            concat = ind + val
                
            tab.loc[index]=concat
            
            index = index + 1
            print(index)

        mSR =  np.divide((1.0* ba1 - bc1), (bb1 - bc1))
        mSR[np.isinf(mSR)] = np.nan
        double = tab['bandes']=="mSR_"+bande1+"_"+bande2+"_"+bande3
        doubleInv = tab['bandes']=="mSR_"+bande1+"_"+bande3+"_"+bande2
        if any(double) == False :
            if any(doubleInv)== False :
       
                ind = ['mSR', "mSR_"+bande1+"_"+bande2+"_"+bande3]
               
                stats = zonal_stats(TFEChemin, mSR, stats = 'mean', affine=affine)
              
                val = []
                    
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                print(index)

        BSI_Tian =  np.divide((1.0* ba1 - bb1 - bc1), (ba1 + bb1 + bc1))
        BSI_Tian[np.isinf(BSI_Tian)] = np.nan
        double = tab['bandes']=="BSITian_"+bande1+"_"+bande2+"_"+bande3
        doubleInv = tab['bandes']=="BSITian_"+bande1+"_"+bande3+"_"+bande2
        if any(double) == False :
            if any(doubleInv)== False :
                ind = ['BSITian', "BSITian_"+bande1+"_"+bande2+"_"+bande3]
               
                stats = zonal_stats(TFEChemin, BSI_Tian, stats = 'mean', affine=affine)
              
                val = []
                    
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                print(index)

        CVI =  np.multiply((ba1 / bc1), (bb1 / bc1))
        CVI[np.isinf(CVI)] = np.nan
        double = tab['bandes']=="CVI_"+bande1+"_"+bande2+"_"+bande3
        doubleInv = tab['bandes']=="CVI_"+bande1+"_"+bande3+"_"+bande2
        if any(double) == False :
            if any(doubleInv)== False :
       
                ind = ['CVI', "CVI_"+bande1+"_"+bande2+"_"+bande3]
               
                stats = zonal_stats(TFEChemin, CVI, stats = 'mean', affine=affine)
              
                val = []
                    
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                print(index)
    
    
    ###Création des indices usuels:
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
    
    affine = src.transform
  
 
#Calcul des indices classiques

 
#calcul du NDVI
    NDVI = np.divide((1.0*bandeB8 - bandeB4), (bandeB8 + bandeB4))
    NDVI[np.isinf(NDVI)]=np.nan
    double = tab['bandes']=="indclass_NDVI"
    if any(double) == False:
          #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
  
        ind = ['indclass', "indclass_NDVI"]
         
        stats = zonal_stats(TFEChemin, NDVI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du GNDVI
    GNDVI = np.divide((1.0*bandeB8 - bandeB3), (bandeB8 + bandeB3))
    GNDVI[np.isinf(GNDVI)]=np.nan
    double = tab['bandes']=="indclass_GNDVI"
    if any(double) == False:
                #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_GNDVI"]
        
        stats = zonal_stats(TFEChemin, GNDVI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1


 #calcul du NDVIre
    NDVIre = np.divide((1.0*bandeB8a - bandeB4), (bandeB8a + bandeB4))
    NDVIre[np.isinf(NDVIre)]=np.nan
    double = tab['bandes']=="indclass_NDVIre"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NDVIre"]
    
        stats = zonal_stats(TFEChemin, NDVIre, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NDI45
    NDI45 = np.divide((1.0*bandeB5 - bandeB4), (bandeB5 + bandeB4))
    NDI45[np.isinf(NDI45)]=np.nan
    double = tab['bandes']=="indclass_NDI45"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
  
        ind = ['indclass', "indclass_NDI45"]
        
        stats = zonal_stats(TFEChemin, NDI45, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NDII
    NDII = np.divide((1.0*bandeB8 - bandeB11), (bandeB8 + bandeB11))
    NDII[np.isinf(NDII)]=np.nan
    double = tab['bandes']=="indclass_NDII"
    if any(double) == False:
         #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
  
        ind = ['indclass', "indclass_NDII"]
        
        stats = zonal_stats(TFEChemin, NDII, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NREDI1
    NREDI1 = np.divide((1.0*bandeB6 - bandeB5), (bandeB6 + bandeB5))
    NREDI1[np.isinf(NREDI1)]=np.nan
    double = tab['bandes']=="indclass_NREDI1"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NREDI1"]
    
        stats = zonal_stats(TFEChemin, NREDI1, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NREDI2
    NREDI2 = np.divide((1.0*bandeB7 - bandeB5), (bandeB7 + bandeB5))
    NREDI2[np.isinf(NREDI2)]=np.nan
    double = tab['bandes']=="indclass_NREDI2"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NREDI2"]
    
        stats = zonal_stats(TFEChemin, NREDI2, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NREDI3
    NREDI3 = np.divide((1.0*bandeB7 - bandeB6), (bandeB7 + bandeB6))
    NREDI3[np.isinf(NREDI3)]=np.nan
    double = tab['bandes']=="indclass_NREDI3"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NREDI3"]
    
        stats = zonal_stats(TFEChemin, NREDI3, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du PSRI
    PSRI = np.divide((1.0*bandeB4 - bandeB3), (bandeB5))
    PSRI[np.isinf(PSRI)]=np.nan
    double = tab['bandes']=="indclass_PSRI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_PSRI"]
    
        stats = zonal_stats(TFEChemin, PSRI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du MSI
    MSI = np.divide((1.0*bandeB11), (bandeB8))
    MSI[np.isinf(MSI)]=np.nan
    double = tab['bandes']=="indclass_MSI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_MSI"]
    
        stats = zonal_stats(TFEChemin, MSI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du IRECI
    IRECI = np.divide((1.0*bandeB7 - bandeB4), (np.divide(1.0*bandeB5 , bandeB6)))
    IRECI[np.isinf(IRECI)]=np.nan
    double = tab['bandes']=="indclass_IRECI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_IRECI"]
    
        stats = zonal_stats(TFEChemin, IRECI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du MTCI
    MTCI = np.divide((1.0*bandeB8 - bandeB5), (bandeB5 - bandeB4))
    MTCI[np.isinf(MTCI)]=np.nan
    double = tab['bandes']=="indclass_MTCI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_MTCI"]
    
        stats = zonal_stats(TFEChemin, MTCI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du MCARI
    MCARI = np.multiply(((bandeB5 - bandeB4) - (0.2*(bandeB5 - bandeB3))), (bandeB5 - bandeB4))
    MCARI[np.isinf(MCARI)]=np.nan
    double = tab['bandes']=="indclass_MCARI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_MCARI"]
    
        stats = zonal_stats(TFEChemin, MCARI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1
     

    print(index)

    tab.to_csv(os.path.join(repSortieDate,nomSortieTab))
    

####################
####################
### Tuile 31TFK ####
####################
####################

 
 
repDonnees = r"../applicationMasque/sortie/sortieT31TFK"
repSortie = "sortie/sortieT31TFK"


listeRep = os.listdir(repDonnees)

#ouvrir les TFE

TFEChemin = "TFE/polygones_T31TFK.shp"    
TFE = gpd.read_file(TFEChemin)


#stats = zonal_stats(TFE2,repCourant+"/"+B2[0], stats = 'mean')
        
        
for i in range (len(listeRep)):
    repCourant = os.path.join(repDonnees, listeRep[i])#se positionner dans le répertoire d'une date
    fichiersRep = os.listdir(repCourant)#lister les fichiers à savoir les différentes bandes
    
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
    
    repSortieDate = os.path.join(repSortie, listeRep[i]) 
    if not os.path.exists(repSortieDate):
        os.makedirs(repSortieDate)
    
     

    legende = ["indices","bandes"]
    entites = len(TFE)
    for entite in range(1,entites+1):
        legende.append(entite)
 
    
    Typo_AS = ["/","/"]
    for typoas in range(len(TFE.typo_AS)):
        Typo_AS.append(TFE.typo_AS[typoas])
    
    Territoire = ["/","/"]
    for territoire in range(len(TFE.territoire)):
        Territoire.append(TFE.territoire[territoire])

   #creation du tableau
    
    tab = pd.DataFrame(columns = legende)
    tab.loc[1]=Typo_AS
    tab.loc[2]=Territoire
    

    index = 3

        
    #calcul des indices
        
  
    print(index)
    
            #two bands vegetation indices (normalized difference et simple ratio)
    
    for elt in itertools.permutations(listeBandes,2):
        bande1 = elt[0].split("_")[3]
        bande2 = elt[1].split("_")[3]
        
     
        with rasterio.open(repCourant+"/"+elt[0], "r") as src:
            ba = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
        with rasterio.open(repCourant+"/"+elt[1], "r") as src:
            bb = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')


        affine = src.transform

        ND =  np.divide((1.0*ba - bb), (ba + bb))
        ND[np.isinf(ND)] = np.nan
        double = tab['bandes']=="ND_"+bande1+"_"+bande2
        doubleInv = tab['bandes']=="ND_"+bande2+"_"+bande1
        if any(double) == False :
            if any(doubleInv)== False :
        #if not os.path.exists(dst_ND):
            #if not os.path.exists(dst_ND_inv): #on observe que a/b = 1/(b/a)
                ind = ['ND', "ND_"+bande1+"_"+bande2]
               
                
                
                stats = zonal_stats(TFEChemin, ND, stats = 'mean', affine=affine)
          
                val = []
                
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                
    

        SR = np.divide(ba, bb)
        SR[np.isinf(SR)] = np.nan
        double = tab['bandes']=="SR_"+bande1+"_"+bande2
        if any(double) == False:
                #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
         
            ind = ['SR', "SR_"+bande1+"_"+bande2]
        
            stats = zonal_stats(TFEChemin, SR, stats = 'mean', affine=affine)
          
            val = []
                
            for stat in range(len(stats)):
                val.append(stats[stat].get('mean'))
                
            concat = ind + val
                
            tab.loc[index]=concat
            
            index = index + 1
 
    print(index)

              # three bands vegetation indices (3BSI / mSR et 3BSI_Tian)
    for elt in itertools.permutations(listeBandes,3):
        bande1 = elt[0].split("_")[3]
        bande2 = elt[1].split("_")[3]
        bande3 = elt[2].split("_")[3]
 
        with rasterio.open(repCourant+"/"+elt[0], "r") as src:
            ba1 = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
        with rasterio.open(repCourant+"/"+elt[1], "r") as src:
            bb1 = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
        with rasterio.open(repCourant+"/"+elt[2], "r") as src:
            bc1 = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
            
        affine = src.transform
            
        BSI =  np.divide((1.0* ba1 - bc1), (bb1 + bc1))
        BSI[np.isinf(BSI)] = np.nan
        double = tab['bandes']=="BSI_"+bande1+"_"+bande2+"_"+bande3
        if any(double) == False:
                #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
         
            ind = ['BSI', "BSI_"+bande1+"_"+bande2+"_"+bande3]
        

            stats = zonal_stats(TFEChemin, BSI, stats = 'mean', affine=affine)
              
            val = []
                
            for stat in range(len(stats)):
                val.append(stats[stat].get('mean'))
                
            concat = ind + val
                
            tab.loc[index]=concat
            
            index = index + 1
            print(index)

        mSR =  np.divide((1.0* ba1 - bc1), (bb1 - bc1))
        mSR[np.isinf(mSR)] = np.nan
        double = tab['bandes']=="mSR_"+bande1+"_"+bande2+"_"+bande3
        doubleInv = tab['bandes']=="mSR_"+bande1+"_"+bande3+"_"+bande2
        if any(double) == False :
            if any(doubleInv)== False :
       
                ind = ['mSR', "mSR_"+bande1+"_"+bande2+"_"+bande3]
               
                stats = zonal_stats(TFEChemin, mSR, stats = 'mean', affine=affine)
              
                val = []
                    
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                print(index)

        BSI_Tian =  np.divide((1.0* ba1 - bb1 - bc1), (ba1 + bb1 + bc1))
        BSI_Tian[np.isinf(BSI_Tian)] = np.nan
        double = tab['bandes']=="BSITian_"+bande1+"_"+bande2+"_"+bande3
        doubleInv = tab['bandes']=="BSITian_"+bande1+"_"+bande3+"_"+bande2
        if any(double) == False :
            if any(doubleInv)== False :
                ind = ['BSITian', "BSITian_"+bande1+"_"+bande2+"_"+bande3]
               
                stats = zonal_stats(TFEChemin, BSI_Tian, stats = 'mean', affine=affine)
              
                val = []
                    
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                print(index)

        CVI =  np.multiply((ba1 / bc1), (bb1 / bc1))
        CVI[np.isinf(CVI)] = np.nan
        double = tab['bandes']=="CVI_"+bande1+"_"+bande2+"_"+bande3
        doubleInv = tab['bandes']=="CVI_"+bande1+"_"+bande3+"_"+bande2
        if any(double) == False :
            if any(doubleInv)== False :
       
                ind = ['CVI', "CVI_"+bande1+"_"+bande2+"_"+bande3]
               
                stats = zonal_stats(TFEChemin, CVI, stats = 'mean', affine=affine)
              
                val = []
                    
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                print(index)
    
    
    ###Création des indices usuels:
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
    
    affine = src.transform
  
 
#Calcul des indices classiques

 
#calcul du NDVI
    NDVI = np.divide((1.0*bandeB8 - bandeB4), (bandeB8 + bandeB4))
    NDVI[np.isinf(NDVI)]=np.nan
    double = tab['bandes']=="indclass_NDVI"
    if any(double) == False:
          #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
  
        ind = ['indclass', "indclass_NDVI"]
         
        stats = zonal_stats(TFEChemin, NDVI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du GNDVI
    GNDVI = np.divide((1.0*bandeB8 - bandeB3), (bandeB8 + bandeB3))
    GNDVI[np.isinf(GNDVI)]=np.nan
    double = tab['bandes']=="indclass_GNDVI"
    if any(double) == False:
                #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_GNDVI"]
        
        stats = zonal_stats(TFEChemin, GNDVI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1


 #calcul du NDVIre
    NDVIre = np.divide((1.0*bandeB8a - bandeB4), (bandeB8a + bandeB4))
    NDVIre[np.isinf(NDVIre)]=np.nan
    double = tab['bandes']=="indclass_NDVIre"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NDVIre"]
    
        stats = zonal_stats(TFEChemin, NDVIre, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NDI45
    NDI45 = np.divide((1.0*bandeB5 - bandeB4), (bandeB5 + bandeB4))
    NDI45[np.isinf(NDI45)]=np.nan
    double = tab['bandes']=="indclass_NDI45"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
  
        ind = ['indclass', "indclass_NDI45"]
        
        stats = zonal_stats(TFEChemin, NDI45, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NDII
    NDII = np.divide((1.0*bandeB8 - bandeB11), (bandeB8 + bandeB11))
    NDII[np.isinf(NDII)]=np.nan
    double = tab['bandes']=="indclass_NDII"
    if any(double) == False:
         #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
  
        ind = ['indclass', "indclass_NDII"]
        
        stats = zonal_stats(TFEChemin, NDII, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NREDI1
    NREDI1 = np.divide((1.0*bandeB6 - bandeB5), (bandeB6 + bandeB5))
    NREDI1[np.isinf(NREDI1)]=np.nan
    double = tab['bandes']=="indclass_NREDI1"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NREDI1"]
    
        stats = zonal_stats(TFEChemin, NREDI1, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NREDI2
    NREDI2 = np.divide((1.0*bandeB7 - bandeB5), (bandeB7 + bandeB5))
    NREDI2[np.isinf(NREDI2)]=np.nan
    double = tab['bandes']=="indclass_NREDI2"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NREDI2"]
    
        stats = zonal_stats(TFEChemin, NREDI2, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NREDI3
    NREDI3 = np.divide((1.0*bandeB7 - bandeB6), (bandeB7 + bandeB6))
    NREDI3[np.isinf(NREDI3)]=np.nan
    double = tab['bandes']=="indclass_NREDI3"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NREDI3"]
    
        stats = zonal_stats(TFEChemin, NREDI3, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du PSRI
    PSRI = np.divide((1.0*bandeB4 - bandeB3), (bandeB5))
    PSRI[np.isinf(PSRI)]=np.nan
    double = tab['bandes']=="indclass_PSRI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_PSRI"]
    
        stats = zonal_stats(TFEChemin, PSRI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du MSI
    MSI = np.divide((1.0*bandeB11), (bandeB8))
    MSI[np.isinf(MSI)]=np.nan
    double = tab['bandes']=="indclass_MSI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_MSI"]
    
        stats = zonal_stats(TFEChemin, MSI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du IRECI
    IRECI = np.divide((1.0*bandeB7 - bandeB4), (np.divide(1.0*bandeB5 , bandeB6)))
    IRECI[np.isinf(IRECI)]=np.nan
    double = tab['bandes']=="indclass_IRECI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_IRECI"]
    
        stats = zonal_stats(TFEChemin, IRECI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du MTCI
    MTCI = np.divide((1.0*bandeB8 - bandeB5), (bandeB5 - bandeB4))
    MTCI[np.isinf(MTCI)]=np.nan
    double = tab['bandes']=="indclass_MTCI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_MTCI"]
    
        stats = zonal_stats(TFEChemin, MTCI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du MCARI
    MCARI = np.multiply(((bandeB5 - bandeB4) - (0.2*(bandeB5 - bandeB3))), (bandeB5 - bandeB4))
    MCARI[np.isinf(MCARI)]=np.nan
    double = tab['bandes']=="indclass_MCARI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_MCARI"]
    
        stats = zonal_stats(TFEChemin, MCARI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1
     

    print(index)

    tab.to_csv(os.path.join(repSortieDate,nomSortieTab))
    

####################
####################
### Tuile 31TGK ####
####################
####################

 
 
repDonnees = r"../applicationMasque/sortie/sortieT31TGK"
repSortie = "sortie/sortieT31TGK"


listeRep = os.listdir(repDonnees)

#ouvrir les TFE

TFEChemin = "TFE/polygones_T31TGK.shp"    
TFE = gpd.read_file(TFEChemin)


#stats = zonal_stats(TFE2,repCourant+"/"+B2[0], stats = 'mean')
        
        
for i in range (len(listeRep)):
    repCourant = os.path.join(repDonnees, listeRep[i])#se positionner dans le répertoire d'une date
    fichiersRep = os.listdir(repCourant)#lister les fichiers à savoir les différentes bandes
    
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
    
    repSortieDate = os.path.join(repSortie, listeRep[i]) 
    if not os.path.exists(repSortieDate):
        os.makedirs(repSortieDate)
    
     

    legende = ["indices","bandes"]
    entites = len(TFE)
    for entite in range(1,entites+1):
        legende.append(entite)
 
    
    Typo_AS = ["/","/"]
    for typoas in range(len(TFE.typo_AS)):
        Typo_AS.append(TFE.typo_AS[typoas])
    
    Territoire = ["/","/"]
    for territoire in range(len(TFE.territoire)):
        Territoire.append(TFE.territoire[territoire])

   #creation du tableau
    
    tab = pd.DataFrame(columns = legende)
    tab.loc[1]=Typo_AS
    tab.loc[2]=Territoire
    

    index = 3

        
    #calcul des indices
        
  
    print(index)
    
            #two bands vegetation indices (normalized difference et simple ratio)
    
    for elt in itertools.permutations(listeBandes,2):
        bande1 = elt[0].split("_")[3]
        bande2 = elt[1].split("_")[3]
        
     
        with rasterio.open(repCourant+"/"+elt[0], "r") as src:
            ba = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
        with rasterio.open(repCourant+"/"+elt[1], "r") as src:
            bb = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')


        affine = src.transform

        ND =  np.divide((1.0*ba - bb), (ba + bb))
        ND[np.isinf(ND)] = np.nan
        double = tab['bandes']=="ND_"+bande1+"_"+bande2
        doubleInv = tab['bandes']=="ND_"+bande2+"_"+bande1
        if any(double) == False :
            if any(doubleInv)== False :
        #if not os.path.exists(dst_ND):
            #if not os.path.exists(dst_ND_inv): #on observe que a/b = 1/(b/a)
                ind = ['ND', "ND_"+bande1+"_"+bande2]
               
                
                
                stats = zonal_stats(TFEChemin, ND, stats = 'mean', affine=affine)
          
                val = []
                
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                
    

        SR = np.divide(ba, bb)
        SR[np.isinf(SR)] = np.nan
        double = tab['bandes']=="SR_"+bande1+"_"+bande2
        if any(double) == False:
                #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
         
            ind = ['SR', "SR_"+bande1+"_"+bande2]
        
            stats = zonal_stats(TFEChemin, SR, stats = 'mean', affine=affine)
          
            val = []
                
            for stat in range(len(stats)):
                val.append(stats[stat].get('mean'))
                
            concat = ind + val
                
            tab.loc[index]=concat
            
            index = index + 1
 
    print(index)

              # three bands vegetation indices (3BSI / mSR et 3BSI_Tian)
    for elt in itertools.permutations(listeBandes,3):
        bande1 = elt[0].split("_")[3]
        bande2 = elt[1].split("_")[3]
        bande3 = elt[2].split("_")[3]
 
        with rasterio.open(repCourant+"/"+elt[0], "r") as src:
            ba1 = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
        with rasterio.open(repCourant+"/"+elt[1], "r") as src:
            bb1 = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
        with rasterio.open(repCourant+"/"+elt[2], "r") as src:
            bc1 = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
            
        affine = src.transform
            
        BSI =  np.divide((1.0* ba1 - bc1), (bb1 + bc1))
        BSI[np.isinf(BSI)] = np.nan
        double = tab['bandes']=="BSI_"+bande1+"_"+bande2+"_"+bande3
        if any(double) == False:
                #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
         
            ind = ['BSI', "BSI_"+bande1+"_"+bande2+"_"+bande3]
        

            stats = zonal_stats(TFEChemin, BSI, stats = 'mean', affine=affine)
              
            val = []
                
            for stat in range(len(stats)):
                val.append(stats[stat].get('mean'))
                
            concat = ind + val
                
            tab.loc[index]=concat
            
            index = index + 1
            print(index)

        mSR =  np.divide((1.0* ba1 - bc1), (bb1 - bc1))
        mSR[np.isinf(mSR)] = np.nan
        double = tab['bandes']=="mSR_"+bande1+"_"+bande2+"_"+bande3
        doubleInv = tab['bandes']=="mSR_"+bande1+"_"+bande3+"_"+bande2
        if any(double) == False :
            if any(doubleInv)== False :
       
                ind = ['mSR', "mSR_"+bande1+"_"+bande2+"_"+bande3]
               
                stats = zonal_stats(TFEChemin, mSR, stats = 'mean', affine=affine)
              
                val = []
                    
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                print(index)

        BSI_Tian =  np.divide((1.0* ba1 - bb1 - bc1), (ba1 + bb1 + bc1))
        BSI_Tian[np.isinf(BSI_Tian)] = np.nan
        double = tab['bandes']=="BSITian_"+bande1+"_"+bande2+"_"+bande3
        doubleInv = tab['bandes']=="BSITian_"+bande1+"_"+bande3+"_"+bande2
        if any(double) == False :
            if any(doubleInv)== False :
                ind = ['BSITian', "BSITian_"+bande1+"_"+bande2+"_"+bande3]
               
                stats = zonal_stats(TFEChemin, BSI_Tian, stats = 'mean', affine=affine)
              
                val = []
                    
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                print(index)

        CVI =  np.multiply((ba1 / bc1), (bb1 / bc1))
        CVI[np.isinf(CVI)] = np.nan
        double = tab['bandes']=="CVI_"+bande1+"_"+bande2+"_"+bande3
        doubleInv = tab['bandes']=="CVI_"+bande1+"_"+bande3+"_"+bande2
        if any(double) == False :
            if any(doubleInv)== False :
       
                ind = ['CVI', "CVI_"+bande1+"_"+bande2+"_"+bande3]
               
                stats = zonal_stats(TFEChemin, CVI, stats = 'mean', affine=affine)
              
                val = []
                    
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                print(index)
    
    
    ###Création des indices usuels:
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
    
    affine = src.transform
  
 
#Calcul des indices classiques

 
#calcul du NDVI
    NDVI = np.divide((1.0*bandeB8 - bandeB4), (bandeB8 + bandeB4))
    NDVI[np.isinf(NDVI)]=np.nan
    double = tab['bandes']=="indclass_NDVI"
    if any(double) == False:
          #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
  
        ind = ['indclass', "indclass_NDVI"]
         
        stats = zonal_stats(TFEChemin, NDVI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du GNDVI
    GNDVI = np.divide((1.0*bandeB8 - bandeB3), (bandeB8 + bandeB3))
    GNDVI[np.isinf(GNDVI)]=np.nan
    double = tab['bandes']=="indclass_GNDVI"
    if any(double) == False:
                #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_GNDVI"]
        
        stats = zonal_stats(TFEChemin, GNDVI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1


 #calcul du NDVIre
    NDVIre = np.divide((1.0*bandeB8a - bandeB4), (bandeB8a + bandeB4))
    NDVIre[np.isinf(NDVIre)]=np.nan
    double = tab['bandes']=="indclass_NDVIre"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NDVIre"]
    
        stats = zonal_stats(TFEChemin, NDVIre, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NDI45
    NDI45 = np.divide((1.0*bandeB5 - bandeB4), (bandeB5 + bandeB4))
    NDI45[np.isinf(NDI45)]=np.nan
    double = tab['bandes']=="indclass_NDI45"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
  
        ind = ['indclass', "indclass_NDI45"]
        
        stats = zonal_stats(TFEChemin, NDI45, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NDII
    NDII = np.divide((1.0*bandeB8 - bandeB11), (bandeB8 + bandeB11))
    NDII[np.isinf(NDII)]=np.nan
    double = tab['bandes']=="indclass_NDII"
    if any(double) == False:
         #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
  
        ind = ['indclass', "indclass_NDII"]
        
        stats = zonal_stats(TFEChemin, NDII, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NREDI1
    NREDI1 = np.divide((1.0*bandeB6 - bandeB5), (bandeB6 + bandeB5))
    NREDI1[np.isinf(NREDI1)]=np.nan
    double = tab['bandes']=="indclass_NREDI1"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NREDI1"]
    
        stats = zonal_stats(TFEChemin, NREDI1, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NREDI2
    NREDI2 = np.divide((1.0*bandeB7 - bandeB5), (bandeB7 + bandeB5))
    NREDI2[np.isinf(NREDI2)]=np.nan
    double = tab['bandes']=="indclass_NREDI2"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NREDI2"]
    
        stats = zonal_stats(TFEChemin, NREDI2, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NREDI3
    NREDI3 = np.divide((1.0*bandeB7 - bandeB6), (bandeB7 + bandeB6))
    NREDI3[np.isinf(NREDI3)]=np.nan
    double = tab['bandes']=="indclass_NREDI3"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NREDI3"]
    
        stats = zonal_stats(TFEChemin, NREDI3, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du PSRI
    PSRI = np.divide((1.0*bandeB4 - bandeB3), (bandeB5))
    PSRI[np.isinf(PSRI)]=np.nan
    double = tab['bandes']=="indclass_PSRI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_PSRI"]
    
        stats = zonal_stats(TFEChemin, PSRI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du MSI
    MSI = np.divide((1.0*bandeB11), (bandeB8))
    MSI[np.isinf(MSI)]=np.nan
    double = tab['bandes']=="indclass_MSI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_MSI"]
    
        stats = zonal_stats(TFEChemin, MSI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du IRECI
    IRECI = np.divide((1.0*bandeB7 - bandeB4), (np.divide(1.0*bandeB5 , bandeB6)))
    IRECI[np.isinf(IRECI)]=np.nan
    double = tab['bandes']=="indclass_IRECI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_IRECI"]
    
        stats = zonal_stats(TFEChemin, IRECI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du MTCI
    MTCI = np.divide((1.0*bandeB8 - bandeB5), (bandeB5 - bandeB4))
    MTCI[np.isinf(MTCI)]=np.nan
    double = tab['bandes']=="indclass_MTCI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_MTCI"]
    
        stats = zonal_stats(TFEChemin, MTCI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du MCARI
    MCARI = np.multiply(((bandeB5 - bandeB4) - (0.2*(bandeB5 - bandeB3))), (bandeB5 - bandeB4))
    MCARI[np.isinf(MCARI)]=np.nan
    double = tab['bandes']=="indclass_MCARI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_MCARI"]
    
        stats = zonal_stats(TFEChemin, MCARI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1
     

    print(index)

    tab.to_csv(os.path.join(repSortieDate,nomSortieTab))
    
####################
####################
### Tuile 31TGL ####
####################
####################

 
 
repDonnees = r"../applicationMasque/sortie/sortieT31TGL"
repSortie = "sortie/sortieT31TGL"


listeRep = os.listdir(repDonnees)

#ouvrir les TFE

TFEChemin = "TFE/polygones_T31TGL.shp"    
TFE = gpd.read_file(TFEChemin)


#stats = zonal_stats(TFE2,repCourant+"/"+B2[0], stats = 'mean')
        
        
for i in range (len(listeRep)):
    repCourant = os.path.join(repDonnees, listeRep[i])#se positionner dans le répertoire d'une date
    fichiersRep = os.listdir(repCourant)#lister les fichiers à savoir les différentes bandes
    
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
    
    repSortieDate = os.path.join(repSortie, listeRep[i]) 
    if not os.path.exists(repSortieDate):
        os.makedirs(repSortieDate)
    
     

    legende = ["indices","bandes"]
    entites = len(TFE)
    for entite in range(1,entites+1):
        legende.append(entite)
 
    
    Typo_AS = ["/","/"]
    for typoas in range(len(TFE.typo_AS)):
        Typo_AS.append(TFE.typo_AS[typoas])
    
    Territoire = ["/","/"]
    for territoire in range(len(TFE.territoire)):
        Territoire.append(TFE.territoire[territoire])

   #creation du tableau
    
    tab = pd.DataFrame(columns = legende)
    tab.loc[1]=Typo_AS
    tab.loc[2]=Territoire
    

    index = 3

        
    #calcul des indices
        
  
    print(index)
    
            #two bands vegetation indices (normalized difference et simple ratio)
    
    for elt in itertools.permutations(listeBandes,2):
        bande1 = elt[0].split("_")[3]
        bande2 = elt[1].split("_")[3]
        
     
        with rasterio.open(repCourant+"/"+elt[0], "r") as src:
            ba = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
        with rasterio.open(repCourant+"/"+elt[1], "r") as src:
            bb = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')


        affine = src.transform

        ND =  np.divide((1.0*ba - bb), (ba + bb))
        ND[np.isinf(ND)] = np.nan
        double = tab['bandes']=="ND_"+bande1+"_"+bande2
        doubleInv = tab['bandes']=="ND_"+bande2+"_"+bande1
        if any(double) == False :
            if any(doubleInv)== False :
        #if not os.path.exists(dst_ND):
            #if not os.path.exists(dst_ND_inv): #on observe que a/b = 1/(b/a)
                ind = ['ND', "ND_"+bande1+"_"+bande2]
               
                
                
                stats = zonal_stats(TFEChemin, ND, stats = 'mean', affine=affine)
          
                val = []
                
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                
    

        SR = np.divide(ba, bb)
        SR[np.isinf(SR)] = np.nan
        double = tab['bandes']=="SR_"+bande1+"_"+bande2
        if any(double) == False:
                #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
         
            ind = ['SR', "SR_"+bande1+"_"+bande2]
        
            stats = zonal_stats(TFEChemin, SR, stats = 'mean', affine=affine)
          
            val = []
                
            for stat in range(len(stats)):
                val.append(stats[stat].get('mean'))
                
            concat = ind + val
                
            tab.loc[index]=concat
            
            index = index + 1
 
    print(index)

              # three bands vegetation indices (3BSI / mSR et 3BSI_Tian)
    for elt in itertools.permutations(listeBandes,3):
        bande1 = elt[0].split("_")[3]
        bande2 = elt[1].split("_")[3]
        bande3 = elt[2].split("_")[3]
 
        with rasterio.open(repCourant+"/"+elt[0], "r") as src:
            ba1 = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
        with rasterio.open(repCourant+"/"+elt[1], "r") as src:
            bb1 = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
        with rasterio.open(repCourant+"/"+elt[2], "r") as src:
            bc1 = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
            
        affine = src.transform
            
        BSI =  np.divide((1.0* ba1 - bc1), (bb1 + bc1))
        BSI[np.isinf(BSI)] = np.nan
        double = tab['bandes']=="BSI_"+bande1+"_"+bande2+"_"+bande3
        if any(double) == False:
                #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
         
            ind = ['BSI', "BSI_"+bande1+"_"+bande2+"_"+bande3]
        

            stats = zonal_stats(TFEChemin, BSI, stats = 'mean', affine=affine)
              
            val = []
                
            for stat in range(len(stats)):
                val.append(stats[stat].get('mean'))
                
            concat = ind + val
                
            tab.loc[index]=concat
            
            index = index + 1
            print(index)

        mSR =  np.divide((1.0* ba1 - bc1), (bb1 - bc1))
        mSR[np.isinf(mSR)] = np.nan
        double = tab['bandes']=="mSR_"+bande1+"_"+bande2+"_"+bande3
        doubleInv = tab['bandes']=="mSR_"+bande1+"_"+bande3+"_"+bande2
        if any(double) == False :
            if any(doubleInv)== False :
       
                ind = ['mSR', "mSR_"+bande1+"_"+bande2+"_"+bande3]
               
                stats = zonal_stats(TFEChemin, mSR, stats = 'mean', affine=affine)
              
                val = []
                    
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                print(index)

        BSI_Tian =  np.divide((1.0* ba1 - bb1 - bc1), (ba1 + bb1 + bc1))
        BSI_Tian[np.isinf(BSI_Tian)] = np.nan
        double = tab['bandes']=="BSITian_"+bande1+"_"+bande2+"_"+bande3
        doubleInv = tab['bandes']=="BSITian_"+bande1+"_"+bande3+"_"+bande2
        if any(double) == False :
            if any(doubleInv)== False :
                ind = ['BSITian', "BSITian_"+bande1+"_"+bande2+"_"+bande3]
               
                stats = zonal_stats(TFEChemin, BSI_Tian, stats = 'mean', affine=affine)
              
                val = []
                    
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                print(index)

        CVI =  np.multiply((ba1 / bc1), (bb1 / bc1))
        CVI[np.isinf(CVI)] = np.nan
        double = tab['bandes']=="CVI_"+bande1+"_"+bande2+"_"+bande3
        doubleInv = tab['bandes']=="CVI_"+bande1+"_"+bande3+"_"+bande2
        if any(double) == False :
            if any(doubleInv)== False :
       
                ind = ['CVI', "CVI_"+bande1+"_"+bande2+"_"+bande3]
               
                stats = zonal_stats(TFEChemin, CVI, stats = 'mean', affine=affine)
              
                val = []
                    
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                print(index)
    
    
    ###Création des indices usuels:
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
    
    affine = src.transform
  
 
#Calcul des indices classiques

 
#calcul du NDVI
    NDVI = np.divide((1.0*bandeB8 - bandeB4), (bandeB8 + bandeB4))
    NDVI[np.isinf(NDVI)]=np.nan
    double = tab['bandes']=="indclass_NDVI"
    if any(double) == False:
          #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
  
        ind = ['indclass', "indclass_NDVI"]
         
        stats = zonal_stats(TFEChemin, NDVI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du GNDVI
    GNDVI = np.divide((1.0*bandeB8 - bandeB3), (bandeB8 + bandeB3))
    GNDVI[np.isinf(GNDVI)]=np.nan
    double = tab['bandes']=="indclass_GNDVI"
    if any(double) == False:
                #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_GNDVI"]
        
        stats = zonal_stats(TFEChemin, GNDVI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1


 #calcul du NDVIre
    NDVIre = np.divide((1.0*bandeB8a - bandeB4), (bandeB8a + bandeB4))
    NDVIre[np.isinf(NDVIre)]=np.nan
    double = tab['bandes']=="indclass_NDVIre"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NDVIre"]
    
        stats = zonal_stats(TFEChemin, NDVIre, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NDI45
    NDI45 = np.divide((1.0*bandeB5 - bandeB4), (bandeB5 + bandeB4))
    NDI45[np.isinf(NDI45)]=np.nan
    double = tab['bandes']=="indclass_NDI45"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
  
        ind = ['indclass', "indclass_NDI45"]
        
        stats = zonal_stats(TFEChemin, NDI45, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NDII
    NDII = np.divide((1.0*bandeB8 - bandeB11), (bandeB8 + bandeB11))
    NDII[np.isinf(NDII)]=np.nan
    double = tab['bandes']=="indclass_NDII"
    if any(double) == False:
         #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
  
        ind = ['indclass', "indclass_NDII"]
        
        stats = zonal_stats(TFEChemin, NDII, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NREDI1
    NREDI1 = np.divide((1.0*bandeB6 - bandeB5), (bandeB6 + bandeB5))
    NREDI1[np.isinf(NREDI1)]=np.nan
    double = tab['bandes']=="indclass_NREDI1"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NREDI1"]
    
        stats = zonal_stats(TFEChemin, NREDI1, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NREDI2
    NREDI2 = np.divide((1.0*bandeB7 - bandeB5), (bandeB7 + bandeB5))
    NREDI2[np.isinf(NREDI2)]=np.nan
    double = tab['bandes']=="indclass_NREDI2"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NREDI2"]
    
        stats = zonal_stats(TFEChemin, NREDI2, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NREDI3
    NREDI3 = np.divide((1.0*bandeB7 - bandeB6), (bandeB7 + bandeB6))
    NREDI3[np.isinf(NREDI3)]=np.nan
    double = tab['bandes']=="indclass_NREDI3"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NREDI3"]
    
        stats = zonal_stats(TFEChemin, NREDI3, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du PSRI
    PSRI = np.divide((1.0*bandeB4 - bandeB3), (bandeB5))
    PSRI[np.isinf(PSRI)]=np.nan
    double = tab['bandes']=="indclass_PSRI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_PSRI"]
    
        stats = zonal_stats(TFEChemin, PSRI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du MSI
    MSI = np.divide((1.0*bandeB11), (bandeB8))
    MSI[np.isinf(MSI)]=np.nan
    double = tab['bandes']=="indclass_MSI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_MSI"]
    
        stats = zonal_stats(TFEChemin, MSI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du IRECI
    IRECI = np.divide((1.0*bandeB7 - bandeB4), (np.divide(1.0*bandeB5 , bandeB6)))
    IRECI[np.isinf(IRECI)]=np.nan
    double = tab['bandes']=="indclass_IRECI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_IRECI"]
    
        stats = zonal_stats(TFEChemin, IRECI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du MTCI
    MTCI = np.divide((1.0*bandeB8 - bandeB5), (bandeB5 - bandeB4))
    MTCI[np.isinf(MTCI)]=np.nan
    double = tab['bandes']=="indclass_MTCI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_MTCI"]
    
        stats = zonal_stats(TFEChemin, MTCI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du MCARI
    MCARI = np.multiply(((bandeB5 - bandeB4) - (0.2*(bandeB5 - bandeB3))), (bandeB5 - bandeB4))
    MCARI[np.isinf(MCARI)]=np.nan
    double = tab['bandes']=="indclass_MCARI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_MCARI"]
    
        stats = zonal_stats(TFEChemin, MCARI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1
     

    print(index)

    tab.to_csv(os.path.join(repSortieDate,nomSortieTab))
    

####################
####################
### Tuile 32TLP ####
####################
####################

 
 
repDonnees = r"../applicationMasque/sortie/sortieT32TLP"
repSortie = "sortie/sortieT32TLP"


listeRep = os.listdir(repDonnees)

#ouvrir les TFE

TFEChemin = "TFE/polygones_T32TLP.shp"    
TFE = gpd.read_file(TFEChemin)


#stats = zonal_stats(TFE2,repCourant+"/"+B2[0], stats = 'mean')
        
        
for i in range (len(listeRep)):
    repCourant = os.path.join(repDonnees, listeRep[i])#se positionner dans le répertoire d'une date
    fichiersRep = os.listdir(repCourant)#lister les fichiers à savoir les différentes bandes
    
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
    
    repSortieDate = os.path.join(repSortie, listeRep[i]) 
    if not os.path.exists(repSortieDate):
        os.makedirs(repSortieDate)
    
     

    legende = ["indices","bandes"]
    entites = len(TFE)
    for entite in range(1,entites+1):
        legende.append(entite)
 
    
    Typo_AS = ["/","/"]
    for typoas in range(len(TFE.typo_AS)):
        Typo_AS.append(TFE.typo_AS[typoas])
    
    Territoire = ["/","/"]
    for territoire in range(len(TFE.territoire)):
        Territoire.append(TFE.territoire[territoire])

   #creation du tableau
    
    tab = pd.DataFrame(columns = legende)
    tab.loc[1]=Typo_AS
    tab.loc[2]=Territoire
    

    index = 3

        
    #calcul des indices
        
  
    print(index)
    
            #two bands vegetation indices (normalized difference et simple ratio)
    
    for elt in itertools.permutations(listeBandes,2):
        bande1 = elt[0].split("_")[3]
        bande2 = elt[1].split("_")[3]
        
     
        with rasterio.open(repCourant+"/"+elt[0], "r") as src:
            ba = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
        with rasterio.open(repCourant+"/"+elt[1], "r") as src:
            bb = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')


        affine = src.transform

        ND =  np.divide((1.0*ba - bb), (ba + bb))
        ND[np.isinf(ND)] = np.nan
        double = tab['bandes']=="ND_"+bande1+"_"+bande2
        doubleInv = tab['bandes']=="ND_"+bande2+"_"+bande1
        if any(double) == False :
            if any(doubleInv)== False :
        #if not os.path.exists(dst_ND):
            #if not os.path.exists(dst_ND_inv): #on observe que a/b = 1/(b/a)
                ind = ['ND', "ND_"+bande1+"_"+bande2]
               
                
                
                stats = zonal_stats(TFEChemin, ND, stats = 'mean', affine=affine)
          
                val = []
                
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                
    

        SR = np.divide(ba, bb)
        SR[np.isinf(SR)] = np.nan
        double = tab['bandes']=="SR_"+bande1+"_"+bande2
        if any(double) == False:
                #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
         
            ind = ['SR', "SR_"+bande1+"_"+bande2]
        
            stats = zonal_stats(TFEChemin, SR, stats = 'mean', affine=affine)
          
            val = []
                
            for stat in range(len(stats)):
                val.append(stats[stat].get('mean'))
                
            concat = ind + val
                
            tab.loc[index]=concat
            
            index = index + 1
 
    print(index)

              # three bands vegetation indices (3BSI / mSR et 3BSI_Tian)
    for elt in itertools.permutations(listeBandes,3):
        bande1 = elt[0].split("_")[3]
        bande2 = elt[1].split("_")[3]
        bande3 = elt[2].split("_")[3]
 
        with rasterio.open(repCourant+"/"+elt[0], "r") as src:
            ba1 = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
        with rasterio.open(repCourant+"/"+elt[1], "r") as src:
            bb1 = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
        with rasterio.open(repCourant+"/"+elt[2], "r") as src:
            bc1 = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
            
        affine = src.transform
            
        BSI =  np.divide((1.0* ba1 - bc1), (bb1 + bc1))
        BSI[np.isinf(BSI)] = np.nan
        double = tab['bandes']=="BSI_"+bande1+"_"+bande2+"_"+bande3
        if any(double) == False:
                #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
         
            ind = ['BSI', "BSI_"+bande1+"_"+bande2+"_"+bande3]
        

            stats = zonal_stats(TFEChemin, BSI, stats = 'mean', affine=affine)
              
            val = []
                
            for stat in range(len(stats)):
                val.append(stats[stat].get('mean'))
                
            concat = ind + val
                
            tab.loc[index]=concat
            
            index = index + 1
            print(index)

        mSR =  np.divide((1.0* ba1 - bc1), (bb1 - bc1))
        mSR[np.isinf(mSR)] = np.nan
        double = tab['bandes']=="mSR_"+bande1+"_"+bande2+"_"+bande3
        doubleInv = tab['bandes']=="mSR_"+bande1+"_"+bande3+"_"+bande2
        if any(double) == False :
            if any(doubleInv)== False :
       
                ind = ['mSR', "mSR_"+bande1+"_"+bande2+"_"+bande3]
               
                stats = zonal_stats(TFEChemin, mSR, stats = 'mean', affine=affine)
              
                val = []
                    
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                print(index)

        BSI_Tian =  np.divide((1.0* ba1 - bb1 - bc1), (ba1 + bb1 + bc1))
        BSI_Tian[np.isinf(BSI_Tian)] = np.nan
        double = tab['bandes']=="BSITian_"+bande1+"_"+bande2+"_"+bande3
        doubleInv = tab['bandes']=="BSITian_"+bande1+"_"+bande3+"_"+bande2
        if any(double) == False :
            if any(doubleInv)== False :
                ind = ['BSITian', "BSITian_"+bande1+"_"+bande2+"_"+bande3]
               
                stats = zonal_stats(TFEChemin, BSI_Tian, stats = 'mean', affine=affine)
              
                val = []
                    
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                print(index)

        CVI =  np.multiply((ba1 / bc1), (bb1 / bc1))
        CVI[np.isinf(CVI)] = np.nan
        double = tab['bandes']=="CVI_"+bande1+"_"+bande2+"_"+bande3
        doubleInv = tab['bandes']=="CVI_"+bande1+"_"+bande3+"_"+bande2
        if any(double) == False :
            if any(doubleInv)== False :
       
                ind = ['CVI', "CVI_"+bande1+"_"+bande2+"_"+bande3]
               
                stats = zonal_stats(TFEChemin, CVI, stats = 'mean', affine=affine)
              
                val = []
                    
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                print(index)
    
    
    ###Création des indices usuels:
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
    
    affine = src.transform
  
 
#Calcul des indices classiques

 
#calcul du NDVI
    NDVI = np.divide((1.0*bandeB8 - bandeB4), (bandeB8 + bandeB4))
    NDVI[np.isinf(NDVI)]=np.nan
    double = tab['bandes']=="indclass_NDVI"
    if any(double) == False:
          #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
  
        ind = ['indclass', "indclass_NDVI"]
         
        stats = zonal_stats(TFEChemin, NDVI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du GNDVI
    GNDVI = np.divide((1.0*bandeB8 - bandeB3), (bandeB8 + bandeB3))
    GNDVI[np.isinf(GNDVI)]=np.nan
    double = tab['bandes']=="indclass_GNDVI"
    if any(double) == False:
                #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_GNDVI"]
        
        stats = zonal_stats(TFEChemin, GNDVI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1


 #calcul du NDVIre
    NDVIre = np.divide((1.0*bandeB8a - bandeB4), (bandeB8a + bandeB4))
    NDVIre[np.isinf(NDVIre)]=np.nan
    double = tab['bandes']=="indclass_NDVIre"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NDVIre"]
    
        stats = zonal_stats(TFEChemin, NDVIre, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NDI45
    NDI45 = np.divide((1.0*bandeB5 - bandeB4), (bandeB5 + bandeB4))
    NDI45[np.isinf(NDI45)]=np.nan
    double = tab['bandes']=="indclass_NDI45"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
  
        ind = ['indclass', "indclass_NDI45"]
        
        stats = zonal_stats(TFEChemin, NDI45, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NDII
    NDII = np.divide((1.0*bandeB8 - bandeB11), (bandeB8 + bandeB11))
    NDII[np.isinf(NDII)]=np.nan
    double = tab['bandes']=="indclass_NDII"
    if any(double) == False:
         #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
  
        ind = ['indclass', "indclass_NDII"]
        
        stats = zonal_stats(TFEChemin, NDII, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NREDI1
    NREDI1 = np.divide((1.0*bandeB6 - bandeB5), (bandeB6 + bandeB5))
    NREDI1[np.isinf(NREDI1)]=np.nan
    double = tab['bandes']=="indclass_NREDI1"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NREDI1"]
    
        stats = zonal_stats(TFEChemin, NREDI1, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NREDI2
    NREDI2 = np.divide((1.0*bandeB7 - bandeB5), (bandeB7 + bandeB5))
    NREDI2[np.isinf(NREDI2)]=np.nan
    double = tab['bandes']=="indclass_NREDI2"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NREDI2"]
    
        stats = zonal_stats(TFEChemin, NREDI2, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NREDI3
    NREDI3 = np.divide((1.0*bandeB7 - bandeB6), (bandeB7 + bandeB6))
    NREDI3[np.isinf(NREDI3)]=np.nan
    double = tab['bandes']=="indclass_NREDI3"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NREDI3"]
    
        stats = zonal_stats(TFEChemin, NREDI3, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du PSRI
    PSRI = np.divide((1.0*bandeB4 - bandeB3), (bandeB5))
    PSRI[np.isinf(PSRI)]=np.nan
    double = tab['bandes']=="indclass_PSRI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_PSRI"]
    
        stats = zonal_stats(TFEChemin, PSRI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du MSI
    MSI = np.divide((1.0*bandeB11), (bandeB8))
    MSI[np.isinf(MSI)]=np.nan
    double = tab['bandes']=="indclass_MSI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_MSI"]
    
        stats = zonal_stats(TFEChemin, MSI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du IRECI
    IRECI = np.divide((1.0*bandeB7 - bandeB4), (np.divide(1.0*bandeB5 , bandeB6)))
    IRECI[np.isinf(IRECI)]=np.nan
    double = tab['bandes']=="indclass_IRECI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_IRECI"]
    
        stats = zonal_stats(TFEChemin, IRECI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du MTCI
    MTCI = np.divide((1.0*bandeB8 - bandeB5), (bandeB5 - bandeB4))
    MTCI[np.isinf(MTCI)]=np.nan
    double = tab['bandes']=="indclass_MTCI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_MTCI"]
    
        stats = zonal_stats(TFEChemin, MTCI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du MCARI
    MCARI = np.multiply(((bandeB5 - bandeB4) - (0.2*(bandeB5 - bandeB3))), (bandeB5 - bandeB4))
    MCARI[np.isinf(MCARI)]=np.nan
    double = tab['bandes']=="indclass_MCARI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_MCARI"]
    
        stats = zonal_stats(TFEChemin, MCARI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1
     

    print(index)

    tab.to_csv(os.path.join(repSortieDate,nomSortieTab))
    
    
####################
####################
### Tuile 32TLQ ####
####################
####################

 
 
repDonnees = r"../applicationMasque/sortie/sortieT32TLQ"
repSortie = "sortie/sortieT32TLQ"


listeRep = os.listdir(repDonnees)

#ouvrir les TFE

TFEChemin = "TFE/polygones_T32TLQ.shp"    
TFE = gpd.read_file(TFEChemin)


#stats = zonal_stats(TFE2,repCourant+"/"+B2[0], stats = 'mean')
        
        
for i in range (len(listeRep)):
    repCourant = os.path.join(repDonnees, listeRep[i])#se positionner dans le répertoire d'une date
    fichiersRep = os.listdir(repCourant)#lister les fichiers à savoir les différentes bandes
    
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
    
    repSortieDate = os.path.join(repSortie, listeRep[i]) 
    if not os.path.exists(repSortieDate):
        os.makedirs(repSortieDate)
    
     

    legende = ["indices","bandes"]
    entites = len(TFE)
    for entite in range(1,entites+1):
        legende.append(entite)
 
    
    Typo_AS = ["/","/"]
    for typoas in range(len(TFE.typo_AS)):
        Typo_AS.append(TFE.typo_AS[typoas])
    
    Territoire = ["/","/"]
    for territoire in range(len(TFE.territoire)):
        Territoire.append(TFE.territoire[territoire])

   #creation du tableau
    
    tab = pd.DataFrame(columns = legende)
    tab.loc[1]=Typo_AS
    tab.loc[2]=Territoire
    

    index = 3

        
    #calcul des indices
        
  
    print(index)
    
            #two bands vegetation indices (normalized difference et simple ratio)
    
    for elt in itertools.permutations(listeBandes,2):
        bande1 = elt[0].split("_")[3]
        bande2 = elt[1].split("_")[3]
        
     
        with rasterio.open(repCourant+"/"+elt[0], "r") as src:
            ba = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
        with rasterio.open(repCourant+"/"+elt[1], "r") as src:
            bb = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')


        affine = src.transform

        ND =  np.divide((1.0*ba - bb), (ba + bb))
        ND[np.isinf(ND)] = np.nan
        double = tab['bandes']=="ND_"+bande1+"_"+bande2
        doubleInv = tab['bandes']=="ND_"+bande2+"_"+bande1
        if any(double) == False :
            if any(doubleInv)== False :
        #if not os.path.exists(dst_ND):
            #if not os.path.exists(dst_ND_inv): #on observe que a/b = 1/(b/a)
                ind = ['ND', "ND_"+bande1+"_"+bande2]
               
                
                
                stats = zonal_stats(TFEChemin, ND, stats = 'mean', affine=affine)
          
                val = []
                
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                
    

        SR = np.divide(ba, bb)
        SR[np.isinf(SR)] = np.nan
        double = tab['bandes']=="SR_"+bande1+"_"+bande2
        if any(double) == False:
                #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
         
            ind = ['SR', "SR_"+bande1+"_"+bande2]
        
            stats = zonal_stats(TFEChemin, SR, stats = 'mean', affine=affine)
          
            val = []
                
            for stat in range(len(stats)):
                val.append(stats[stat].get('mean'))
                
            concat = ind + val
                
            tab.loc[index]=concat
            
            index = index + 1
 
    print(index)

              # three bands vegetation indices (3BSI / mSR et 3BSI_Tian)
    for elt in itertools.permutations(listeBandes,3):
        bande1 = elt[0].split("_")[3]
        bande2 = elt[1].split("_")[3]
        bande3 = elt[2].split("_")[3]
 
        with rasterio.open(repCourant+"/"+elt[0], "r") as src:
            ba1 = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
        with rasterio.open(repCourant+"/"+elt[1], "r") as src:
            bb1 = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
        with rasterio.open(repCourant+"/"+elt[2], "r") as src:
            bc1 = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
            
        affine = src.transform
            
        BSI =  np.divide((1.0* ba1 - bc1), (bb1 + bc1))
        BSI[np.isinf(BSI)] = np.nan
        double = tab['bandes']=="BSI_"+bande1+"_"+bande2+"_"+bande3
        if any(double) == False:
                #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
         
            ind = ['BSI', "BSI_"+bande1+"_"+bande2+"_"+bande3]
        

            stats = zonal_stats(TFEChemin, BSI, stats = 'mean', affine=affine)
              
            val = []
                
            for stat in range(len(stats)):
                val.append(stats[stat].get('mean'))
                
            concat = ind + val
                
            tab.loc[index]=concat
            
            index = index + 1
            print(index)

        mSR =  np.divide((1.0* ba1 - bc1), (bb1 - bc1))
        mSR[np.isinf(mSR)] = np.nan
        double = tab['bandes']=="mSR_"+bande1+"_"+bande2+"_"+bande3
        doubleInv = tab['bandes']=="mSR_"+bande1+"_"+bande3+"_"+bande2
        if any(double) == False :
            if any(doubleInv)== False :
       
                ind = ['mSR', "mSR_"+bande1+"_"+bande2+"_"+bande3]
               
                stats = zonal_stats(TFEChemin, mSR, stats = 'mean', affine=affine)
              
                val = []
                    
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                print(index)

        BSI_Tian =  np.divide((1.0* ba1 - bb1 - bc1), (ba1 + bb1 + bc1))
        BSI_Tian[np.isinf(BSI_Tian)] = np.nan
        double = tab['bandes']=="BSITian_"+bande1+"_"+bande2+"_"+bande3
        doubleInv = tab['bandes']=="BSITian_"+bande1+"_"+bande3+"_"+bande2
        if any(double) == False :
            if any(doubleInv)== False :
                ind = ['BSITian', "BSITian_"+bande1+"_"+bande2+"_"+bande3]
               
                stats = zonal_stats(TFEChemin, BSI_Tian, stats = 'mean', affine=affine)
              
                val = []
                    
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                print(index)

        CVI =  np.multiply((ba1 / bc1), (bb1 / bc1))
        CVI[np.isinf(CVI)] = np.nan
        double = tab['bandes']=="CVI_"+bande1+"_"+bande2+"_"+bande3
        doubleInv = tab['bandes']=="CVI_"+bande1+"_"+bande3+"_"+bande2
        if any(double) == False :
            if any(doubleInv)== False :
       
                ind = ['CVI', "CVI_"+bande1+"_"+bande2+"_"+bande3]
               
                stats = zonal_stats(TFEChemin, CVI, stats = 'mean', affine=affine)
              
                val = []
                    
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                print(index)
    
    
    ###Création des indices usuels:
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
    
    affine = src.transform
  
 
#Calcul des indices classiques

 
#calcul du NDVI
    NDVI = np.divide((1.0*bandeB8 - bandeB4), (bandeB8 + bandeB4))
    NDVI[np.isinf(NDVI)]=np.nan
    double = tab['bandes']=="indclass_NDVI"
    if any(double) == False:
          #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
  
        ind = ['indclass', "indclass_NDVI"]
         
        stats = zonal_stats(TFEChemin, NDVI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du GNDVI
    GNDVI = np.divide((1.0*bandeB8 - bandeB3), (bandeB8 + bandeB3))
    GNDVI[np.isinf(GNDVI)]=np.nan
    double = tab['bandes']=="indclass_GNDVI"
    if any(double) == False:
                #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_GNDVI"]
        
        stats = zonal_stats(TFEChemin, GNDVI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1


 #calcul du NDVIre
    NDVIre = np.divide((1.0*bandeB8a - bandeB4), (bandeB8a + bandeB4))
    NDVIre[np.isinf(NDVIre)]=np.nan
    double = tab['bandes']=="indclass_NDVIre"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NDVIre"]
    
        stats = zonal_stats(TFEChemin, NDVIre, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NDI45
    NDI45 = np.divide((1.0*bandeB5 - bandeB4), (bandeB5 + bandeB4))
    NDI45[np.isinf(NDI45)]=np.nan
    double = tab['bandes']=="indclass_NDI45"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
  
        ind = ['indclass', "indclass_NDI45"]
        
        stats = zonal_stats(TFEChemin, NDI45, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NDII
    NDII = np.divide((1.0*bandeB8 - bandeB11), (bandeB8 + bandeB11))
    NDII[np.isinf(NDII)]=np.nan
    double = tab['bandes']=="indclass_NDII"
    if any(double) == False:
         #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
  
        ind = ['indclass', "indclass_NDII"]
        
        stats = zonal_stats(TFEChemin, NDII, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NREDI1
    NREDI1 = np.divide((1.0*bandeB6 - bandeB5), (bandeB6 + bandeB5))
    NREDI1[np.isinf(NREDI1)]=np.nan
    double = tab['bandes']=="indclass_NREDI1"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NREDI1"]
    
        stats = zonal_stats(TFEChemin, NREDI1, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NREDI2
    NREDI2 = np.divide((1.0*bandeB7 - bandeB5), (bandeB7 + bandeB5))
    NREDI2[np.isinf(NREDI2)]=np.nan
    double = tab['bandes']=="indclass_NREDI2"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NREDI2"]
    
        stats = zonal_stats(TFEChemin, NREDI2, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NREDI3
    NREDI3 = np.divide((1.0*bandeB7 - bandeB6), (bandeB7 + bandeB6))
    NREDI3[np.isinf(NREDI3)]=np.nan
    double = tab['bandes']=="indclass_NREDI3"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NREDI3"]
    
        stats = zonal_stats(TFEChemin, NREDI3, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du PSRI
    PSRI = np.divide((1.0*bandeB4 - bandeB3), (bandeB5))
    PSRI[np.isinf(PSRI)]=np.nan
    double = tab['bandes']=="indclass_PSRI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_PSRI"]
    
        stats = zonal_stats(TFEChemin, PSRI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du MSI
    MSI = np.divide((1.0*bandeB11), (bandeB8))
    MSI[np.isinf(MSI)]=np.nan
    double = tab['bandes']=="indclass_MSI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_MSI"]
    
        stats = zonal_stats(TFEChemin, MSI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du IRECI
    IRECI = np.divide((1.0*bandeB7 - bandeB4), (np.divide(1.0*bandeB5 , bandeB6)))
    IRECI[np.isinf(IRECI)]=np.nan
    double = tab['bandes']=="indclass_IRECI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_IRECI"]
    
        stats = zonal_stats(TFEChemin, IRECI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du MTCI
    MTCI = np.divide((1.0*bandeB8 - bandeB5), (bandeB5 - bandeB4))
    MTCI[np.isinf(MTCI)]=np.nan
    double = tab['bandes']=="indclass_MTCI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_MTCI"]
    
        stats = zonal_stats(TFEChemin, MTCI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du MCARI
    MCARI = np.multiply(((bandeB5 - bandeB4) - (0.2*(bandeB5 - bandeB3))), (bandeB5 - bandeB4))
    MCARI[np.isinf(MCARI)]=np.nan
    double = tab['bandes']=="indclass_MCARI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_MCARI"]
    
        stats = zonal_stats(TFEChemin, MCARI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1
     

    print(index)

    tab.to_csv(os.path.join(repSortieDate,nomSortieTab))
    
    
####################
####################
### Tuile 32TLR ####
####################
####################

 
 
repDonnees = r"../applicationMasque/sortie/sortieT32TLR"
repSortie = "sortie/sortieT32TLR"


listeRep = os.listdir(repDonnees)

#ouvrir les TFE

TFEChemin = "TFE/polygones_T32TLR.shp"    
TFE = gpd.read_file(TFEChemin)


#stats = zonal_stats(TFE2,repCourant+"/"+B2[0], stats = 'mean')
        
        
for i in range (len(listeRep)):
    repCourant = os.path.join(repDonnees, listeRep[i])#se positionner dans le répertoire d'une date
    fichiersRep = os.listdir(repCourant)#lister les fichiers à savoir les différentes bandes
    
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
    
    repSortieDate = os.path.join(repSortie, listeRep[i]) 
    if not os.path.exists(repSortieDate):
        os.makedirs(repSortieDate)
    
     

    legende = ["indices","bandes"]
    entites = len(TFE)
    for entite in range(1,entites+1):
        legende.append(entite)
 
    
    Typo_AS = ["/","/"]
    for typoas in range(len(TFE.typo_AS)):
        Typo_AS.append(TFE.typo_AS[typoas])
    
    Territoire = ["/","/"]
    for territoire in range(len(TFE.territoire)):
        Territoire.append(TFE.territoire[territoire])

   #creation du tableau
    
    tab = pd.DataFrame(columns = legende)
    tab.loc[1]=Typo_AS
    tab.loc[2]=Territoire
    

    index = 3

        
    #calcul des indices
        
  
    print(index)
    
            #two bands vegetation indices (normalized difference et simple ratio)
    
    for elt in itertools.permutations(listeBandes,2):
        bande1 = elt[0].split("_")[3]
        bande2 = elt[1].split("_")[3]
        
     
        with rasterio.open(repCourant+"/"+elt[0], "r") as src:
            ba = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
        with rasterio.open(repCourant+"/"+elt[1], "r") as src:
            bb = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')


        affine = src.transform

        ND =  np.divide((1.0*ba - bb), (ba + bb))
        ND[np.isinf(ND)] = np.nan
        double = tab['bandes']=="ND_"+bande1+"_"+bande2
        doubleInv = tab['bandes']=="ND_"+bande2+"_"+bande1
        if any(double) == False :
            if any(doubleInv)== False :
        #if not os.path.exists(dst_ND):
            #if not os.path.exists(dst_ND_inv): #on observe que a/b = 1/(b/a)
                ind = ['ND', "ND_"+bande1+"_"+bande2]
               
                
                
                stats = zonal_stats(TFEChemin, ND, stats = 'mean', affine=affine)
          
                val = []
                
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                
    

        SR = np.divide(ba, bb)
        SR[np.isinf(SR)] = np.nan
        double = tab['bandes']=="SR_"+bande1+"_"+bande2
        if any(double) == False:
                #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
         
            ind = ['SR', "SR_"+bande1+"_"+bande2]
        
            stats = zonal_stats(TFEChemin, SR, stats = 'mean', affine=affine)
          
            val = []
                
            for stat in range(len(stats)):
                val.append(stats[stat].get('mean'))
                
            concat = ind + val
                
            tab.loc[index]=concat
            
            index = index + 1
 
    print(index)

              # three bands vegetation indices (3BSI / mSR et 3BSI_Tian)
    for elt in itertools.permutations(listeBandes,3):
        bande1 = elt[0].split("_")[3]
        bande2 = elt[1].split("_")[3]
        bande3 = elt[2].split("_")[3]
 
        with rasterio.open(repCourant+"/"+elt[0], "r") as src:
            ba1 = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
        with rasterio.open(repCourant+"/"+elt[1], "r") as src:
            bb1 = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
        with rasterio.open(repCourant+"/"+elt[2], "r") as src:
            bc1 = src.read(1)
            profile = src.profile
            profile.update(
                    dtype=rasterio.float64,
                    count=1,
                    compress='lzw')
            
        affine = src.transform
            
        BSI =  np.divide((1.0* ba1 - bc1), (bb1 + bc1))
        BSI[np.isinf(BSI)] = np.nan
        double = tab['bandes']=="BSI_"+bande1+"_"+bande2+"_"+bande3
        if any(double) == False:
                #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
         
            ind = ['BSI', "BSI_"+bande1+"_"+bande2+"_"+bande3]
        

            stats = zonal_stats(TFEChemin, BSI, stats = 'mean', affine=affine)
              
            val = []
                
            for stat in range(len(stats)):
                val.append(stats[stat].get('mean'))
                
            concat = ind + val
                
            tab.loc[index]=concat
            
            index = index + 1
            print(index)

        mSR =  np.divide((1.0* ba1 - bc1), (bb1 - bc1))
        mSR[np.isinf(mSR)] = np.nan
        double = tab['bandes']=="mSR_"+bande1+"_"+bande2+"_"+bande3
        doubleInv = tab['bandes']=="mSR_"+bande1+"_"+bande3+"_"+bande2
        if any(double) == False :
            if any(doubleInv)== False :
       
                ind = ['mSR', "mSR_"+bande1+"_"+bande2+"_"+bande3]
               
                stats = zonal_stats(TFEChemin, mSR, stats = 'mean', affine=affine)
              
                val = []
                    
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                print(index)

        BSI_Tian =  np.divide((1.0* ba1 - bb1 - bc1), (ba1 + bb1 + bc1))
        BSI_Tian[np.isinf(BSI_Tian)] = np.nan
        double = tab['bandes']=="BSITian_"+bande1+"_"+bande2+"_"+bande3
        doubleInv = tab['bandes']=="BSITian_"+bande1+"_"+bande3+"_"+bande2
        if any(double) == False :
            if any(doubleInv)== False :
                ind = ['BSITian', "BSITian_"+bande1+"_"+bande2+"_"+bande3]
               
                stats = zonal_stats(TFEChemin, BSI_Tian, stats = 'mean', affine=affine)
              
                val = []
                    
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                print(index)

        CVI =  np.multiply((ba1 / bc1), (bb1 / bc1))
        CVI[np.isinf(CVI)] = np.nan
        double = tab['bandes']=="CVI_"+bande1+"_"+bande2+"_"+bande3
        doubleInv = tab['bandes']=="CVI_"+bande1+"_"+bande3+"_"+bande2
        if any(double) == False :
            if any(doubleInv)== False :
       
                ind = ['CVI', "CVI_"+bande1+"_"+bande2+"_"+bande3]
               
                stats = zonal_stats(TFEChemin, CVI, stats = 'mean', affine=affine)
              
                val = []
                    
                for stat in range(len(stats)):
                    val.append(stats[stat].get('mean'))
                    
                concat = ind + val
                    
                tab.loc[index]=concat
                
                index = index + 1
                print(index)
    
    
    ###Création des indices usuels:
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
    
    affine = src.transform
  
 
#Calcul des indices classiques

 
#calcul du NDVI
    NDVI = np.divide((1.0*bandeB8 - bandeB4), (bandeB8 + bandeB4))
    NDVI[np.isinf(NDVI)]=np.nan
    double = tab['bandes']=="indclass_NDVI"
    if any(double) == False:
          #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
  
        ind = ['indclass', "indclass_NDVI"]
         
        stats = zonal_stats(TFEChemin, NDVI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du GNDVI
    GNDVI = np.divide((1.0*bandeB8 - bandeB3), (bandeB8 + bandeB3))
    GNDVI[np.isinf(GNDVI)]=np.nan
    double = tab['bandes']=="indclass_GNDVI"
    if any(double) == False:
                #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_GNDVI"]
        
        stats = zonal_stats(TFEChemin, GNDVI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1


 #calcul du NDVIre
    NDVIre = np.divide((1.0*bandeB8a - bandeB4), (bandeB8a + bandeB4))
    NDVIre[np.isinf(NDVIre)]=np.nan
    double = tab['bandes']=="indclass_NDVIre"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NDVIre"]
    
        stats = zonal_stats(TFEChemin, NDVIre, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NDI45
    NDI45 = np.divide((1.0*bandeB5 - bandeB4), (bandeB5 + bandeB4))
    NDI45[np.isinf(NDI45)]=np.nan
    double = tab['bandes']=="indclass_NDI45"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
  
        ind = ['indclass', "indclass_NDI45"]
        
        stats = zonal_stats(TFEChemin, NDI45, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NDII
    NDII = np.divide((1.0*bandeB8 - bandeB11), (bandeB8 + bandeB11))
    NDII[np.isinf(NDII)]=np.nan
    double = tab['bandes']=="indclass_NDII"
    if any(double) == False:
         #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
  
        ind = ['indclass', "indclass_NDII"]
        
        stats = zonal_stats(TFEChemin, NDII, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NREDI1
    NREDI1 = np.divide((1.0*bandeB6 - bandeB5), (bandeB6 + bandeB5))
    NREDI1[np.isinf(NREDI1)]=np.nan
    double = tab['bandes']=="indclass_NREDI1"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NREDI1"]
    
        stats = zonal_stats(TFEChemin, NREDI1, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NREDI2
    NREDI2 = np.divide((1.0*bandeB7 - bandeB5), (bandeB7 + bandeB5))
    NREDI2[np.isinf(NREDI2)]=np.nan
    double = tab['bandes']=="indclass_NREDI2"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NREDI2"]
    
        stats = zonal_stats(TFEChemin, NREDI2, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du NREDI3
    NREDI3 = np.divide((1.0*bandeB7 - bandeB6), (bandeB7 + bandeB6))
    NREDI3[np.isinf(NREDI3)]=np.nan
    double = tab['bandes']=="indclass_NREDI3"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_NREDI3"]
    
        stats = zonal_stats(TFEChemin, NREDI3, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du PSRI
    PSRI = np.divide((1.0*bandeB4 - bandeB3), (bandeB5))
    PSRI[np.isinf(PSRI)]=np.nan
    double = tab['bandes']=="indclass_PSRI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_PSRI"]
    
        stats = zonal_stats(TFEChemin, PSRI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du MSI
    MSI = np.divide((1.0*bandeB11), (bandeB8))
    MSI[np.isinf(MSI)]=np.nan
    double = tab['bandes']=="indclass_MSI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_MSI"]
    
        stats = zonal_stats(TFEChemin, MSI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du IRECI
    IRECI = np.divide((1.0*bandeB7 - bandeB4), (np.divide(1.0*bandeB5 , bandeB6)))
    IRECI[np.isinf(IRECI)]=np.nan
    double = tab['bandes']=="indclass_IRECI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_IRECI"]
    
        stats = zonal_stats(TFEChemin, IRECI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du MTCI
    MTCI = np.divide((1.0*bandeB8 - bandeB5), (bandeB5 - bandeB4))
    MTCI[np.isinf(MTCI)]=np.nan
    double = tab['bandes']=="indclass_MTCI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_MTCI"]
    
        stats = zonal_stats(TFEChemin, MTCI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1

 #calcul du MCARI
    MCARI = np.multiply(((bandeB5 - bandeB4) - (0.2*(bandeB5 - bandeB3))), (bandeB5 - bandeB4))
    MCARI[np.isinf(MCARI)]=np.nan
    double = tab['bandes']=="indclass_MCARI"
    if any(double) == False:
            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
     
        ind = ['indclass', "indclass_MCARI"]
    
        stats = zonal_stats(TFEChemin, MCARI, stats = 'mean', affine=affine)
              
        val = []
            
        for stat in range(len(stats)):
            val.append(stats[stat].get('mean'))
            
        concat = ind + val
            
        tab.loc[index]=concat
        
        index = index + 1
     

    print(index)

    tab.to_csv(os.path.join(repSortieDate,nomSortieTab))