#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 14:12:01 2021

@author: Emilie SIROT
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
import statistics


####################
####################
### Tuile 31TFJ ####
####################
####################


#temporel

repDonnees = r"../calculIndicesTemporels/sortie/sortieT31TFJ"
repSortie = "sortie/sortieT31TFJ"


fichiersRep = os.listdir(repDonnees)
csvfile = pd.read_csv(os.path.join(repDonnees,fichiersRep[0]), header=0)


#récupérer tous les indices calculés dans le tableau
indices = csvfile['bandes'].unique()
indicesListe = list(indices)
indicesListe.sort()
del indicesListe[0]

#récupérer toutes les dates dans le tableau
dates = csvfile['date'].unique()
datesListe = list(dates)
datesListe.sort()
del datesListe[0]

#récupérer l'année traitée
date = datesListe[0]
splitDate = []
for k in range(0, len(date), 2):
    splitDate.append(date[k : k + 2])

annee = splitDate[0]+splitDate[1]

#calculer le nombre d'indices et le nombre de dates
nombreIndices = len(indicesListe)
nombreDates = len(datesListe)

#type de végétation qui diffère selon les tuiles en fonction des TFE
legendeTabInd = ["MEDI", "LAND","SUB","BOIS","ECOR","PROD"]



for index in range(3, nombreIndices):
     
    tabInd = pd.DataFrame(columns = legendeTabInd, index = datesListe)
    
  
    listeMedMEDI = []
    listeMedLAND = []
    listeMedSUB = []
    listeMedBOIS = []
    listeMedECOR = []
    listeMedPROD = []

    
       
    for dt in range(index, len(csvfile), nombreIndices):
        
        nomSortieGraph = csvfile.iloc[index,2]+".csv"
        
        listeMEDI = []
        listeLAND = []
        listeSUB = []
        listeBOIS = []
        listeECOR = []
        listePROD = []
   
        
    
        
        for c in range(3, len(csvfile.columns)):
            
            
            
            if csvfile.iloc[2,c] == "MEDI":
                listeMEDI.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "LAND":
                listeLAND.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "SUB":
                listeSUB.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "BOIS":
                listeBOIS.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "ECOR":
                listeECOR.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "PROD":
                listePROD.append(csvfile.iloc[dt,c])
        
    

    
        listeMEDIFloat = list(map(float, listeMEDI))
        listeLANDFloat = list(map(float, listeLAND))
        listeSUBFloat = list(map(float, listeSUB))
        listeBOISFloat = list(map(float, listeBOIS))
        listeECORFloat = list(map(float, listeECOR))
        listePRODFloat = list(map(float, listePROD))
        
       
        medianeMEDI = statistics.median(listeMEDIFloat)
        listeMedMEDI.append(medianeMEDI)
        
        medianeLAND = statistics.median(listeLANDFloat)
        listeMedLAND.append(medianeLAND)
        
        medianeSUB = statistics.median(listeSUBFloat)
        listeMedSUB.append(medianeSUB)
        
        medianeBOIS = statistics.median(listeBOISFloat)
        listeMedBOIS.append(medianeBOIS)
        
        medianeECOR = statistics.median(listeECORFloat)
        listeMedECOR.append(medianeECOR)
        
        medianePROD = statistics.median(listePRODFloat)
        listeMedPROD.append(medianePROD)
        
    tabInd = tabInd.assign(MEDI=listeMedMEDI)
    tabInd = tabInd.assign(LAND=listeMedLAND)
    tabInd = tabInd.assign(SUB=listeMedSUB)
    tabInd = tabInd.assign(BOIS=listeMedBOIS)
    tabInd = tabInd.assign(ECOR=listeMedECOR)
    tabInd = tabInd.assign(PROD=listeMedPROD)
        
    #tabInd.to_csv(os.path.join(repSortie,nomSortieGraph), index=False)
    tabInd.to_csv(os.path.join(repSortie,nomSortieGraph))

#graphique
    
  
    tabInd.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabInd.plot()
    
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil des types de végétations avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    
    plt.savefig(f"sortie/sortieT31TFJ/{nomSortieGraph}.png", dpi = 300)
    
  

####################
####################
### Tuile 31TFK ####
####################
####################


#temporel

repDonnees = r"../calculIndicesTemporels/sortie/sortieT31TFK"
repSortie = "sortie/sortieT31TFK"


fichiersRep = os.listdir(repDonnees)
csvfile = pd.read_csv(os.path.join(repDonnees,fichiersRep[0]), header=0)


#récupérer tous les indices calculés dans le tableau
indices = csvfile['bandes'].unique()
indicesListe = list(indices)
indicesListe.sort()
del indicesListe[0]

#récupérer toutes les dates dans le tableau
dates = csvfile['date'].unique()
datesListe = list(dates)
datesListe.sort()
del datesListe[0]

#récupérer l'année traitée
date = datesListe[0]
splitDate = []
for k in range(0, len(date), 2):
    splitDate.append(date[k : k + 2])

annee = splitDate[0]+splitDate[1]

#calculer le nombre d'indices et le nombre de dates
nombreIndices = len(indicesListe)
nombreDates = len(datesListe)

#type de végétation qui diffère selon les tuiles en fonction des TFE
legendeTabInd = ["MEDI", "LAND","SUB","BOIS","ECOR","PROD"]



for index in range(3, nombreIndices):
     
    tabInd = pd.DataFrame(columns = legendeTabInd, index = datesListe)
    
  
    listeMedMEDI = []
    listeMedLAND = []
    listeMedSUB = []
    listeMedBOIS = []
    listeMedECOR = []
    listeMedPROD = []

    
       
    for dt in range(index, len(csvfile), nombreIndices):
        
        nomSortieGraph = csvfile.iloc[index,2]+".csv"
        
        listeMEDI = []
        listeLAND = []
        listeSUB = []
        listeBOIS = []
        listeECOR = []
        listePROD = []
   
        
    
        
        for c in range(3, len(csvfile.columns)):
            
            
            
            if csvfile.iloc[2,c] == "MEDI":
                listeMEDI.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "LAND":
                listeLAND.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "SUB":
                listeSUB.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "BOIS":
                listeBOIS.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "ECOR":
                listeECOR.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "PROD":
                listePROD.append(csvfile.iloc[dt,c])
        
    

    
        listeMEDIFloat = list(map(float, listeMEDI))
        listeLANDFloat = list(map(float, listeLAND))
        listeSUBFloat = list(map(float, listeSUB))
        listeBOISFloat = list(map(float, listeBOIS))
        listeECORFloat = list(map(float, listeECOR))
        listePRODFloat = list(map(float, listePROD))
        
       
        medianeMEDI = statistics.median(listeMEDIFloat)
        listeMedMEDI.append(medianeMEDI)
        
        medianeLAND = statistics.median(listeLANDFloat)
        listeMedLAND.append(medianeLAND)
        
        medianeSUB = statistics.median(listeSUBFloat)
        listeMedSUB.append(medianeSUB)
        
        medianeBOIS = statistics.median(listeBOISFloat)
        listeMedBOIS.append(medianeBOIS)
        
        medianeECOR = statistics.median(listeECORFloat)
        listeMedECOR.append(medianeECOR)
        
        medianePROD = statistics.median(listePRODFloat)
        listeMedPROD.append(medianePROD)
        
    tabInd = tabInd.assign(MEDI=listeMedMEDI)
    tabInd = tabInd.assign(LAND=listeMedLAND)
    tabInd = tabInd.assign(SUB=listeMedSUB)
    tabInd = tabInd.assign(BOIS=listeMedBOIS)
    tabInd = tabInd.assign(ECOR=listeMedECOR)
    tabInd = tabInd.assign(PROD=listeMedPROD)
        
    #tabInd.to_csv(os.path.join(repSortie,nomSortieGraph), index=False)
    tabInd.to_csv(os.path.join(repSortie,nomSortieGraph))

#graphique
    
  
    tabInd.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabInd.plot()
    
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil des types de végétations avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    
    plt.savefig(f"sortie/sortieT31TFK/{nomSortieGraph}.png", dpi = 300)
    
  
    
  
    

####################
####################
### Tuile 31TFK ####
####################
####################


#temporel

repDonnees = r"../calculIndicesTemporels/sortie/sortieT31TFK"
repSortie = "sortie/sortieT31TFK"


fichiersRep = os.listdir(repDonnees)
csvfile = pd.read_csv(os.path.join(repDonnees,fichiersRep[0]), header=0)


#récupérer tous les indices calculés dans le tableau
indices = csvfile['bandes'].unique()
indicesListe = list(indices)
indicesListe.sort()
del indicesListe[0]

#récupérer toutes les dates dans le tableau
dates = csvfile['date'].unique()
datesListe = list(dates)
datesListe.sort()
del datesListe[0]

#récupérer l'année traitée
date = datesListe[0]
splitDate = []
for k in range(0, len(date), 2):
    splitDate.append(date[k : k + 2])

annee = splitDate[0]+splitDate[1]

#calculer le nombre d'indices et le nombre de dates
nombreIndices = len(indicesListe)
nombreDates = len(datesListe)

#type de végétation qui diffère selon les tuiles en fonction des TFE
legendeTabInd = ["SUB","ECOR"]



for index in range(3, nombreIndices):
     
    tabInd = pd.DataFrame(columns = legendeTabInd, index = datesListe)
    
  
   
    listeMedSUB = []
    listeMedECOR = []
    

    
       
    for dt in range(index, len(csvfile), nombreIndices):
        
        nomSortieGraph = csvfile.iloc[index,2]+".csv"
        
        
        listeSUB = []
        listeECOR = []
        
   
        
    
        
        for c in range(3, len(csvfile.columns)):
            
            
            
                
                
            elif csvfile.iloc[2,c] == "SUB":
                listeSUB.append(csvfile.iloc[dt,c])
                
         
                
            elif csvfile.iloc[2,c] == "ECOR":
                listeECOR.append(csvfile.iloc[dt,c])
                
         
        
    

    
        listeSUBFloat = list(map(float, listeSUB))
        listeECORFloat = list(map(float, listeECOR))
  
        
        
        medianeSUB = statistics.median(listeSUBFloat)
        listeMedSUB.append(medianeSUB)
        
      
        
        medianeECOR = statistics.median(listeECORFloat)
        listeMedECOR.append(medianeECOR)
        
    
        
    tabInd = tabInd.assign(SUB=listeMedSUB)

    tabInd = tabInd.assign(ECOR=listeMedECOR)
    
        
    #tabInd.to_csv(os.path.join(repSortie,nomSortieGraph), index=False)
    tabInd.to_csv(os.path.join(repSortie,nomSortieGraph))

#graphique
    
  
    tabInd.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabInd.plot()
    
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil des types de végétations avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    
    plt.savefig(f"sortie/sortieT31TFK/{nomSortieGraph}.png", dpi = 300)
    

####################
####################
### Tuile 31TGK ####
####################
####################


#temporel

repDonnees = r"../calculIndicesTemporels/sortie/sortieT31TGK"
repSortie = "sortie/sortieT31TGK"


fichiersRep = os.listdir(repDonnees)
csvfile = pd.read_csv(os.path.join(repDonnees,fichiersRep[0]), header=0)


#récupérer tous les indices calculés dans le tableau
indices = csvfile['bandes'].unique()
indicesListe = list(indices)
indicesListe.sort()
del indicesListe[0]

#récupérer toutes les dates dans le tableau
dates = csvfile['date'].unique()
datesListe = list(dates)
datesListe.sort()
del datesListe[0]

#récupérer l'année traitée
date = datesListe[0]
splitDate = []
for k in range(0, len(date), 2):
    splitDate.append(date[k : k + 2])

annee = splitDate[0]+splitDate[1]

#calculer le nombre d'indices et le nombre de dates
nombreIndices = len(indicesListe)
nombreDates = len(datesListe)

#type de végétation qui diffère selon les tuiles en fonction des TFE
legendeTabInd = ["SUB","ECOR","ALP","BOMB","BRAC","EBOU","ENHE","HUM","LAND","NAR","NIV","PROD","QUE"]
    tabInd = pd.DataFrame(columns = legendeTabInd, index = datesListe)
    
  
   
    listeMedSUB = []
    listeMedECOR = []
    listeMedALP = []
    listeMedBOMB = []
    listeMedBRAC = []
    listeMedEBOU = []
    listeMedENHE = []   
    listeMedHUM = []
    listeMedLAND = []
    listeMedNAR = []
    listeMedNIV = []
    listeMedPROD = []
    listeMedQUE = []
    
    
    for dt in range(index, len(csvfile), nombreIndices):
        
        nomSortieGraph = csvfile.iloc[index,2]+".csv"
        
        listeSUB = []
        listeECOR = []
        listeALP = []
        listeBOMB = []
        listeBRAC = []
        listeEBOU = []
        listeENHE = []   
        listeHUM = []
        listeLAND = []
        listeNAR = []
        listeNIV = []
        listePROD = []
        listeQUE = []
            
        
   
        
    
        
        for c in range(3, len(csvfile.columns)):
            
            
            
                
                
            elif csvfile.iloc[2,c] == "SUB":
                listeSUB.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "ECOR":
                listeECOR.append(csvfile.iloc[dt,c])
                
         
            elif csvfile.iloc[2,c] == "ALP":
                listeALP.append(csvfile.iloc[dt,c])
        
            elif csvfile.iloc[2,c] == "BOMB":
                listeBOMB.append(csvfile.iloc[dt,c])
        
            elif csvfile.iloc[2,c] == "BRAC":
                listeBRAC.append(csvfile.iloc[dt,c])

    
            elif csvfile.iloc[2,c] == "EBOU":
                listeEBOU.append(csvfile.iloc[dt,c])
                
            elif csvfile.iloc[2,c] == "ENHE":
                listeENHE.append(csvfile.iloc[dt,c])

            elif csvfile.iloc[2,c] == "HUM":
                listeHUM.append(csvfile.iloc[dt,c])

            elif csvfile.iloc[2,c] == "LAND":
                listeLAND.append(csvfile.iloc[dt,c])

            elif csvfile.iloc[2,c] == "NAR":
                listeNAR.append(csvfile.iloc[dt,c])

            elif csvfile.iloc[2,c] == "NIV":
                listeNIV.append(csvfile.iloc[dt,c])

            elif csvfile.iloc[2,c] == "PROD":
                listePROD.append(csvfile.iloc[dt,c])
                
            elif csvfile.iloc[2,c] == "QUE":
                listeQUE.append(csvfile.iloc[dt,c])

        listeSUBFloat = list(map(float, listeSUB))
        listeECORFloat = list(map(float, listeECOR))
        listeALPFloat = list(map(float, listeALP))
        listeBOMBFloat = list(map(float, listeBOMB))
        listeBRACFloat = list(map(float, listeBRAC))
        listeEBOUFloat = list(map(float, listeEBOU))
        listeENHEFloat = list(map(float, listeENHE))
        listeHUMFloat = list(map(float, listeHUM))
        listeLANDFloat = list(map(float, listeLAND))
        listeNARFloat = list(map(float, listeNAR))
        listeNIVFloat = list(map(float, listeNIV))
        listePRODFloat = list(map(float, listePROD))
        listeQUEFloat = list(map(float, listeQUE))
  
        
        
        medianeSUB = statistics.median(listeSUBFloat)
        listeMedSUB.append(medianeSUB)
        
        medianeECOR = statistics.median(listeECORFloat)
        listeMedECOR.append(medianeECOR)
       
        medianeALP = statistics.median(listeALPFloat)
        listeMedALP.append(medianeALP)
        
        medianeBOMB = statistics.median(listeBOMBFloat)
        listeMedBOMB.append(medianeBOMB)
        
        medianeBRAC = statistics.median(listeBRACFloat)
        listeMedBRAC.append(medianeBRAC)
    
        medianeEBOU = statistics.median(listeEBOUFloat)
        listeMedEBOU.append(medianeEBOU)
        
        medianeENHE = statistics.median(listeENHEFloat)
        listeMedENHE.append(medianeENHE)
        
        medianeHUM = statistics.median(listeHUMFloat)
        listeMedHUM.append(medianeHUM)
        
        medianeLAND = statistics.median(listeLANDFloat)
        listeMedLAND.append(medianeLAND)
        
        medianeNAR = statistics.median(listeNARFloat)
        listeMedNAR.append(medianeNAR)
        
        medianeNIV = statistics.median(listeNIVFloat)
        listeMedNIV.append(medianeNIV)
        
        medianePROD = statistics.median(listePRODFloat)
        listeMedPROD.append(medianePROD)
        
        medianeQUE = statistics.median(listeQUEFloat)
        listeMedQUE.append(medianeQUE)
    
        
    tabInd = tabInd.assign(SUB=listeMedSUB)
    tabInd = tabInd.assign(ECOR=listeMedECOR)
    tabInd = tabInd.assign(ALP=listeMedALP)
    tabInd = tabInd.assign(BOMB=listeMedBOMB)
    tabInd = tabInd.assign(BRAC=listeMedBRAC)
    tabInd = tabInd.assign(EBOU=listeMedEBOU)
    tabInd = tabInd.assign(ENHE=listeMedENHE)
    tabInd = tabInd.assign(HUM=listeMedHUM)
    tabInd = tabInd.assign(LAND=listeMedLAND)
    tabInd = tabInd.assign(NAR=listeMedNAR)
    tabInd = tabInd.assign(NIV=listeMedNIV)
    tabInd = tabInd.assign(PROD=listeMedPROD)
    tabInd = tabInd.assign(QUE=listeMedQUE)
    
        
    #tabInd.to_csv(os.path.join(repSortie,nomSortieGraph), index=False)
    tabInd.to_csv(os.path.join(repSortie,nomSortieGraph))

#graphique
    
  
    tabInd.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabInd.plot()
    
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil des types de végétations avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    
    plt.savefig(f"sortie/sortieT31TGK/{nomSortieGraph}.png", dpi = 300)



####################
####################
### Tuile 31TGL ####
####################
####################


#temporel

repDonnees = r"../calculIndicesTemporels/sortie/sortieT31TGL"
repSortie = "sortie/sortieT31TGL"


fichiersRep = os.listdir(repDonnees)
csvfile = pd.read_csv(os.path.join(repDonnees,fichiersRep[0]), header=0)


#récupérer tous les indices calculés dans le tableau
indices = csvfile['bandes'].unique()
indicesListe = list(indices)
indicesListe.sort()
del indicesListe[0]

#récupérer toutes les dates dans le tableau
dates = csvfile['date'].unique()
datesListe = list(dates)
datesListe.sort()
del datesListe[0]

#récupérer l'année traitée
date = datesListe[0]
splitDate = []
for k in range(0, len(date), 2):
    splitDate.append(date[k : k + 2])

annee = splitDate[0]+splitDate[1]

#calculer le nombre d'indices et le nombre de dates
nombreIndices = len(indicesListe)
nombreDates = len(datesListe)

#type de végétation qui diffère selon les tuiles en fonction des TFE
legendeTabInd = ["SUB","ECOR","ALP","BOMB","NA","ENHE","NAR","NIV","PROD","QUE"]
    tabInd = pd.DataFrame(columns = legendeTabInd, index = datesListe)
    
  
   
    listeMedSUB = []
    listeMedECOR = []
    listeMedALP = []
    listeMedBOMB = []
    listeMedNA = []
    listeMedENHE = []   
    listeMedNAR = []
    listeMedNIV = []
    listeMedPROD = []
    listeMedQUE = []
    
    
    for dt in range(index, len(csvfile), nombreIndices):
        
        nomSortieGraph = csvfile.iloc[index,2]+".csv"
        
        listeSUB = []
        listeECOR = []
        listeALP = []
        listeBOMB = []
        listeNA = []
        listeENHE = []   
        listeNAR = []
        listeNIV = []
        listePROD = []
        listeQUE = []
            
        
   
        
    
        
        for c in range(3, len(csvfile.columns)):
            
            
            
                
                
            elif csvfile.iloc[2,c] == "SUB":
                listeSUB.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "ECOR":
                listeECOR.append(csvfile.iloc[dt,c])
                
         
            elif csvfile.iloc[2,c] == "ALP":
                listeALP.append(csvfile.iloc[dt,c])
        
            elif csvfile.iloc[2,c] == "BOMB":
                listeBOMB.append(csvfile.iloc[dt,c])
        
            elif csvfile.iloc[2,c] == "NA":
                listeNA.append(csvfile.iloc[dt,c])

                
            elif csvfile.iloc[2,c] == "ENHE":
                listeENHE.append(csvfile.iloc[dt,c])

            elif csvfile.iloc[2,c] == "NAR":
                listeNAR.append(csvfile.iloc[dt,c])

            elif csvfile.iloc[2,c] == "NIV":
                listeNIV.append(csvfile.iloc[dt,c])

            elif csvfile.iloc[2,c] == "PROD":
                listePROD.append(csvfile.iloc[dt,c])
                
            elif csvfile.iloc[2,c] == "QUE":
                listeQUE.append(csvfile.iloc[dt,c])

        listeSUBFloat = list(map(float, listeSUB))
        listeECORFloat = list(map(float, listeECOR))
        listeALPFloat = list(map(float, listeALP))
        listeBOMBFloat = list(map(float, listeBOMB))
        listeNAFloat = list(map(float, listeNA))
        listeENHEFloat = list(map(float, listeENHE))
        listeNARFloat = list(map(float, listeNAR))
        listeNIVFloat = list(map(float, listeNIV))
        listePRODFloat = list(map(float, listePROD))
        listeQUEFloat = list(map(float, listeQUE))
  
        
        
        medianeSUB = statistics.median(listeSUBFloat)
        listeMedSUB.append(medianeSUB)
        
        medianeECOR = statistics.median(listeECORFloat)
        listeMedECOR.append(medianeECOR)
       
        medianeALP = statistics.median(listeALPFloat)
        listeMedALP.append(medianeALP)
        
        medianeBOMB = statistics.median(listeBOMBFloat)
        listeMedBOMB.append(medianeBOMB)
        
        medianeNA = statistics.median(listeNAFloat)
        listeMedNA.append(medianeNA)
        
        medianeENHE = statistics.median(listeENHEFloat)
        listeMedENHE.append(medianeENHE)
        
        medianeNAR = statistics.median(listeNARFloat)
        listeMedNAR.append(medianeNAR)
        
        medianeNIV = statistics.median(listeNIVFloat)
        listeMedNIV.append(medianeNIV)
        
        medianePROD = statistics.median(listePRODFloat)
        listeMedPROD.append(medianePROD)
        
        medianeQUE = statistics.median(listeQUEFloat)
        listeMedQUE.append(medianeQUE)
    
        
    tabInd = tabInd.assign(SUB=listeMedSUB)
    tabInd = tabInd.assign(ECOR=listeMedECOR)
    tabInd = tabInd.assign(ALP=listeMedALP)
    tabInd = tabInd.assign(BOMB=listeMedBOMB)
    tabInd = tabInd.assign(NA=listeMedNA)
    tabInd = tabInd.assign(ENHE=listeMedENHE)
    tabInd = tabInd.assign(NAR=listeMedNAR)
    tabInd = tabInd.assign(NIV=listeMedNIV)
    tabInd = tabInd.assign(PROD=listeMedPROD)
    tabInd = tabInd.assign(QUE=listeMedQUE)
    
        
    #tabInd.to_csv(os.path.join(repSortie,nomSortieGraph), index=False)
    tabInd.to_csv(os.path.join(repSortie,nomSortieGraph))

#graphique
    
  
    tabInd.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabInd.plot()
    
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil des types de végétations avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    
    plt.savefig(f"sortie/sortieT31TGL/{nomSortieGraph}.png", dpi = 300)
    
    

####################
####################
### Tuile 32TLP ####
####################
####################


#temporel

repDonnees = r"../calculIndicesTemporels/sortie/sortieT32TLP"
repSortie = "sortie/sortieT32TLP"


fichiersRep = os.listdir(repDonnees)
csvfile = pd.read_csv(os.path.join(repDonnees,fichiersRep[0]), header=0)


#récupérer tous les indices calculés dans le tableau
indices = csvfile['bandes'].unique()
indicesListe = list(indices)
indicesListe.sort()
del indicesListe[0]

#récupérer toutes les dates dans le tableau
dates = csvfile['date'].unique()
datesListe = list(dates)
datesListe.sort()
del datesListe[0]

#récupérer l'année traitée
date = datesListe[0]
splitDate = []
for k in range(0, len(date), 2):
    splitDate.append(date[k : k + 2])

annee = splitDate[0]+splitDate[1]

#calculer le nombre d'indices et le nombre de dates
nombreIndices = len(indicesListe)
nombreDates = len(datesListe)

#type de végétation qui diffère selon les tuiles en fonction des TFE
legendeTabInd = ["BOMB","BRAC","NAR","PROD","SUB"]
    tabInd = pd.DataFrame(columns = legendeTabInd, index = datesListe)
    
  
   
    listeMedSUB = []
    listeMedBOMB = []
    listeMedBRAC = []
    listeMedNAR = []
    listeMedPROD = []

    
    
    for dt in range(index, len(csvfile), nombreIndices):
        
        nomSortieGraph = csvfile.iloc[index,2]+".csv"
        
        listeSUB = []
        listeBOMB = []
        listeBRAC = []
        listeNAR = []
        listePROD = []

            

        
        for c in range(3, len(csvfile.columns)):
            
            
            
                
                
            elif csvfile.iloc[2,c] == "SUB":
                listeSUB.append(csvfile.iloc[dt,c])
                
        
            elif csvfile.iloc[2,c] == "BOMB":
                listeBOMB.append(csvfile.iloc[dt,c])
        
            elif csvfile.iloc[2,c] == "BRAC":
                listeBRAC.append(csvfile.iloc[dt,c])


            elif csvfile.iloc[2,c] == "NAR":
                listeNAR.append(csvfile.iloc[dt,c])


            elif csvfile.iloc[2,c] == "PROD":
                listePROD.append(csvfile.iloc[dt,c])
                


        listeSUBFloat = list(map(float, listeSUB))
        listeBOMBFloat = list(map(float, listeBOMB))
        listeBRACFloat = list(map(float, listeBRAC))
        listeNARFloat = list(map(float, listeNAR))
        listePRODFloat = list(map(float, listePROD))

  
        
        
        medianeSUB = statistics.median(listeSUBFloat)
        listeMedSUB.append(medianeSUB)
        
        
        medianeBOMB = statistics.median(listeBOMBFloat)
        listeMedBOMB.append(medianeBOMB)
        
        medianeBRAC = statistics.median(listeBRACFloat)
        listeMedBRAC.append(medianeBRAC)

        
        medianeNAR = statistics.median(listeNARFloat)
        listeMedNAR.append(medianeNAR)
        
        
        medianePROD = statistics.median(listePRODFloat)
        listeMedPROD.append(medianePROD)
        
 
        
    tabInd = tabInd.assign(SUB=listeMedSUB)
    tabInd = tabInd.assign(BOMB=listeMedBOMB)
    tabInd = tabInd.assign(BRAC=listeMedBRAC)
    tabInd = tabInd.assign(NAR=listeMedNAR)
    tabInd = tabInd.assign(PROD=listeMedPROD)
  
    
        
    #tabInd.to_csv(os.path.join(repSortie,nomSortieGraph), index=False)
    tabInd.to_csv(os.path.join(repSortie,nomSortieGraph))

#graphique
    
  
    tabInd.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabInd.plot()
    
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil des types de végétations avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    
    plt.savefig(f"sortie/sortieT32TLP/{nomSortieGraph}.png", dpi = 300)
    

####################
####################
### Tuile 32TLQ ####
####################
####################


#temporel

repDonnees = r"../calculIndicesTemporels/sortie/sortieT32TLQ"
repSortie = "sortie/sortieT32TLQ"


fichiersRep = os.listdir(repDonnees)
csvfile = pd.read_csv(os.path.join(repDonnees,fichiersRep[0]), header=0)


#récupérer tous les indices calculés dans le tableau
indices = csvfile['bandes'].unique()
indicesListe = list(indices)
indicesListe.sort()
del indicesListe[0]

#récupérer toutes les dates dans le tableau
dates = csvfile['date'].unique()
datesListe = list(dates)
datesListe.sort()
del datesListe[0]

#récupérer l'année traitée
date = datesListe[0]
splitDate = []
for k in range(0, len(date), 2):
    splitDate.append(date[k : k + 2])

annee = splitDate[0]+splitDate[1]

#calculer le nombre d'indices et le nombre de dates
nombreIndices = len(indicesListe)
nombreDates = len(datesListe)

#type de végétation qui diffère selon les tuiles en fonction des TFE
legendeTabInd = ["SUB","ECOR","ALP","BOMB","NAR","NIV","PROD","QUE"]
    tabInd = pd.DataFrame(columns = legendeTabInd, index = datesListe)
    
  
   
    listeMedSUB = []
    listeMedECOR = []
    listeMedALP = []
    listeMedBOMB = []
    listeMedNAR = []
    listeMedNIV = []
    listeMedPROD = []
    listeMedQUE = []
    
    
    for dt in range(index, len(csvfile), nombreIndices):
        
        nomSortieGraph = csvfile.iloc[index,2]+".csv"
        
        listeSUB = []
        listeECOR = []
        listeALP = []
        listeBOMB = []
        listeNAR = []
        listeNIV = []
        listePROD = []
        listeQUE = []
            
        
   
        
    
        
        for c in range(3, len(csvfile.columns)):
            
            
            
                
                
            elif csvfile.iloc[2,c] == "SUB":
                listeSUB.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "ECOR":
                listeECOR.append(csvfile.iloc[dt,c])
                
         
            elif csvfile.iloc[2,c] == "ALP":
                listeALP.append(csvfile.iloc[dt,c])
        
            elif csvfile.iloc[2,c] == "BOMB":
                listeBOMB.append(csvfile.iloc[dt,c])
        

            elif csvfile.iloc[2,c] == "NAR":
                listeNAR.append(csvfile.iloc[dt,c])

            elif csvfile.iloc[2,c] == "NIV":
                listeNIV.append(csvfile.iloc[dt,c])

            elif csvfile.iloc[2,c] == "PROD":
                listePROD.append(csvfile.iloc[dt,c])
                
            elif csvfile.iloc[2,c] == "QUE":
                listeQUE.append(csvfile.iloc[dt,c])

        listeSUBFloat = list(map(float, listeSUB))
        listeECORFloat = list(map(float, listeECOR))
        listeALPFloat = list(map(float, listeALP))
        listeBOMBFloat = list(map(float, listeBOMB))
        listeNARFloat = list(map(float, listeNAR))
        listeNIVFloat = list(map(float, listeNIV))
        listePRODFloat = list(map(float, listePROD))
        listeQUEFloat = list(map(float, listeQUE))
  
        
        
        medianeSUB = statistics.median(listeSUBFloat)
        listeMedSUB.append(medianeSUB)
        
        medianeECOR = statistics.median(listeECORFloat)
        listeMedECOR.append(medianeECOR)
       
        medianeALP = statistics.median(listeALPFloat)
        listeMedALP.append(medianeALP)
        
        medianeBOMB = statistics.median(listeBOMBFloat)
        listeMedBOMB.append(medianeBOMB)
        
        medianeNAR = statistics.median(listeNARFloat)
        listeMedNAR.append(medianeNAR)
        
        medianeNIV = statistics.median(listeNIVFloat)
        listeMedNIV.append(medianeNIV)
        
        medianePROD = statistics.median(listePRODFloat)
        listeMedPROD.append(medianePROD)
        
        medianeQUE = statistics.median(listeQUEFloat)
        listeMedQUE.append(medianeQUE)
    
        
    tabInd = tabInd.assign(SUB=listeMedSUB)
    tabInd = tabInd.assign(ECOR=listeMedECOR)
    tabInd = tabInd.assign(ALP=listeMedALP)
    tabInd = tabInd.assign(BOMB=listeMedBOMB)
    tabInd = tabInd.assign(NAR=listeMedNAR)
    tabInd = tabInd.assign(NIV=listeMedNIV)
    tabInd = tabInd.assign(PROD=listeMedPROD)
    tabInd = tabInd.assign(QUE=listeMedQUE)
    
        
    #tabInd.to_csv(os.path.join(repSortie,nomSortieGraph), index=False)
    tabInd.to_csv(os.path.join(repSortie,nomSortieGraph))

#graphique
    
  
    tabInd.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabInd.plot()
    
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil des types de végétations avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    
    plt.savefig(f"sortie/sortieT32TLQ/{nomSortieGraph}.png", dpi = 300)
    
####################
####################
### Tuile 32TLR ####
####################
####################


#temporel

repDonnees = r"../calculIndicesTemporels/sortie/sortieT32TLR"
repSortie = "sortie/sortieT32TLR"


fichiersRep = os.listdir(repDonnees)
csvfile = pd.read_csv(os.path.join(repDonnees,fichiersRep[0]), header=0)


#récupérer tous les indices calculés dans le tableau
indices = csvfile['bandes'].unique()
indicesListe = list(indices)
indicesListe.sort()
del indicesListe[0]

#récupérer toutes les dates dans le tableau
dates = csvfile['date'].unique()
datesListe = list(dates)
datesListe.sort()
del datesListe[0]

#récupérer l'année traitée
date = datesListe[0]
splitDate = []
for k in range(0, len(date), 2):
    splitDate.append(date[k : k + 2])

annee = splitDate[0]+splitDate[1]

#calculer le nombre d'indices et le nombre de dates
nombreIndices = len(indicesListe)
nombreDates = len(datesListe)

#type de végétation qui diffère selon les tuiles en fonction des TFE
legendeTabInd = ["ENHE","ALP","BOMB","NAR","NIV","PROD","QUE"]
    tabInd = pd.DataFrame(columns = legendeTabInd, index = datesListe)
    
  
   

    listeMedENHE = []
    listeMedALP = []
    listeMedBOMB = []
    listeMedNAR = []
    listeMedNIV = []
    listeMedPROD = []
    listeMedQUE = []
    
    
    for dt in range(index, len(csvfile), nombreIndices):
        
        nomSortieGraph = csvfile.iloc[index,2]+".csv"
        
      
        listeENHE = []
        listeALP = []
        listeBOMB = []
        listeNAR = []
        listeNIV = []
        listePROD = []
        listeQUE = []
            
        
   
        
    
        
        for c in range(3, len(csvfile.columns)):
            
            
            
                
            elif csvfile.iloc[2,c] == "ENHE":
                listeECOR.append(csvfile.iloc[dt,c])
                
         
            elif csvfile.iloc[2,c] == "ALP":
                listeALP.append(csvfile.iloc[dt,c])
        
            elif csvfile.iloc[2,c] == "BOMB":
                listeBOMB.append(csvfile.iloc[dt,c])
        

            elif csvfile.iloc[2,c] == "NAR":
                listeNAR.append(csvfile.iloc[dt,c])

            elif csvfile.iloc[2,c] == "NIV":
                listeNIV.append(csvfile.iloc[dt,c])

            elif csvfile.iloc[2,c] == "PROD":
                listePROD.append(csvfile.iloc[dt,c])
                
            elif csvfile.iloc[2,c] == "QUE":
                listeQUE.append(csvfile.iloc[dt,c])

    
        listeENHEFloat = list(map(float, listeENHE))
        listeALPFloat = list(map(float, listeALP))
        listeBOMBFloat = list(map(float, listeBOMB))
        listeNARFloat = list(map(float, listeNAR))
        listeNIVFloat = list(map(float, listeNIV))
        listePRODFloat = list(map(float, listePROD))
        listeQUEFloat = list(map(float, listeQUE))
  
     
        
        medianeENHE = statistics.median(listeENHEFloat)
        listeMedENHE.append(medianeENHE)
       
        medianeALP = statistics.median(listeALPFloat)
        listeMedALP.append(medianeALP)
        
        medianeBOMB = statistics.median(listeBOMBFloat)
        listeMedBOMB.append(medianeBOMB)
        
        medianeNAR = statistics.median(listeNARFloat)
        listeMedNAR.append(medianeNAR)
        
        medianeNIV = statistics.median(listeNIVFloat)
        listeMedNIV.append(medianeNIV)
        
        medianePROD = statistics.median(listePRODFloat)
        listeMedPROD.append(medianePROD)
        
        medianeQUE = statistics.median(listeQUEFloat)
        listeMedQUE.append(medianeQUE)
    
        
  
    tabInd = tabInd.assign(ENHE=listeMedENHE)
    tabInd = tabInd.assign(ALP=listeMedALP)
    tabInd = tabInd.assign(BOMB=listeMedBOMB)
    tabInd = tabInd.assign(NAR=listeMedNAR)
    tabInd = tabInd.assign(NIV=listeMedNIV)
    tabInd = tabInd.assign(PROD=listeMedPROD)
    tabInd = tabInd.assign(QUE=listeMedQUE)
    
        
    #tabInd.to_csv(os.path.join(repSortie,nomSortieGraph), index=False)
    tabInd.to_csv(os.path.join(repSortie,nomSortieGraph))

#graphique
    
  
    tabInd.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabInd.plot()
    
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil des types de végétations avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    
    plt.savefig(f"sortie/sortieT32TLR/{nomSortieGraph}.png", dpi = 300)