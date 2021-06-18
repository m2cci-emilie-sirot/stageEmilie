#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 15:28:24 2021

@author: Emilie Sirot d'après le script de Valentin Barbier
"""

import os
import rasterio
from osgeo import gdal, gdal_array
import numpy as np

####################
####################
### Tuile 31TFJ ####
####################
####################

#drivers

gdal.AllRegister()

repDonnees = r"../applicationMasque/sortie/sortieT31TFJ"
repSortie = "sortie/sortieT31TFJ"


listeRep = os.listdir(repDonnees)


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
    
    for j in range(len(listeBandes)):
            nomPartiesImage = os.path.basename(listeBandes[j]).split("_")#séparer les parties du fichier en cours de traitement pour les réutiliser pour la sortie
            sat = nomPartiesImage[0]
            date = nomPartiesImage[1]
            tuile = nomPartiesImage[2]
            bande = nomPartiesImage[3]
        
            #définir les répertoires en sortie  
            rep = f"{sat}_{date}_{tuile}"
            repSortieDate = os.path.join(repSortie, rep)
            os.makedirs(repSortieDate, exist_ok=True) # création du dossier sur le disque
        
    
    
            # with rasterio.open(repCourant+"/"+listeBandes[0]) as src:
            #     meta = src.meta
                
            # meta.update(count= len(listeBandes))
            
            # with rasterio.open(repSortieDate+'/stack.tif', 'w', **meta) as dst:
            #     for id, layer in enumerate(listeBandes, start=1):
            #         with rasterio.open(repCourant+"/"+layer) as src1:
            #             dst.write_band(id, src1.read(1))
            
            
    
    
    
    
    
    
    
    
    
    
    

    # #ouverture des bandes avec GDAL
    # B2image = gdal.Open(repCourant+"/"+B2[0])
    # B3image = gdal.Open(repCourant+"/"+B3[0])
    # B3image = gdal.Open(repCourant+"/"+B3[0])
    # B4image = gdal.Open(repCourant+"/"+B4[0])
    # B5image = gdal.Open(repCourant+"/"+B5[0])
    # B6image = gdal.Open(repCourant+"/"+B6[0])
    # B7image = gdal.Open(repCourant+"/"+B7[0])
    # B8image = gdal.Open(repCourant+"/"+B8[0])
    # B8Aimage = gdal.Open(repCourant+"/"+B8A[0])
    # B11image = gdal.Open(repCourant+"/"+B11[0])
    # B12image = gdal.Open(repCourant+"/"+B12[0])

    # #transformation des bandes en array
    
    # B2Array = B2image.ReadAsArray()
    # B3Array = B3image.ReadAsArray()
    # B4Array = B4image.ReadAsArray()
    # B5Array = B5image.ReadAsArray()
    # B6Array = B6image.ReadAsArray()
    # B7Array = B7image.ReadAsArray()
    # B8Array = B8image.ReadAsArray()
    # B8AArray = B8Aimage.ReadAsArray()
    # B11Array = B11image.ReadAsArray()
    # B12Array = B12image.ReadAsArray()

    # stack = np.array([B2Array, B3Array, B4Array, B5Array, B5Array, B6Array, B7Array, B8Array, B8AArray, B11Array, B12Array])

    # gdal_array.SaveArray(stack.astype("int"), "stack.tif", "GTiff")


    # rep=os.path.join(root,"Traitements")
    # rep_donnees=os.path.join(rep,ferme,"3_images_masquees",annee)

#     for (path,dirs,files) in os.walk(rep_donnees):
#         for dir in dirs:
#             listeBandes=[]
# #            print(dir)
#             for (path1, dirs1, files1) in os.walk(rep_donnees):
#                 for file1 in files1:
# #                    print("file1 :", file1)
#                     if((dir in path1) and ("msk" in file1)):
#                         listeBandes.append(os.path.join(path1,file1))
#                         x=file1.split("_")[1].split("-")[0]# a,b,c,d,e,f,g,h,i,j,k=file.split("_") # x,y,z=b.split("-")
# #                    else:
# #                        print("\nErreur")
# #                        print("dir :", dir)
# #                        print("path1 :", path1)
# #                        print("file1 :", file1)

           
             if not os.path.exists(os.path.join(rep_donnees,dir, "%s_scaling_stack.tif"%(x))):
#                print("li_band :", li_band)
                os.system("gdal_merge.py -separate -co PHOTOMETRIC=RGB -o %s %s %s %s %s %s %s %s %s %s %s"
                              %(os.path.join(rep_donnees,dir, "%s_scaling_stack.tif"%(x)),li_band[0], li_band[1], li_band[2],
                                li_band[3], li_band[4],li_band[5], li_band[6], li_band[7], li_band[8], li_band[9]))
                with rasterio.open(os.path.join(rep_donnees,dir, "%s_scaling_stack.tif"%(x)), "r") as src:
                    band = src.read(1)
                    profile = src.profile
                    band[band==0]=np.nan
                    os.remove(os.path.join(rep_donnees,dir, "%s_scaling_stack.tif"%(x)))
                    with rasterio.open(os.path.join(rep_donnees,dir, "%s_scaling_stack.tif"%(x)), "w", **profile) as dst:
                        dst.write(band.astype(rasterio.float64), 1)
                        
                        
                        
                        
                        
    