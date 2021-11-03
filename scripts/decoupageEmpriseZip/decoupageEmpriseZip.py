#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 15:02:45 2021

@author: Emilie Sirot
"""

#librairies utilisees
import os
from pprint import pprint
from zipfile import ZipFile
from osgeo import gdal

####################
####################
### Tuile 31TFJ ####
####################
####################


#definition des repertoires existants dans lesquels utiliser les donnees et des repertoires de sortie des traitements
repDonnees = "archive_zip" #repertoire qui contient les dossiers .zip Sentinel2
repEmprise = "emprise" #repertoire qui contient les emprises 
repSortie = "sortie/sortieT31TFJ" #repertoire pour la sortie des fichiers 

#definition de l'emprise de découpage selon la tuile
emp31TFJ = "emprise/empT31TFJ.gpkg"

#defintion de du repertoire de la tuile
rep31TFJ = os.listdir("archive_zip/T31TFJ")

#boucle permettant de parcourir les repertoire de donnees
for i in range(len(rep31TFJ)):
    
    #definir le sous-repertoire en cours
    dossierZip = os.path.join(repDonnees, "T31TFJ/"+rep31TFJ[i])
    
    #accès aux fichiers du sous-repertoire
    rep31TFJSousRep = ZipFile(dossierZip, 'r')
    pprint(rep31TFJSousRep.filelist)
    
    #creation d'une liste de ces fichiers
    rep31TFJFichiers = rep31TFJSousRep.namelist()

# # Selection des images à traiter

    # Selection des images à garder
    images = [f for f in rep31TFJFichiers if 'FRE' in f]
    #masqueSnow = [f for f in rep31TFJFichiers if ('EXS'in f or 'SNW' in f) and '.tif' in f]
    masque = [f for f in rep31TFJFichiers if 'CLM' in f and 'R1' in f ]
    
# # Dossier et fichiers de sortie
 
    #definir le nom des repertoires en sortie
    nomParties = os.path.basename(dossierZip).split("_")
    sat = nomParties[0].replace("SENTINEL", "S")
    date = nomParties[1].split("-")[0]
    
    
    rep = f"{sat}_{date}_{nomParties[3]}"
    repSortieExtrait = os.path.join(repSortie, rep)
    os.makedirs(repSortieExtrait, exist_ok=True) # creation du dossier sur le disque


# # Traitement de l'image compressee
# gdal lit directement des donnees dans des archives.  
# Pour des repDonneess au format zip on utilise le protocol vsizip.  
# Pour lire des donnees on donne le chemin de l'repDonnees (comme si c'etait un dossier) puis le chemin de l'image dans l'repDonnees.
  
    for img in images:
               
        imageParties = img.split("_")
        bande = imageParties[12].split(".")[0]
        nomExtrait = f"{rep}_{bande}"
        fichierExtrait = os.path.join(repSortieExtrait, nomExtrait) # nom + chemin de l'image
        sortieTif = gdal.Warp(fichierExtrait,
                            f"/vsizip/{dossierZip}/{img}", # vsizip + chemin du zip + chemin de l'image dans le zip
                            creationOptions=['COMPRESS=LZW', 'PREDICTOR=2'], # compression du tif
                            cutlineDSName=emp31TFJ, # decoupage en fonction d'un contour
                            dstNodata=-10000, # valeur de nodata -10000
                            xRes=10, yRes=-10, # resolution de sortie
                            targetAlignedPixels=True, # on garde le même emplacement des pixels que l'image de depart
                            cropToCutline=True) # on reduit l'image à l"emprise du contour
                             
                                 
        if not sortieTif:
            print(f"Erreur : {fichierExtrait}")
            sortieTif = None
    

    for img in masque:
           
        masque_parts = img.split("_")
        masque_name = masque_parts[11]+"_"+masque_parts[12].split(".")[0]
        nomExtrait = f"{rep}_{masque_name}"
        fichierExtrait = os.path.join(repSortieExtrait, nomExtrait) # nom + chemin de l'image
        sortieTif = gdal.Warp(fichierExtrait,
                            f"/vsizip/{dossierZip}/{img}", # vsizip + chemin du zip + chemin de l'image dans le zip
                            creationOptions=['COMPRESS=LZW', 'PREDICTOR=2'], # compression du tif
                            cutlineDSName=emp31TFJ, # decoupage en fonction d'un contour
                            dstNodata=-10000, # valeur de nodata
                            xRes=10, yRes=-10, # resolution de sortie
                            targetAlignedPixels=True, # on garde le même emplacement des pixels que l'image de depart
                            cropToCutline=True # on reduit l'image à l"emprise du contour
                            )
    if not sortieTif:
        print(f"Erreur : {fichierExtrait}")
        sortieTif = None
        
####################
####################
### Tuile 31TFK ####
####################
####################


repDonnees = "archive_zip" #repertoire qui contient les dossiers .zip Sentinel2
repEmprise = "emprise" #repertoire qui contient les emprises 
repSortie = "sortie/sortieT31TFK" #repertoire pour la sortie des fichiers 


emp31TFK = "emprise/empT31TFK.gpkg"


rep31TFK = os.listdir("archive_zip/T31TFK")

for i in range(len(rep31TFK)):
    
    #definir le sous-repertoire en cours
    dossierZip = os.path.join(repDonnees, "T31TFK/"+rep31TFK[i])
    
    #accès aux fichiers du sous-repertoire
    rep31TFKSousRep = ZipFile(dossierZip, 'r')
    pprint(rep31TFKSousRep.filelist)
    
    #creation d'une liste de ces fichiers
    rep31TFKFichiers = rep31TFKSousRep.namelist()

# # Selection des images à traiter

    # Selection des images à garder
    images = [f for f in rep31TFKFichiers if 'FRE' in f]
    #masqueSnow = [f for f in rep31TFKFichiers if ('EXS'in f or 'SNW' in f) and '.tif' in f]
    masque = [f for f in rep31TFKFichiers if 'CLM' in f and 'R1' in f ]
    
# # Dossier et fichiers de sortie
 
    #definir le nom des repertoires en sortie
    nomParties = os.path.basename(dossierZip).split("_")
    sat = nomParties[0].replace("SENTINEL", "S")
    date = nomParties[1].split("-")[0]
    
    
    rep = f"{sat}_{date}_{nomParties[3]}"
    repSortieExtrait = os.path.join(repSortie, rep)
    os.makedirs(repSortieExtrait, exist_ok=True) # creation du dossier sur le disque


# # Traitement de l'image compressee
# gdal lit directement des donnees dans des archives.  
# Pour des repDonneess au format zip on utilise le protocol vsizip.  
# Pour lire des donnees on donne le chemin de l'repDonnees (comme si c'etait un dossier) puis le chemin de l'image dans l'repDonnees.
  
    for img in images:
               
        imageParties = img.split("_")
        bande = imageParties[12].split(".")[0]
        nomExtrait = f"{rep}_{bande}"
        fichierExtrait = os.path.join(repSortieExtrait, nomExtrait) # nom + chemin de l'image
        sortieTif = gdal.Warp(fichierExtrait,
                            f"/vsizip/{dossierZip}/{img}", # vsizip + chemin du zip + chemin de l'image dans le zip
                            creationOptions=['COMPRESS=LZW', 'PREDICTOR=2'], # compression du tif
                            cutlineDSName=emp31TFK, # decoupage en fonction d'un contour
                            dstNodata=-10000, # valeur de nodata -10000
                            xRes=10, yRes=-10, # resolution de sortie
                            targetAlignedPixels=True, # on garde le même emplacement des pixels que l'image de depart
                            cropToCutline=True) # on reduit l'image à l"emprise du contour
                             
                                 
        if not sortieTif:
            print(f"Erreur : {fichierExtrait}")
            sortieTif = None
    

    for img in masque:
           
        masque_parts = img.split("_")
        masque_name = masque_parts[11]+"_"+masque_parts[12].split(".")[0]
        nomExtrait = f"{rep}_{masque_name}"
        fichierExtrait = os.path.join(repSortieExtrait, nomExtrait) # nom + chemin de l'image
        sortieTif = gdal.Warp(fichierExtrait,
                            f"/vsizip/{dossierZip}/{img}", # vsizip + chemin du zip + chemin de l'image dans le zip
                            creationOptions=['COMPRESS=LZW', 'PREDICTOR=2'], # compression du tif
                            cutlineDSName=emp31TFK, # decoupage en fonction d'un contour
                            dstNodata=-10000, # valeur de nodata
                            xRes=10, yRes=-10, # resolution de sortie
                            targetAlignedPixels=True, # on garde le même emplacement des pixels que l'image de depart
                            cropToCutline=True # on reduit l'image à l"emprise du contour
                            )
    if not sortieTif:
        print(f"Erreur : {fichierExtrait}")
        sortieTif = None
        
        
####################
####################
### Tuile 31TGK ####
####################
####################


repDonnees = "archive_zip" #repertoire qui contient les dossiers .zip Sentinel2
repEmprise = "emprise" #repertoire qui contient les emprises 
repSortie = "sortie/sortieT31TGK" #repertoire pour la sortie des fichiers 


emp31TGK = "emprise/empT31TGK.gpkg"


rep31TGK = os.listdir("archive_zip/T31TGK")

for i in range(len(rep31TGK)):
    
    #definir le sous-repertoire en cours
    dossierZip = os.path.join(repDonnees, "T31TGK/"+rep31TGK[i])
    
    #accès aux fichiers du sous-repertoire
    rep31TGKSousRep = ZipFile(dossierZip, 'r')
    pprint(rep31TGKSousRep.filelist)
    
    #creation d'une liste de ces fichiers
    rep31TGKFichiers = rep31TGKSousRep.namelist()

# # Selection des images à traiter

    # Selection des images à garder
    images = [f for f in rep31TGKFichiers if 'FRE' in f]
    #masqueSnow = [f for f in rep31TGKFichiers if ('EXS'in f or 'SNW' in f) and '.tif' in f]
    masque = [f for f in rep31TGKFichiers if 'CLM' in f and 'R1' in f ]
    
# # Dossier et fichiers de sortie
 
    #definir le nom des repertoires en sortie
    nomParties = os.path.basename(dossierZip).split("_")
    sat = nomParties[0].replace("SENTINEL", "S")
    date = nomParties[1].split("-")[0]
    
    
    rep = f"{sat}_{date}_{nomParties[3]}"
    repSortieExtrait = os.path.join(repSortie, rep)
    os.makedirs(repSortieExtrait, exist_ok=True) # creation du dossier sur le disque


# # Traitement de l'image compressee
# gdal lit directement des donnees dans des archives.  
# Pour des repDonneess au format zip on utilise le protocol vsizip.  
# Pour lire des donnees on donne le chemin de l'repDonnees (comme si c'etait un dossier) puis le chemin de l'image dans l'repDonnees.
  
    for img in images:
               
        imageParties = img.split("_")
        bande = imageParties[12].split(".")[0]
        nomExtrait = f"{rep}_{bande}"
        fichierExtrait = os.path.join(repSortieExtrait, nomExtrait) # nom + chemin de l'image
        sortieTif = gdal.Warp(fichierExtrait,
                            f"/vsizip/{dossierZip}/{img}", # vsizip + chemin du zip + chemin de l'image dans le zip
                            creationOptions=['COMPRESS=LZW', 'PREDICTOR=2'], # compression du tif
                            cutlineDSName=emp31TGK, # decoupage en fonction d'un contour
                            dstNodata=-10000, # valeur de nodata -10000
                            xRes=10, yRes=-10, # resolution de sortie
                            targetAlignedPixels=True, # on garde le même emplacement des pixels que l'image de depart
                            cropToCutline=True) # on reduit l'image à l"emprise du contour
                             
                                 
        if not sortieTif:
            print(f"Erreur : {fichierExtrait}")
            sortieTif = None
    

    for img in masque:
           
        masque_parts = img.split("_")
        masque_name = masque_parts[11]+"_"+masque_parts[12].split(".")[0]
        nomExtrait = f"{rep}_{masque_name}"
        fichierExtrait = os.path.join(repSortieExtrait, nomExtrait) # nom + chemin de l'image
        sortieTif = gdal.Warp(fichierExtrait,
                            f"/vsizip/{dossierZip}/{img}", # vsizip + chemin du zip + chemin de l'image dans le zip
                            creationOptions=['COMPRESS=LZW', 'PREDICTOR=2'], # compression du tif
                            cutlineDSName=emp31TGK, # decoupage en fonction d'un contour
                            dstNodata=-10000, # valeur de nodata
                            xRes=10, yRes=-10, # resolution de sortie
                            targetAlignedPixels=True, # on garde le même emplacement des pixels que l'image de depart
                            cropToCutline=True # on reduit l'image à l"emprise du contour
                            )
    if not sortieTif:
        print(f"Erreur : {fichierExtrait}")
        sortieTif = None
    
####################
####################
### Tuile 31TGL ####
####################
####################


repDonnees = "archive_zip" #repertoire qui contient les dossiers .zip Sentinel2
repEmprise = "emprise" #repertoire qui contient les emprises 
repSortie = "sortie/sortieT31TGL" #repertoire pour la sortie des fichiers 


emp31TGL = "emprise/empT31TGL.gpkg"


rep31TGL = os.listdir("archive_zip/T31TGL")

for i in range(len(rep31TGL)):
    
    #definir le sous-repertoire en cours
    dossierZip = os.path.join(repDonnees, "T31TGL/"+rep31TGL[i])
    
    #accès aux fichiers du sous-repertoire
    rep31TGLSousRep = ZipFile(dossierZip, 'r')
    pprint(rep31TGLSousRep.filelist)
    
    #creation d'une liste de ces fichiers
    rep31TGLFichiers = rep31TGLSousRep.namelist()

# # Selection des images à traiter

    # Selection des images à garder
    images = [f for f in rep31TGLFichiers if 'FRE' in f]
    #masqueSnow = [f for f in rep31TGLFichiers if ('EXS'in f or 'SNW' in f) and '.tif' in f]
    masque = [f for f in rep31TGLFichiers if 'CLM' in f and 'R1' in f ]
    
# # Dossier et fichiers de sortie
 
    #definir le nom des repertoires en sortie
    nomParties = os.path.basename(dossierZip).split("_")
    sat = nomParties[0].replace("SENTINEL", "S")
    date = nomParties[1].split("-")[0]
    
    
    rep = f"{sat}_{date}_{nomParties[3]}"
    repSortieExtrait = os.path.join(repSortie, rep)
    os.makedirs(repSortieExtrait, exist_ok=True) # creation du dossier sur le disque


# # Traitement de l'image compressee
# gdal lit directement des donnees dans des archives.  
# Pour des repDonneess au format zip on utilise le protocol vsizip.  
# Pour lire des donnees on donne le chemin de l'repDonnees (comme si c'etait un dossier) puis le chemin de l'image dans l'repDonnees.
  
    for img in images:
               
        imageParties = img.split("_")
        bande = imageParties[12].split(".")[0]
        nomExtrait = f"{rep}_{bande}"
        fichierExtrait = os.path.join(repSortieExtrait, nomExtrait) # nom + chemin de l'image
        sortieTif = gdal.Warp(fichierExtrait,
                            f"/vsizip/{dossierZip}/{img}", # vsizip + chemin du zip + chemin de l'image dans le zip
                            creationOptions=['COMPRESS=LZW', 'PREDICTOR=2'], # compression du tif
                            cutlineDSName=emp31TGL, # decoupage en fonction d'un contour
                            dstNodata=-10000, # valeur de nodata -10000
                            xRes=10, yRes=-10, # resolution de sortie
                            targetAlignedPixels=True, # on garde le même emplacement des pixels que l'image de depart
                            cropToCutline=True) # on reduit l'image à l"emprise du contour
                             
                                 
        if not sortieTif:
            print(f"Erreur : {fichierExtrait}")
            sortieTif = None
    

    for img in masque:
           
        masque_parts = img.split("_")
        masque_name = masque_parts[11]+"_"+masque_parts[12].split(".")[0]
        nomExtrait = f"{rep}_{masque_name}"
        fichierExtrait = os.path.join(repSortieExtrait, nomExtrait) # nom + chemin de l'image
        sortieTif = gdal.Warp(fichierExtrait,
                            f"/vsizip/{dossierZip}/{img}", # vsizip + chemin du zip + chemin de l'image dans le zip
                            creationOptions=['COMPRESS=LZW', 'PREDICTOR=2'], # compression du tif
                            cutlineDSName=emp31TGL, # decoupage en fonction d'un contour
                            dstNodata=-10000, # valeur de nodata
                            xRes=10, yRes=-10, # resolution de sortie
                            targetAlignedPixels=True, # on garde le même emplacement des pixels que l'image de depart
                            cropToCutline=True # on reduit l'image à l"emprise du contour
                            )
    if not sortieTif:
        print(f"Erreur : {fichierExtrait}")
        sortieTif = None
        

####################
####################
### Tuile 32TLP ####
####################
####################


repDonnees = "archive_zip" #repertoire qui contient les dossiers .zip Sentinel2
repEmprise = "emprise" #repertoire qui contient les emprises 
repSortie = "sortie/sortieT32TLP" #repertoire pour la sortie des fichiers 


emp32TLP = "emprise/empT32TLP.gpkg"


rep32TLP = os.listdir("archive_zip/T32TLP")

for i in range(len(rep32TLP)):
    
    #definir le sous-repertoire en cours
    dossierZip = os.path.join(repDonnees, "T32TLP/"+rep32TLP[i])
    
    #accès aux fichiers du sous-repertoire
    rep32TLPSousRep = ZipFile(dossierZip, 'r')
    pprint(rep32TLPSousRep.filelist)
    
    #creation d'une liste de ces fichiers
    rep32TLPFichiers = rep32TLPSousRep.namelist()

# # Selection des images à traiter

    # Selection des images à garder
    images = [f for f in rep32TLPFichiers if 'FRE' in f]
    #masqueSnow = [f for f in rep32TLPFichiers if ('EXS'in f or 'SNW' in f) and '.tif' in f]
    masque = [f for f in rep32TLPFichiers if 'CLM' in f and 'R1' in f ]
    
# # Dossier et fichiers de sortie
 
    #definir le nom des repertoires en sortie
    nomParties = os.path.basename(dossierZip).split("_")
    sat = nomParties[0].replace("SENTINEL", "S")
    date = nomParties[1].split("-")[0]
    
    
    rep = f"{sat}_{date}_{nomParties[3]}"
    repSortieExtrait = os.path.join(repSortie, rep)
    os.makedirs(repSortieExtrait, exist_ok=True) # creation du dossier sur le disque


# # Traitement de l'image compressee
# gdal lit directement des donnees dans des archives.  
# Pour des repDonneess au format zip on utilise le protocol vsizip.  
# Pour lire des donnees on donne le chemin de l'repDonnees (comme si c'etait un dossier) puis le chemin de l'image dans l'repDonnees.
  
    for img in images:
               
        imageParties = img.split("_")
        bande = imageParties[12].split(".")[0]
        nomExtrait = f"{rep}_{bande}"
        fichierExtrait = os.path.join(repSortieExtrait, nomExtrait) # nom + chemin de l'image
        sortieTif = gdal.Warp(fichierExtrait,
                            f"/vsizip/{dossierZip}/{img}", # vsizip + chemin du zip + chemin de l'image dans le zip
                            creationOptions=['COMPRESS=LZW', 'PREDICTOR=2'], # compression du tif
                            cutlineDSName=emp32TLP, # decoupage en fonction d'un contour
                            dstNodata=-10000, # valeur de nodata -10000
                            xRes=10, yRes=-10, # resolution de sortie
                            targetAlignedPixels=True, # on garde le même emplacement des pixels que l'image de depart
                            cropToCutline=True) # on reduit l'image à l"emprise du contour
                             
                                 
        if not sortieTif:
            print(f"Erreur : {fichierExtrait}")
            sortieTif = None
    

    for img in masque:
           
        masque_parts = img.split("_")
        masque_name = masque_parts[11]+"_"+masque_parts[12].split(".")[0]
        nomExtrait = f"{rep}_{masque_name}"
        fichierExtrait = os.path.join(repSortieExtrait, nomExtrait) # nom + chemin de l'image
        sortieTif = gdal.Warp(fichierExtrait,
                            f"/vsizip/{dossierZip}/{img}", # vsizip + chemin du zip + chemin de l'image dans le zip
                            creationOptions=['COMPRESS=LZW', 'PREDICTOR=2'], # compression du tif
                            cutlineDSName=emp32TLP, # decoupage en fonction d'un contour
                            dstNodata=-10000, # valeur de nodata
                            xRes=10, yRes=-10, # resolution de sortie
                            targetAlignedPixels=True, # on garde le même emplacement des pixels que l'image de depart
                            cropToCutline=True # on reduit l'image à l"emprise du contour
                            )
    if not sortieTif:
        print(f"Erreur : {fichierExtrait}")
        sortieTif = None
        
        
####################
####################
### Tuile 32TLQ ####
####################
####################


repDonnees = "archive_zip" #repertoire qui contient les dossiers .zip Sentinel2
repEmprise = "emprise" #repertoire qui contient les emprises 
repSortie = "sortie/sortieT32TLQ" #repertoire pour la sortie des fichiers 


emp32TLQ = "emprise/empT32TLQ.gpkg"


rep32TLQ = os.listdir("archive_zip/T32TLQ")

for i in range(len(rep32TLQ)):
    
    #definir le sous-repertoire en cours
    dossierZip = os.path.join(repDonnees, "T32TLQ/"+rep32TLQ[i])
    
    #accès aux fichiers du sous-repertoire
    rep32TLQSousRep = ZipFile(dossierZip, 'r')
    pprint(rep32TLQSousRep.filelist)
    
    #creation d'une liste de ces fichiers
    rep32TLQFichiers = rep32TLQSousRep.namelist()

# # Selection des images à traiter

    # Selection des images à garder
    images = [f for f in rep32TLQFichiers if 'FRE' in f]
    #masqueSnow = [f for f in rep32TLQFichiers if ('EXS'in f or 'SNW' in f) and '.tif' in f]
    masque = [f for f in rep32TLQFichiers if 'CLM' in f and 'R1' in f ]
    
# # Dossier et fichiers de sortie
 
    #definir le nom des repertoires en sortie
    nomParties = os.path.basename(dossierZip).split("_")
    sat = nomParties[0].replace("SENTINEL", "S")
    date = nomParties[1].split("-")[0]
    
    
    rep = f"{sat}_{date}_{nomParties[3]}"
    repSortieExtrait = os.path.join(repSortie, rep)
    os.makedirs(repSortieExtrait, exist_ok=True) # creation du dossier sur le disque


# # Traitement de l'image compressee
# gdal lit directement des donnees dans des archives.  
# Pour des repDonneess au format zip on utilise le protocol vsizip.  
# Pour lire des donnees on donne le chemin de l'repDonnees (comme si c'etait un dossier) puis le chemin de l'image dans l'repDonnees.
  
    for img in images:
               
        imageParties = img.split("_")
        bande = imageParties[12].split(".")[0]
        nomExtrait = f"{rep}_{bande}"
        fichierExtrait = os.path.join(repSortieExtrait, nomExtrait) # nom + chemin de l'image
        sortieTif = gdal.Warp(fichierExtrait,
                            f"/vsizip/{dossierZip}/{img}", # vsizip + chemin du zip + chemin de l'image dans le zip
                            creationOptions=['COMPRESS=LZW', 'PREDICTOR=2'], # compression du tif
                            cutlineDSName=emp32TLQ, # decoupage en fonction d'un contour
                            dstNodata=-10000, # valeur de nodata -10000
                            xRes=10, yRes=-10, # resolution de sortie
                            targetAlignedPixels=True, # on garde le même emplacement des pixels que l'image de depart
                            cropToCutline=True) # on reduit l'image à l"emprise du contour
                             
                                 
        if not sortieTif:
            print(f"Erreur : {fichierExtrait}")
            sortieTif = None
    

    for img in masque:
           
        masque_parts = img.split("_")
        masque_name = masque_parts[11]+"_"+masque_parts[12].split(".")[0]
        nomExtrait = f"{rep}_{masque_name}"
        fichierExtrait = os.path.join(repSortieExtrait, nomExtrait) # nom + chemin de l'image
        sortieTif = gdal.Warp(fichierExtrait,
                            f"/vsizip/{dossierZip}/{img}", # vsizip + chemin du zip + chemin de l'image dans le zip
                            creationOptions=['COMPRESS=LZW', 'PREDICTOR=2'], # compression du tif
                            cutlineDSName=emp32TLQ, # decoupage en fonction d'un contour
                            dstNodata=-10000, # valeur de nodata
                            xRes=10, yRes=-10, # resolution de sortie
                            targetAlignedPixels=True, # on garde le même emplacement des pixels que l'image de depart
                            cropToCutline=True # on reduit l'image à l"emprise du contour
                            )
    if not sortieTif:
        print(f"Erreur : {fichierExtrait}")
        sortieTif = None
        
####################
####################
### Tuile 32TLR ####
####################
####################


repDonnees = "archive_zip" #repertoire qui contient les dossiers .zip Sentinel2
repEmprise = "emprise" #repertoire qui contient les emprises 
repSortie = "sortie/sortieT32TLR" #repertoire pour la sortie des fichiers 


emp32TLR = "emprise/empT32TLR.gpkg"


rep32TLR = os.listdir("archive_zip/T32TLR")

for i in range(len(rep32TLR)):
    
    #definir le sous-repertoire en cours
    dossierZip = os.path.join(repDonnees, "T32TLR/"+rep32TLR[i])
    
    #accès aux fichiers du sous-repertoire
    rep32TLRSousRep = ZipFile(dossierZip, 'r')
    pprint(rep32TLRSousRep.filelist)
    
    #creation d'une liste de ces fichiers
    rep32TLRFichiers = rep32TLRSousRep.namelist()

# # Selection des images à traiter

    # Selection des images à garder
    images = [f for f in rep32TLRFichiers if 'FRE' in f]
    #masqueSnow = [f for f in rep32TLRFichiers if ('EXS'in f or 'SNW' in f) and '.tif' in f]
    masque = [f for f in rep32TLRFichiers if 'CLM' in f and 'R1' in f ]
    
# # Dossier et fichiers de sortie
 
    #definir le nom des repertoires en sortie
    nomParties = os.path.basename(dossierZip).split("_")
    sat = nomParties[0].replace("SENTINEL", "S")
    date = nomParties[1].split("-")[0]
    
    
    rep = f"{sat}_{date}_{nomParties[3]}"
    repSortieExtrait = os.path.join(repSortie, rep)
    os.makedirs(repSortieExtrait, exist_ok=True) # creation du dossier sur le disque


# # Traitement de l'image compressee
# gdal lit directement des donnees dans des archives.  
# Pour des repDonneess au format zip on utilise le protocol vsizip.  
# Pour lire des donnees on donne le chemin de l'repDonnees (comme si c'etait un dossier) puis le chemin de l'image dans l'repDonnees.
  
    for img in images:
               
        imageParties = img.split("_")
        bande = imageParties[12].split(".")[0]
        nomExtrait = f"{rep}_{bande}"
        fichierExtrait = os.path.join(repSortieExtrait, nomExtrait) # nom + chemin de l'image
        sortieTif = gdal.Warp(fichierExtrait,
                            f"/vsizip/{dossierZip}/{img}", # vsizip + chemin du zip + chemin de l'image dans le zip
                            creationOptions=['COMPRESS=LZW', 'PREDICTOR=2'], # compression du tif
                            cutlineDSName=emp32TLR, # decoupage en fonction d'un contour
                            dstNodata=-10000, # valeur de nodata -10000
                            xRes=10, yRes=-10, # resolution de sortie
                            targetAlignedPixels=True, # on garde le même emplacement des pixels que l'image de depart
                            cropToCutline=True) # on reduit l'image à l"emprise du contour
                             
                                 
        if not sortieTif:
            print(f"Erreur : {fichierExtrait}")
            sortieTif = None
    

    for img in masque:
           
        masque_parts = img.split("_")
        masque_name = masque_parts[11]+"_"+masque_parts[12].split(".")[0]
        nomExtrait = f"{rep}_{masque_name}"
        fichierExtrait = os.path.join(repSortieExtrait, nomExtrait) # nom + chemin de l'image
        sortieTif = gdal.Warp(fichierExtrait,
                            f"/vsizip/{dossierZip}/{img}", # vsizip + chemin du zip + chemin de l'image dans le zip
                            creationOptions=['COMPRESS=LZW', 'PREDICTOR=2'], # compression du tif
                            cutlineDSName=emp32TLR, # decoupage en fonction d'un contour
                            dstNodata=-10000, # valeur de nodata
                            xRes=10, yRes=-10, # resolution de sortie
                            targetAlignedPixels=True, # on garde le même emplacement des pixels que l'image de depart
                            cropToCutline=True # on reduit l'image à l"emprise du contour
                            )
    if not sortieTif:
        print(f"Erreur : {fichierExtrait}")
        sortieTif = None