#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 14:19:07 2021

@author: Emilie SIROT
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

 
 
repDonnees = r"../applicationMasque/sortie/sortieT31TFJ"
repSortie = "sortie/sortieT31TFJ"


listeRep = os.listdir(repDonnees)

#ouvrir les TFE

TFEChemin = "TFE/tfe_bio_T31TFJ_WGS84.shp"    
TFE = gpd.read_file(TFEChemin) #ouverture du shp
     
gidTFE = ["indices","bandes"]
for gid in range(len(TFE.gid)):
    gidTFE.append(TFE.gid[gid])


listeCoordonnees = []
     
for j in range(len(TFE)):
    x = TFE.iloc[j].geometry.centroid.x #récupère les coordonnées d'un point
    y = TFE.iloc[j].geometry.centroid.y
     
    listeCoordonnees.append((x,y))
        
        
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
    
    
    #caracteristiques de l'image
    
                   
    imageRef = gdal.Open(repCourant+'/'+B2[0])
    # bandImageRef = imageRef.GetRasterBand(1)       
    cols = imageRef.RasterXSize
    rows = imageRef.RasterYSize
    transform = imageRef.GetGeoTransform()
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = -transform[5]
    

    #creation du tableau
    
    tab = pd.DataFrame(columns = gidTFE)


        
    #calcul des indices
        
    
    
    indices=["3BSI","3BSITian","CVI","mSR","ND","SR","indclass"]
    for (path,dirs,files) in os.walk(repDonnees):
        for dir in dirs:
            for indice in indices:
                if not os.path.exists(os.path.join(repSortie,dir,indice)):
                    os.makedirs(os.path.join(repSortie,dir,indice))


            #two bands vegetation indices (normalized difference et simple ratio)
            #for index in range(135):
            for elt in itertools.permutations(listeBandes,2):
                bande1 = elt[0].split("_")[3]
                bande2 = elt[1].split("_")[3]
                ND_of = "%s_%s_ND_%s.tif" % (bande1, bande2, date )
                ND_of_inv="%s_%s_ND_%s.tif" % (bande2, bande1, date )
                SR_of = "%s_%s_SR_%s.tif" % (bande1, bande2, date )
                # SR_of_inv="%s_%s_SR_%s.tif" % (bande2, bande1, x )
                dst_ND=os.path.join(repSortie+"/"+listeRep[i],"ND", ND_of)
                dst_SR=os.path.join(repSortie+"/"+listeRep[i],"SR", SR_of)
                dst_ND_inv=os.path.join(repSortie+"/"+listeRep[i],"ND", ND_of_inv)
                # dst_SR_inv=os.path.join(rep_destination_finale1,"SR", SR_of_inv)
                if (not os.path.exists(dst_ND) or (not os.path.exists(dst_SR) and not os.path.exists(dst_ND_inv))): #On évite de lire à chaque fois les fichiers .tif
                    #cette logique regarde si le fichier ND existe ou si il n'existe ni SR ou SR inverse. Si jamais un de ces fichiers existe pas on les recréer
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



                    for index in range(135):
    
                        ND =  np.divide((1.0*ba - bb), (ba + bb))
                        ND[np.isinf(ND)] = np.nan
                        if not os.path.exists(dst_ND):
                            #if not os.path.exists(dst_ND_inv): #on observe que a/b = 1/(b/a)
                                ind = ['ND', bande1+"_"+bande2]
                            
                                val = []
                        
            
                                for point in listeCoordonnees:
                                    col = int((point[0] - xOrigin) / pixelWidth)
                                    row = int((yOrigin - point[1] ) / pixelHeight)
                    
                                    val.append(ND[row][col])
                                    
                                concat = ind + val
                                    
                                tab.loc[index]=concat
                            
                    
 
    
     
#lire la valeur des points TFE sur les pixels correspondantà l'indice

                    # if not os.path.exists(dst_ND):
                    #     if not os.path.exists(dst_ND_inv): #on observe que a/b = 1/(b/a)
                    #         with rasterio.open(dst_ND, "w", **profile) as dst:
                    #             dst.write(ND.astype(rasterio.float64), 1)

                    SR = np.divide(ba, bb)
                    SR[np.isinf(SR)] = np.nan
                    if not os.path.exists(dst_SR):
                            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
                     
                        ind = ['ND', bande1+"_"+bande2]
                    
                        val = []
                
    
                        for point in listeCoordonnees:
                            col = int((point[0] - xOrigin) / pixelWidth)
                            row = int((yOrigin - point[1] ) / pixelHeight)
            
                            val.append(SR[row][col])
                            
                        concat = ind + val
                            
                        tab.loc[index+1]=concat








              # three bands vegetation indices (3BSI / mSR et 3BSI_Tian)
            for elt in itertools.permutations(listeBandes,3):
                bande1 = elt[0].split("_")[3]
                bande2 = elt[1].split("_")[3]
                bande3 = elt[2].split("_")[3]
                BSI_of = "%s_%s_%s_3BSI_%s.tif" % (bande1, bande2, bande3, date )
                mSR_of = "%s_%s_%s_mSR_%s.tif" % (bande1, bande2, bande3, date )
                mSR_of_inv = "%s_%s_%s_mSR_%s.tif" % (bande1, bande3, bande2, date )
                BSI_Tian_of = "%s_%s_%s_3BSITian_%s.tif" % (bande1, bande2, bande3, date )
                BSI_Tian_of_inv = "%s_%s_%s_3BSITian_%s.tif" % (bande1, bande3, bande2, date )
                CVI_of = "%s_%s_%s_CVI_%s.tif" % (bande1, bande2, bande3, date )
                CVI_of_inv = "%s_%s_%s_CVI_%s.tif" % (bande2, bande1, bande3, date )
                dst_3BSI=os.path.join(repSortie+"/"+listeRep[i],"3BSI", BSI_of)
                dst_MSR=os.path.join(repSortie+"/"+listeRep[i],"mSR", mSR_of)
                dst_MSR_inv=os.path.join(repSortie+"/"+listeRep[i],"mSR", mSR_of_inv)
                dst_BSI_Tian=os.path.join(repSortie+"/"+listeRep[i],"3BSITian", BSI_Tian_of)
                dst_BSI_Tian_inv=os.path.join(repSortie+"/"+listeRep[i],"3BSITian", BSI_Tian_of_inv)
                dst_CVI=os.path.join(repSortie+"/"+listeRep[i],"CVI", CVI_of)
                dst_CVI_inv=os.path.join(repSortie+"/"+listeRep[i],"CVI", CVI_of_inv)
                if(not os.path.exists(dst_3BSI) or (not os.path.exists(dst_MSR) and not os.path.exists(dst_MSR_inv)) or (not os.path.exists(dst_BSI_Tian) and not os.path.exists(dst_BSI_Tian_inv))or(not os.path.exists(dst_CVI) and not os.path.exists(dst_CVI_inv))):
                    with rasterio.open(repCourant+"/"+listeBandes[0], "r") as src:
                        ba1 = src.read(1)
                        profile = src.profile
                        profile.update(
                                dtype=rasterio.float64,
                                count=1,
                                compress='lzw')
                    with rasterio.open(repCourant+"/"+listeBandes[1], "r") as src:
                        bb1 = src.read(1)
                        profile = src.profile
                        profile.update(
                                dtype=rasterio.float64,
                                count=1,
                                compress='lzw')
                    with rasterio.open(repCourant+"/"+listeBandes[2], "r") as src:
                        bc1 = src.read(1)
                        profile = src.profile
                        profile.update(
                                dtype=rasterio.float64,
                                count=1,
                                compress='lzw')

                    BSI =  np.divide((1.0* ba1 - bc1), (bb1 + bc1))
                    BSI[np.isinf(BSI)] = np.nan
                    if not os.path.exists(dst_3BSI):
                        with rasterio.open(dst_3BSI, "w", **profile) as dst:
                            dst.write(BSI.astype(rasterio.float64), 1)

                    mSR =  np.divide((1.0* ba1 - bc1), (bb1 - bc1))
                    mSR[np.isinf(mSR)] = np.nan
                    if not os.path.exists(dst_MSR):
                        if not os.path.exists(dst_MSR_inv):
                            with rasterio.open(dst_MSR, "w", **profile) as dst:
                                dst.write(mSR.astype(rasterio.float64), 1)

                    BSI_Tian =  np.divide((1.0* ba1 - bb1 - bc1), (ba1 + bb1 + bc1))
                    BSI_Tian[np.isinf(BSI_Tian)] = np.nan
                    if not os.path.exists(dst_BSI_Tian):
                        if not os.path.exists(dst_BSI_Tian_inv):
                            with rasterio.open(dst_BSI_Tian, "w", **profile) as dst:
                                dst.write(BSI_Tian.astype(rasterio.float64), 1)

                    CVI =  np.multiply((ba1 / bc1), (bb1 / bc1))
                    CVI[np.isinf(CVI)] = np.nan
                    if not os.path.exists(dst_CVI):
                        if not os.path.exists(dst_CVI_inv):
                            with rasterio.open(dst_CVI, "w", **profile) as dst:
                                dst.write(CVI.astype(rasterio.float64), 1)
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
            dst_indices=os.path.join(repSortie+"/"+listeRep[i],"indclass")
            ###################################################################
            #Calcul des indices classiques du fichier .xml
            ###################################################################
            #calcul du NDVI
            NDVI = np.divide((1.0*bandeB8 - bandeB4), (bandeB8 + bandeB4))
            NDVI[np.isinf(NDVI)]=np.nan
            if not os.path.exists(os.path.join(dst_indices,"NDVI_indclass_%s.tif"%(date))):
                with rasterio.open(os.path.join(dst_indices,"NDVI_indclass_%s.tif"%(date)), "w", **profile) as dst:
                    dst.write(NDVI.astype(rasterio.float64), 1)

            #calcul du GNDVI
            GNDVI = np.divide((1.0*bandeB8 - bandeB3), (bandeB8 + bandeB3))
            GNDVI[np.isinf(GNDVI)]=np.nan
            if not os.path.exists(os.path.join(dst_indices,"GNDVI_indclass_%s.tif"%(date))):
                with rasterio.open(os.path.join(dst_indices,"GNDVI_indclass_%s.tif"%(date)), "w", **profile) as dst:
                    dst.write(GNDVI.astype(rasterio.float64), 1)

            #calcul du NDVIre
            NDVIre = np.divide((1.0*bandeB8a - bandeB4), (bandeB8a + bandeB4))
            NDVIre[np.isinf(NDVIre)]=np.nan
            if not os.path.exists(os.path.join(dst_indices,"NDVIre_indclass_%s.tif"%(date))):
                with rasterio.open(os.path.join(dst_indices,"NDVIre_indclass_%s.tif"%(date)), "w", **profile) as dst:
                    dst.write(NDVIre.astype(rasterio.float64), 1)

            #calcul du NDI45
            NDI45 = np.divide((1.0*bandeB5 - bandeB4), (bandeB5 + bandeB4))
            NDI45[np.isinf(NDI45)]=np.nan
            if not os.path.exists(os.path.join(dst_indices,"NDI45_indclass_%s.tif"%(date))):
                with rasterio.open(os.path.join(dst_indices,"NDI45_indclass_%s.tif"%(date)), "w", **profile) as dst:
                    dst.write(NDI45.astype(rasterio.float64), 1)

            #calcul du NDII
            NDII = np.divide((1.0*bandeB8 - bandeB11), (bandeB8 + bandeB11))
            NDII[np.isinf(NDII)]=np.nan
            if not os.path.exists(os.path.join(dst_indices,"NDII_indclass_%s.tif"%(date))):
                with rasterio.open(os.path.join(dst_indices,"NDII_indclass_%s.tif"%(date)), "w", **profile) as dst:
                    dst.write(NDII.astype(rasterio.float64), 1)

            #calcul du NREDI1
            NREDI1 = np.divide((1.0*bandeB6 - bandeB5), (bandeB6 + bandeB5))
            NREDI1[np.isinf(NREDI1)]=np.nan
            if not os.path.exists(os.path.join(dst_indices,"NREDI1_indclass_%s.tif"%(date))):
                with rasterio.open(os.path.join(dst_indices,"NREDI1_indclass_%s.tif"%(date)), "w", **profile) as dst:
                    dst.write(NREDI1.astype(rasterio.float64), 1)

            #calcul du NREDI2
            NREDI2 = np.divide((1.0*bandeB7 - bandeB5), (bandeB7 + bandeB5))
            NREDI2[np.isinf(NREDI2)]=np.nan
            if not os.path.exists(os.path.join(dst_indices,"NREDI2_indclass_%s.tif"%(date))):
                with rasterio.open(os.path.join(dst_indices,"NREDI2_indclass_%s.tif"%(date)), "w", **profile) as dst:
                    dst.write(NREDI2.astype(rasterio.float64), 1)

            #calcul du NREDI3
            NREDI3 = np.divide((1.0*bandeB7 - bandeB6), (bandeB7 + bandeB6))
            NREDI3[np.isinf(NREDI3)]=np.nan
            if not os.path.exists(os.path.join(dst_indices,"NREDI3_indclass_%s.tif"%(date))):
                with rasterio.open(os.path.join(dst_indices,"NREDI3_indclass_%s.tif"%(date)), "w", **profile) as dst:
                    dst.write(NREDI3.astype(rasterio.float64), 1)

            #calcul du PSRI
            PSRI = np.divide((1.0*bandeB4 - bandeB3), (bandeB5))
            PSRI[np.isinf(PSRI)]=np.nan
            if not os.path.exists(os.path.join(dst_indices,"PSRI_indclass_%s.tif"%(date))):
                with rasterio.open(os.path.join(dst_indices,"PSRI_indclass_%s.tif"%(date)), "w", **profile) as dst:
                    dst.write(PSRI.astype(rasterio.float64), 1)

            #calcul du MSI
            MSI = np.divide((1.0*bandeB11), (bandeB8))
            MSI[np.isinf(MSI)]=np.nan
            if not os.path.exists(os.path.join(dst_indices,"MSI_indclass_%s.tif"%(date))):
                with rasterio.open(os.path.join(dst_indices,"MSI_indclass_%s.tif"%(date)), "w", **profile) as dst:
                    dst.write(MSI.astype(rasterio.float64), 1)

            #calcul du IRECI
            IRECI = np.divide((1.0*bandeB7 - bandeB4), (np.divide(1.0*bandeB5 , bandeB6)))
            IRECI[np.isinf(IRECI)]=np.nan
            if not os.path.exists(os.path.join(dst_indices,"IRECI_indclass_%s.tif"%(date))):
                with rasterio.open(os.path.join(dst_indices,"IRECI_indclass_%s.tif"%(date)), "w", **profile) as dst:
                    dst.write(IRECI.astype(rasterio.float64), 1)

            #calcul du MTCI
            MTCI = np.divide((1.0*bandeB8 - bandeB5), (bandeB5 - bandeB4))
            MTCI[np.isinf(MTCI)]=np.nan
            if not os.path.exists(os.path.join(dst_indices,"MTCI_indclass_%s.tif"%(date))):
                with rasterio.open(os.path.join(dst_indices,"MTCI_indclass_%s.tif"%(date)), "w", **profile) as dst:
                    dst.write(MTCI.astype(rasterio.float64), 1)

            #calcul du MCARI
            MCARI = np.multiply(((bandeB5 - bandeB4) - (0.2*(bandeB5 - bandeB3))), (bandeB5 - bandeB4))
            MCARI[np.isinf(MCARI)]=np.nan
            if not os.path.exists(os.path.join(dst_indices,"MCARI_indclass_%s.tif"%(date))):
                with rasterio.open(os.path.join(dst_indices,"MCARI_indclass_%s.tif"%(date)), "w", **profile) as dst:
                    dst.write(MCARI.astype(rasterio.float64), 1)