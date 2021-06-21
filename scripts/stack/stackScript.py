#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 15:28:24 2021

@author: Emilie Sirot
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
        
    
    
            with rasterio.open(repCourant+"/"+listeBandes[0]) as src:
                meta = src.meta
                
            meta.update(count= len(listeBandes))
            
            with rasterio.open(repSortieDate+'/stack.tif', 'w', **meta) as dst:
                for id, layer in enumerate(listeBandes, start=1):
                    with rasterio.open(repCourant+"/"+layer) as src1:
                        dst.write_band(id, src1.read(1))
            
####################
####################
### Tuile 31TFK ####
####################
####################

#drivers

gdal.AllRegister()

repDonnees = r"../applicationMasque/sortie/sortieT31TFK"
repSortie = "sortie/sortieT31TFK"


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
        
    
    
            with rasterio.open(repCourant+"/"+listeBandes[0]) as src:
                meta = src.meta
                
            meta.update(count= len(listeBandes))
            
            with rasterio.open(repSortieDate+'/stack.tif', 'w', **meta) as dst:
                for id, layer in enumerate(listeBandes, start=1):
                    with rasterio.open(repCourant+"/"+layer) as src1:
                        dst.write_band(id, src1.read(1))

####################
####################
### Tuile 31TGK ####
####################
####################

#drivers

gdal.AllRegister()

repDonnees = r"../applicationMasque/sortie/sortieT31TGK"
repSortie = "sortie/sortieT31TGK"


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
        
    
    
            with rasterio.open(repCourant+"/"+listeBandes[0]) as src:
                meta = src.meta
                
            meta.update(count= len(listeBandes))
            
            with rasterio.open(repSortieDate+'/stack.tif', 'w', **meta) as dst:
                for id, layer in enumerate(listeBandes, start=1):
                    with rasterio.open(repCourant+"/"+layer) as src1:
                        dst.write_band(id, src1.read(1))
                        
####################
####################
### Tuile 31TGL ####
####################
####################

#drivers

gdal.AllRegister()

repDonnees = r"../applicationMasque/sortie/sortieT31TGL"
repSortie = "sortie/sortieT31TGL"


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
        
    
    
            with rasterio.open(repCourant+"/"+listeBandes[0]) as src:
                meta = src.meta
                
            meta.update(count= len(listeBandes))
            
            with rasterio.open(repSortieDate+'/stack.tif', 'w', **meta) as dst:
                for id, layer in enumerate(listeBandes, start=1):
                    with rasterio.open(repCourant+"/"+layer) as src1:
                        dst.write_band(id, src1.read(1))
                        
####################
####################
### Tuile 32TLP ####
####################
####################

#drivers

gdal.AllRegister()

repDonnees = r"../applicationMasque/sortie/sortieT32TLP"
repSortie = "sortie/sortieT32TLP"


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
        
    
    
            with rasterio.open(repCourant+"/"+listeBandes[0]) as src:
                meta = src.meta
                
            meta.update(count= len(listeBandes))
            
            with rasterio.open(repSortieDate+'/stack.tif', 'w', **meta) as dst:
                for id, layer in enumerate(listeBandes, start=1):
                    with rasterio.open(repCourant+"/"+layer) as src1:
                        dst.write_band(id, src1.read(1))
                        
####################
####################
### Tuile 32TLQ ####
####################
####################

#drivers

gdal.AllRegister()

repDonnees = r"../applicationMasque/sortie/sortieT32TLQ"
repSortie = "sortie/sortieT32TLQ"


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
        
    
    
            with rasterio.open(repCourant+"/"+listeBandes[0]) as src:
                meta = src.meta
                
            meta.update(count= len(listeBandes))
            
            with rasterio.open(repSortieDate+'/stack.tif', 'w', **meta) as dst:
                for id, layer in enumerate(listeBandes, start=1):
                    with rasterio.open(repCourant+"/"+layer) as src1:
                        dst.write_band(id, src1.read(1))
                        
                        
####################
####################
### Tuile 32TLR ####
####################
####################

#drivers

gdal.AllRegister()

repDonnees = r"../applicationMasque/sortie/sortieT32TLR"
repSortie = "sortie/sortieT32TLR"


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
        
    
    
            with rasterio.open(repCourant+"/"+listeBandes[0]) as src:
                meta = src.meta
                
            meta.update(count= len(listeBandes))
            
            with rasterio.open(repSortieDate+'/stack.tif', 'w', **meta) as dst:
                for id, layer in enumerate(listeBandes, start=1):
                    with rasterio.open(repCourant+"/"+layer) as src1:
                        dst.write_band(id, src1.read(1))