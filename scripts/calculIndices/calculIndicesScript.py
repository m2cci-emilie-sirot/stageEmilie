#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 16:44:05 2021

@author: Emilie Sirot d'après le script de Valentin Barbier
"""

def indices(root,ferme,annee):
    """
    Principe
    ========

    Cette fonction permet de créer des indices liés aux bandes colorées qui permettront de déterminer la biomasse dans les prairies

    :param root: répertoire de travail global
    :param ferme: ferme étudiée (correspond à la zone d'étude)
    :param annee: année d'étude
    :type root: string
    :type ferme: string
    :type annee: string


 
    Fonction qui permet de créer des indices liés aux bandes colorées qui permettront de déterminer la biomasse dans les prairies
    rep_destination est le répertoire d'enregistrement des données
    li_band est une liste des bandes colorées

 """
 
####################
####################
### Tuile 31TFJ ####
####################
####################

 
 
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
    del B8[1]
    B8A = [f for f in fichiersRep if 'B8A' in f]
    B11 = [f for f in fichiersRep if 'B11' in f]
    B12 = [f for f in fichiersRep if 'B12' in f]
    
    
    listeBandes = B2+B3+B4+B5+B6+B7+B8+B8A+B11+B12



















    rep=os.path.join(root,"Traitements")
    repDonnees=os.path.join(rep,ferme,"3_images_masquees",annee)
    rep_destination_finale=os.path.join(rep,ferme,"4_indices",annee)

    indices=["3BSI","3BSITian","CVI","mSR","ND","SR","indclass"]
    for (path,dirs,files) in os.walk(repDonnees):
        for dir in dirs:
            for indice in indices:
                if not os.path.exists(os.path.join(rep_destination_finale,dir,indice)):
                    os.makedirs(os.path.join(rep_destination_finale,dir,indice))


    for (path,dirs,files) in os.walk(repDonnees):
        for dir in dirs:
            li_band2=[]
            rep_destination_finale1=os.path.join(rep_destination_finale,dir)
            for (path1,dirs1,files1) in os.walk(repDonnees):
                for file1 in files1:
                    if((dir in path1) and ("msk" in file1)):
                        li_band2.append(os.path.join(path1,file1))

                        x=file1.split("_")[1].split("-")[0]# a,b,c,d,e,f,g,h,i,j,k=file.split("_") # x,y,z=b.split("-")

            #Je trie li_band dans l'ordre de la liste suivante
            li_band1=["B2","B3","B4","B5","B6","B7","B8","B8A","B11","B12"]
            it=0
            li_band=[]
            for i in li_band1:
                for j in li_band2:

                    if(j.split("_")[-3]==i):
                        li_band.append(j)
                it+=1


            # two bands vegetation indices (normalized difference et simple ratio)

            for elt in itertools.permutations(li_band,2):
                bande1 = elt[0].split("_")[-3]
                bande2 = elt[1].split("_")[-3]
                ND_of = "%s_%s_ND_%s.tif" % (bande1, bande2, x )
                ND_of_inv="%s_%s_ND_%s.tif" % (bande2, bande1, x )
                SR_of = "%s_%s_SR_%s.tif" % (bande1, bande2, x )
                # SR_of_inv="%s_%s_SR_%s.tif" % (bande2, bande1, x )
                dst_ND=os.path.join(rep_destination_finale1,"ND", ND_of)
                dst_SR=os.path.join(rep_destination_finale1,"SR", SR_of)
                dst_ND_inv=os.path.join(rep_destination_finale1,"ND", ND_of_inv)
                # dst_SR_inv=os.path.join(rep_destination_finale1,"SR", SR_of_inv)
                if (not os.path.exists(dst_ND) or (not os.path.exists(dst_SR) and not os.path.exists(dst_ND_inv))): #On évite de lire à chaque fois les fichiers .tif
                    #cette logique regarde si le fichier ND existe ou si il n'existe ni SR ou SR inverse. Si jamais un de ces fichiers existe pas on les recréer
                    with rasterio.open(elt[0], "r") as src:
                        ba = src.read(1)
                        profile = src.profile
                        profile.update(
                                dtype=rasterio.float64,
                                count=1,
                                compress='lzw')
                    with rasterio.open(elt[1], "r") as src:
                        bb = src.read(1)
                        profile = src.profile
                        profile.update(
                                dtype=rasterio.float64,
                                count=1,
                                compress='lzw')

                    ND =  np.divide((1.0*ba - bb), (ba + bb))
                    ND[np.isinf(ND)] = np.nan
                    if not os.path.exists(dst_ND):
                        if not os.path.exists(dst_ND_inv): #on observe que a/b = 1/(b/a)
                            with rasterio.open(dst_ND, "w", **profile) as dst:
                                dst.write(ND.astype(rasterio.float64), 1)

                    SR = np.divide(ba, bb)
                    SR[np.isinf(SR)] = np.nan
                    if not os.path.exists(dst_SR):
                            #Pour éviter d'avoir de grosses corrélations entre ces indices, on en créer qu'un sur les deux
                        with rasterio.open(dst_SR, "w", **profile) as dst:
                            dst.write(SR.astype(rasterio.float64), 1)

              # three bands vegetation indices (3BSI / mSR et 3BSI_Tian)
            for elt in itertools.permutations(li_band,3):
                bande1 = elt[0].split("_")[-3]
                bande2 = elt[1].split("_")[-3]
                bande3 = elt[2].split("_")[-3]
                BSI_of = "%s_%s_%s_3BSI_%s.tif" % (bande1, bande2, bande3, x )
                mSR_of = "%s_%s_%s_mSR_%s.tif" % (bande1, bande2, bande3, x )
                mSR_of_inv = "%s_%s_%s_mSR_%s.tif" % (bande1, bande3, bande2, x )
                BSI_Tian_of = "%s_%s_%s_3BSITian_%s.tif" % (bande1, bande2, bande3, x )
                BSI_Tian_of_inv = "%s_%s_%s_3BSITian_%s.tif" % (bande1, bande3, bande2, x )
                CVI_of = "%s_%s_%s_CVI_%s.tif" % (bande1, bande2, bande3, x )
                CVI_of_inv = "%s_%s_%s_CVI_%s.tif" % (bande2, bande1, bande3, x )
                dst_3BSI=os.path.join(rep_destination_finale1,"3BSI", BSI_of)
                dst_MSR=os.path.join(rep_destination_finale1,"mSR", mSR_of)
                dst_MSR_inv=os.path.join(rep_destination_finale1,"mSR", mSR_of_inv)
                dst_BSI_Tian=os.path.join(rep_destination_finale1,"3BSITian", BSI_Tian_of)
                dst_BSI_Tian_inv=os.path.join(rep_destination_finale1,"3BSITian", BSI_Tian_of_inv)
                dst_CVI=os.path.join(rep_destination_finale1,"CVI", CVI_of)
                dst_CVI_inv=os.path.join(rep_destination_finale1,"CVI", CVI_of_inv)
                if(not os.path.exists(dst_3BSI) or (not os.path.exists(dst_MSR) and not os.path.exists(dst_MSR_inv)) or (not os.path.exists(dst_BSI_Tian) and not os.path.exists(dst_BSI_Tian_inv))or(not os.path.exists(dst_CVI) and not os.path.exists(dst_CVI_inv))):
                    with rasterio.open(elt[0], "r") as src:
                        ba1 = src.read(1)
                        profile = src.profile
                        profile.update(
                                dtype=rasterio.float64,
                                count=1,
                                compress='lzw')
                    with rasterio.open(elt[1], "r") as src:
                        bb1 = src.read(1)
                        profile = src.profile
                        profile.update(
                                dtype=rasterio.float64,
                                count=1,
                                compress='lzw')
                    with rasterio.open(elt[2], "r") as src:
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
            with rasterio.open(li_band[0], "r") as src:
                bandeB2 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(li_band[1], "r") as src:
                bandeB3 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(li_band[2], "r") as src:
                bandeB4 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(li_band[3], "r") as src:
                bandeB5 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(li_band[4], "r") as src:
                bandeB6 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(li_band[5], "r") as src:
                bandeB7 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(li_band[6], "r") as src:
                bandeB8 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(li_band[7], "r") as src:
                bandeB8a = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            with rasterio.open(li_band[8], "r") as src:
                bandeB11 = src.read(1)
                profile = src.profile
                profile.update(
                        dtype=rasterio.float64,
                        count=1,
                        compress='lzw')
            rep_destination_finale2=os.path.join(rep_destination_finale1,"indclass")
            ###################################################################
            #Calcul des indices classiques du fichier .xml
            ###################################################################
            #calcul du NDVI
            NDVI = np.divide((1.0*bandeB8 - bandeB4), (bandeB8 + bandeB4))
            NDVI[np.isinf(NDVI)]=np.nan
            if not os.path.exists(os.path.join(rep_destination_finale2,"NDVI_indclass_%s.tif"%(x))):
                with rasterio.open(os.path.join(rep_destination_finale2,"NDVI_indclass_%s.tif"%(x)), "w", **profile) as dst:
                    dst.write(NDVI.astype(rasterio.float64), 1)

            #calcul du GNDVI
            GNDVI = np.divide((1.0*bandeB8 - bandeB3), (bandeB8 + bandeB3))
            GNDVI[np.isinf(GNDVI)]=np.nan
            if not os.path.exists(os.path.join(rep_destination_finale2,"GNDVI_indclass_%s.tif"%(x))):
                with rasterio.open(os.path.join(rep_destination_finale2,"GNDVI_indclass_%s.tif"%(x)), "w", **profile) as dst:
                    dst.write(GNDVI.astype(rasterio.float64), 1)

            #calcul du NDVIre
            NDVIre = np.divide((1.0*bandeB8a - bandeB4), (bandeB8a + bandeB4))
            NDVIre[np.isinf(NDVIre)]=np.nan
            if not os.path.exists(os.path.join(rep_destination_finale2,"NDVIre_indclass_%s.tif"%(x))):
                with rasterio.open(os.path.join(rep_destination_finale2,"NDVIre_indclass_%s.tif"%(x)), "w", **profile) as dst:
                    dst.write(NDVIre.astype(rasterio.float64), 1)

            #calcul du NDI45
            NDI45 = np.divide((1.0*bandeB5 - bandeB4), (bandeB5 + bandeB4))
            NDI45[np.isinf(NDI45)]=np.nan
            if not os.path.exists(os.path.join(rep_destination_finale2,"NDI45_indclass_%s.tif"%(x))):
                with rasterio.open(os.path.join(rep_destination_finale2,"NDI45_indclass_%s.tif"%(x)), "w", **profile) as dst:
                    dst.write(NDI45.astype(rasterio.float64), 1)

            #calcul du NDII
            NDII = np.divide((1.0*bandeB8 - bandeB11), (bandeB8 + bandeB11))
            NDII[np.isinf(NDII)]=np.nan
            if not os.path.exists(os.path.join(rep_destination_finale2,"NDII_indclass_%s.tif"%(x))):
                with rasterio.open(os.path.join(rep_destination_finale2,"NDII_indclass_%s.tif"%(x)), "w", **profile) as dst:
                    dst.write(NDII.astype(rasterio.float64), 1)

            #calcul du NREDI1
            NREDI1 = np.divide((1.0*bandeB6 - bandeB5), (bandeB6 + bandeB5))
            NREDI1[np.isinf(NREDI1)]=np.nan
            if not os.path.exists(os.path.join(rep_destination_finale2,"NREDI1_indclass_%s.tif"%(x))):
                with rasterio.open(os.path.join(rep_destination_finale2,"NREDI1_indclass_%s.tif"%(x)), "w", **profile) as dst:
                    dst.write(NREDI1.astype(rasterio.float64), 1)

            #calcul du NREDI2
            NREDI2 = np.divide((1.0*bandeB7 - bandeB5), (bandeB7 + bandeB5))
            NREDI2[np.isinf(NREDI2)]=np.nan
            if not os.path.exists(os.path.join(rep_destination_finale2,"NREDI2_indclass_%s.tif"%(x))):
                with rasterio.open(os.path.join(rep_destination_finale2,"NREDI2_indclass_%s.tif"%(x)), "w", **profile) as dst:
                    dst.write(NREDI2.astype(rasterio.float64), 1)

            #calcul du NREDI3
            NREDI3 = np.divide((1.0*bandeB7 - bandeB6), (bandeB7 + bandeB6))
            NREDI3[np.isinf(NREDI3)]=np.nan
            if not os.path.exists(os.path.join(rep_destination_finale2,"NREDI3_indclass_%s.tif"%(x))):
                with rasterio.open(os.path.join(rep_destination_finale2,"NREDI3_indclass_%s.tif"%(x)), "w", **profile) as dst:
                    dst.write(NREDI3.astype(rasterio.float64), 1)

            #calcul du PSRI
            PSRI = np.divide((1.0*bandeB4 - bandeB3), (bandeB5))
            PSRI[np.isinf(PSRI)]=np.nan
            if not os.path.exists(os.path.join(rep_destination_finale2,"PSRI_indclass_%s.tif"%(x))):
                with rasterio.open(os.path.join(rep_destination_finale2,"PSRI_indclass_%s.tif"%(x)), "w", **profile) as dst:
                    dst.write(PSRI.astype(rasterio.float64), 1)

            #calcul du MSI
            MSI = np.divide((1.0*bandeB11), (bandeB8))
            MSI[np.isinf(MSI)]=np.nan
            if not os.path.exists(os.path.join(rep_destination_finale2,"MSI_indclass_%s.tif"%(x))):
                with rasterio.open(os.path.join(rep_destination_finale2,"MSI_indclass_%s.tif"%(x)), "w", **profile) as dst:
                    dst.write(MSI.astype(rasterio.float64), 1)

            #calcul du IRECI
            IRECI = np.divide((1.0*bandeB7 - bandeB4), (np.divide(1.0*bandeB5 , bandeB6)))
            IRECI[np.isinf(IRECI)]=np.nan
            if not os.path.exists(os.path.join(rep_destination_finale2,"IRECI_indclass_%s.tif"%(x))):
                with rasterio.open(os.path.join(rep_destination_finale2,"IRECI_indclass_%s.tif"%(x)), "w", **profile) as dst:
                    dst.write(IRECI.astype(rasterio.float64), 1)

            #calcul du MTCI
            MTCI = np.divide((1.0*bandeB8 - bandeB5), (bandeB5 - bandeB4))
            MTCI[np.isinf(MTCI)]=np.nan
            if not os.path.exists(os.path.join(rep_destination_finale2,"MTCI_indclass_%s.tif"%(x))):
                with rasterio.open(os.path.join(rep_destination_finale2,"MTCI_indclass_%s.tif"%(x)), "w", **profile) as dst:
                    dst.write(MTCI.astype(rasterio.float64), 1)

            #calcul du MCARI
            MCARI = np.multiply(((bandeB5 - bandeB4) - (0.2*(bandeB5 - bandeB3))), (bandeB5 - bandeB4))
            MCARI[np.isinf(MCARI)]=np.nan
            if not os.path.exists(os.path.join(rep_destination_finale2,"MCARI_indclass_%s.tif"%(x))):
                with rasterio.open(os.path.join(rep_destination_finale2,"MCARI_indclass_%s.tif"%(x)), "w", **profile) as dst:
                    dst.write(MCARI.astype(rasterio.float64), 1)


if (__name__ == '__main__'):
    root="/mnt/communPSN/Recherche/Herdect/modeles_VA/"
    tuile="T30TXS"
    ferme="85_Etablieres"
    typosat="FRE"
    annee="2020"