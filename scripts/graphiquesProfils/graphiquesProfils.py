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



for index in range(3, nombreIndices):
     
    
    
    tabMEDI = pd.DataFrame(index = datesListe, columns =["MEDI"])
    tabLAND = pd.DataFrame(index = datesListe, columns =["LAND"])
    tabSUB = pd.DataFrame(index = datesListe, columns =["SUB"])
    tabBOIS = pd.DataFrame(index = datesListe, columns =["BOIS"])
    tabECOR = pd.DataFrame(index = datesListe, columns =["ECOR"])
    tabPROD = pd.DataFrame(index = datesListe, columns =["PROD"])
  



    listeMedMEDI = []
    listeMedLAND = []
    listeMedSUB = []
    listeMedBOIS = []
    listeMedECOR = []
    listeMedPROD = []
       
    
    for dt in range(index, len(csvfile), nombreIndices):
        
        nomSortieGraph = csvfile.iloc[index,2]
        
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
        
    tabMEDI = tabMEDI.assign(MEDI=listeMedMEDI)
    tabLAND = tabLAND.assign(LAND=listeMedLAND)
    tabSUB = tabSUB.assign(SUB=listeMedSUB)
    tabBOIS = tabBOIS.assign(BOIS=listeMedBOIS)
    tabECOR = tabECOR.assign(ECOR=listeMedECOR)
    tabPROD = tabPROD.assign(PROD=listeMedPROD)
        
     


#graphique
    
  
    tabMEDI.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabLAND.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabSUB.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabBOIS.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabECOR.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabPROD.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    
    
    tabMEDI.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation MEDI avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TFJ/{nomSortieGraph}_MEDI.png", dpi = 300)
    
  
    
    tabLAND.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil de type de végétation LAND avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TFJ/{nomSortieGraph}_LAND.png", dpi = 300)
    
  
    
    tabSUB.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation SUB avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
    
    plt.savefig(f"sortie/sortieT31TFJ/{nomSortieGraph}_SUB.png", dpi = 300)
    
  
    tabBOIS.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation BOIS avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
    
    plt.savefig(f"sortie/sortieT31TFJ/{nomSortieGraph}_BOIS.png", dpi = 300)
    
  
    tabECOR.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation ECOR avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TFJ/{nomSortieGraph}_ECOR.png", dpi = 300)
    
  
    
    tabPROD.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation PROD avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TFJ/{nomSortieGraph}_PROD.png", dpi = 300)
    
  
    
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




for index in range(3, nombreIndices):
     

    tabSUB = pd.DataFrame(index = datesListe, columns =["SUB"])
    tabECOR = pd.DataFrame(index = datesListe, columns =["ECOR"])

  

    listeMedSUB = []
    listeMedECOR = []

       
    
    for dt in range(index, len(csvfile), nombreIndices):
        
        nomSortieGraph = csvfile.iloc[index,2]
        
     
        listeSUB = []
        listeECOR = []
        

    
        
        for c in range(3, len(csvfile.columns)):
            
                
                
            if csvfile.iloc[2,c] == "SUB":
                listeSUB.append(csvfile.iloc[dt,c])
                
     
                
                
            elif csvfile.iloc[2,c] == "ECOR":
                listeECOR.append(csvfile.iloc[dt,c])
               
                
         

        listeSUBFloat = list(map(float, listeSUB))
        listeECORFloat = list(map(float, listeECOR))


        medianeSUB = statistics.median(listeSUBFloat)
        listeMedSUB.append(medianeSUB)
    
    
        medianeECOR = statistics.median(listeECORFloat)
        listeMedECOR.append(medianeECOR)
    
 
    tabSUB = tabSUB.assign(SUB=listeMedSUB)
    tabECOR = tabECOR.assign(ECOR=listeMedECOR)

        
    
  

#graphique
    
  
   
    tabSUB.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabECOR.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)


    
    tabSUB.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation SUB avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
    
    plt.savefig(f"sortie/sortieT31TFK/{nomSortieGraph}_SUB.png", dpi = 300)
    
  
  
    tabECOR.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation ECOR avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TFK/{nomSortieGraph}_ECOR.png", dpi = 300)
    
  
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



for index in range(3, nombreIndices):
     
    tabQUE = pd.DataFrame(index = datesListe, columns =["QUE"])
    tabNIV = pd.DataFrame(index = datesListe, columns =["NIV"])
    tabNAR = pd.DataFrame(index = datesListe, columns =["NAR"])
    tabHUM = pd.DataFrame(index = datesListe, columns =["HUM"])
    tabENHE = pd.DataFrame(index = datesListe, columns =["ENHE"])
    tabEBOU = pd.DataFrame(index = datesListe, columns =["EBOU"])
    tabBRAC = pd.DataFrame(index = datesListe, columns =["BRAC"])
    tabBOMB = pd.DataFrame(index = datesListe, columns =["BOMB"])
    tabALP = pd.DataFrame(index = datesListe, columns =["ALP"])
    tabLAND = pd.DataFrame(index = datesListe, columns =["LAND"])
    tabSUB = pd.DataFrame(index = datesListe, columns =["SUB"])
    tabECOR = pd.DataFrame(index = datesListe, columns =["ECOR"])
    tabPROD = pd.DataFrame(index = datesListe, columns =["PROD"])
  



    listeMedQUE = []
    listeMedLAND = []
    listeMedSUB = []
    listeMedNIV = []
    listeMedECOR = []
    listeMedPROD = []
    listeMedNAR = []
    listeMedHUM = []
    listeMedENHE = []
    listeMedEBOU = []
    listeMedBRAC = []
    listeMedBOMB = []
    listeMedALP = []
    
    for dt in range(index, len(csvfile), nombreIndices):
        
        nomSortieGraph = csvfile.iloc[index,2]
        
        listeQUE = []
        listeLAND = []
        listeSUB = []
        listeNIV = []
        listeECOR = []
        listePROD = []
        listeNAR = []
        listeHUM = []
        listeENHE = []
        listeEBOU = []
        listeBRAC = []
        listeBOMB = []
        listeALP = []
   
        

    
        
        for c in range(3, len(csvfile.columns)):
            
            
            
            if csvfile.iloc[2,c] == "QUE":
                listeQUE.append(csvfile.iloc[dt,c])
                
                
                
            elif csvfile.iloc[2,c] == "LAND":
                listeLAND.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "SUB":
                listeSUB.append(csvfile.iloc[dt,c])
                
                
                
            elif csvfile.iloc[2,c] == "NIV":
                listeNIV.append(csvfile.iloc[dt,c])
                
                
                
            elif csvfile.iloc[2,c] == "ECOR":
                listeECOR.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "PROD":
                listePROD.append(csvfile.iloc[dt,c])
                
        
            elif csvfile.iloc[2,c] == "HUM":
                listeHUM.append(csvfile.iloc[dt,c])
                
            
            elif csvfile.iloc[2,c] == "ENHE":
                listeENHE.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "EBOU":
                listeEBOU.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "BRAC":
                listeBRAC.append(csvfile.iloc[dt,c])
                
        
            elif csvfile.iloc[2,c] == "BOMB":
                listeBOMB.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "ALP":
                listeALP.append(csvfile.iloc[dt,c])
                
        
        
        
        
        
        

        
        listeQUEFloat = list(map(float, listeQUE))
        listeLANDFloat = list(map(float, listeLAND))
        listeSUBFloat = list(map(float, listeSUB))
        listeNIVFloat = list(map(float, listeNIV))
        listeECORFloat = list(map(float, listeECOR))
        listePRODFloat = list(map(float, listePROD))
        listeHUMFloat = list(map(float, listeHUM))
        listeENHEFloat = list(map(float, listeENHE))
        listeEBOUFloat = list(map(float, listeEBOU))
        listeBRACFloat = list(map(float, listeBRAC))
        listeBOMBFloat = list(map(float, listeBOMB))
        listeALPFloat = list(map(float, listeALP))
        
   
        medianeQUE = statistics.median(listeQUEFloat)
        listeMedQUE.append(medianeQUE)
    
        medianeLAND = statistics.median(listeLANDFloat)
        listeMedLAND.append(medianeLAND)
    
        medianeSUB = statistics.median(listeSUBFloat)
        listeMedSUB.append(medianeSUB)
    
        medianeNIV = statistics.median(listeNIVFloat)
        listeMedNIV.append(medianeNIV)
    
        medianeECOR = statistics.median(listeECORFloat)
        listeMedECOR.append(medianeECOR)
    
        medianePROD = statistics.median(listePRODFloat)
        listeMedPROD.append(medianePROD)
        
        medianeHUM = statistics.median(listeHUMFloat)
        listeMedHUM.append(medianeHUM)
        
        medianeEHNE = statistics.median(listeENHEFloat)
        listeMedEHNE.append(medianeEHNE)
        
        medianeEBOU = statistics.median(listeEBOUFloat)
        listeMedEBOU.append(medianeEBOU)
        
        medianeBRAC = statistics.median(listeBRACFloat)
        listeMedBRAC.append(medianeBRAC)
        
        medianeBOMB = statistics.median(listeBOMBFloat)
        listeMedBOMB.append(medianeBOMB)
        
        medianeALP = statistics.median(listeALPFloat)
        listeMedALP.append(medianeALP)
        
        
    tabQUE = tabQUE.assign(QUE=listeMedQUE)
    tabLAND = tabLAND.assign(LAND=listeMedLAND)
    tabSUB = tabSUB.assign(SUB=listeMedSUB)
    tabNIV = tabNIV.assign(NIV=listeMedNIV)
    tabECOR = tabECOR.assign(ECOR=listeMedECOR)
    tabPROD = tabPROD.assign(PROD=listeMedPROD)
    tabHUM = tabHUM.assign(HUM=listeMedHUM)
    tabEHNE = tabEHNE.assign(EHNE=listeMedEHNE)
    tabEBOU = tabEBOU.assign(EBOU=listeMedEBOU)
    tabBRAC = tabBRAC.assign(BRAC=listeMedBRAC)
    tabBOMB = tabBOMB.assign(BOMB=listeMedBOMB)
    tabALP = tabALP.assign(ALP=listeMedALP)
        
        


#graphique
    
  
    tabQUE.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabLAND.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabSUB.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabNIV.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabECOR.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabPROD.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabHUM.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabEHNE.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabEBOU.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabBRAC.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabBOMB.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabALP.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    
    tabQUE.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation QUE avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TGK/{nomSortieGraph}_QUE.png", dpi = 300)
    
  
    
    tabLAND.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil de type de végétation LAND avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TGK/{nomSortieGraph}_LAND.png", dpi = 300)
    
  
    
    tabSUB.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation SUB avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
    
    plt.savefig(f"sortie/sortieT31TGK/{nomSortieGraph}_SUB.png", dpi = 300)
    
  
    tabNIV.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation NIV avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
    
    plt.savefig(f"sortie/sortieT31TGK/{nomSortieGraph}_NIV.png", dpi = 300)
    
  
    tabECOR.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation ECOR avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TGK/{nomSortieGraph}_ECOR.png", dpi = 300)
    
  
    
    tabPROD.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation PROD avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TGK/{nomSortieGraph}_PROD.png", dpi = 300)
    
    
    tabHUM.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation HUM avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TGK/{nomSortieGraph}_HUM.png", dpi = 300)
    
    tabEHNE.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation EHNE avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TGK/{nomSortieGraph}_EHNE.png", dpi = 300)
    
    tabEBOU.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation EBOU avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TGK/{nomSortieGraph}_EBOU.png", dpi = 300)
    
    tabBRAC.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation BRAC avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TGK/{nomSortieGraph}_BRAC.png", dpi = 300)
    
    tabBOMB.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation BOMB avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TGK/{nomSortieGraph}_BOMB.png", dpi = 300)
    
    tabALP.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation ALP avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TGK/{nomSortieGraph}_ALP.png", dpi = 300)
    
    
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



for index in range(3, nombreIndices):
     
    tabQUE = pd.DataFrame(index = datesListe, columns =["QUE"])
    tabNIV = pd.DataFrame(index = datesListe, columns =["NIV"])
    tabNAR = pd.DataFrame(index = datesListe, columns =["NAR"])
    tabNA = pd.DataFrame(index = datesListe, columns =["NA"])
    tabENHE = pd.DataFrame(index = datesListe, columns =["ENHE"])
    tabBOMB = pd.DataFrame(index = datesListe, columns =["BOMB"])
    tabALP = pd.DataFrame(index = datesListe, columns =["ALP"])
    tabSUB = pd.DataFrame(index = datesListe, columns =["SUB"])
    tabECOR = pd.DataFrame(index = datesListe, columns =["ECOR"])
    tabPROD = pd.DataFrame(index = datesListe, columns =["PROD"])
  



    listeMedQUE = []
    listeMedSUB = []
    listeMedNIV = []
    listeMedECOR = []
    listeMedPROD = []
    listeMedNAR = []
    listeMedNA = []
    listeMedENHE = []
    listeMedBOMB = []
    listeMedALP = []
    
    for dt in range(index, len(csvfile), nombreIndices):
        
        nomSortieGraph = csvfile.iloc[index,2]
        
        listeQUE = []
        listeSUB = []
        listeNIV = []
        listeECOR = []
        listePROD = []
        listeNAR = []
        listeNA = []
        listeENHE = []
        listeBOMB = []
        listeALP = []
   
        

    
        
        for c in range(3, len(csvfile.columns)):
            
            
            
            if csvfile.iloc[2,c] == "QUE":
                listeQUE.append(csvfile.iloc[dt,c])
                

                
            elif csvfile.iloc[2,c] == "SUB":
                listeSUB.append(csvfile.iloc[dt,c])
                
                
                
            elif csvfile.iloc[2,c] == "NIV":
                listeNIV.append(csvfile.iloc[dt,c])
                
                
                
            elif csvfile.iloc[2,c] == "ECOR":
                listeECOR.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "PROD":
                listePROD.append(csvfile.iloc[dt,c])
                
        
            elif csvfile.iloc[2,c] == "NAR":
                listeNAR.append(csvfile.iloc[dt,c])
                
            
            elif csvfile.iloc[2,c] == "NA":
                listeNA.append(csvfile.iloc[dt,c])
                
            
            elif csvfile.iloc[2,c] == "ENHE":
                listeENHE.append(csvfile.iloc[dt,c])
                
         
            elif csvfile.iloc[2,c] == "BOMB":
                listeBOMB.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "ALP":
                listeALP.append(csvfile.iloc[dt,c])
                
        
        
        
        
        
        

        
        listeQUEFloat = list(map(float, listeQUE))
        listeSUBFloat = list(map(float, listeSUB))
        listeNIVFloat = list(map(float, listeNIV))
        listeECORFloat = list(map(float, listeECOR))
        listePRODFloat = list(map(float, listePROD))
        listeNAFloat = list(map(float, listeNA))
        listeENHEFloat = list(map(float, listeENHE))
        listeBOMBFloat = list(map(float, listeBOMB))
        listeALPFloat = list(map(float, listeALP))
        listeNARFloat = list(map(float, listeNAR))
   
        medianeQUE = statistics.median(listeQUEFloat)
        listeMedQUE.append(medianeQUE)
    
    
        medianeSUB = statistics.median(listeSUBFloat)
        listeMedSUB.append(medianeSUB)
    
        medianeNIV = statistics.median(listeNIVFloat)
        listeMedNIV.append(medianeNIV)
    
        medianeECOR = statistics.median(listeECORFloat)
        listeMedECOR.append(medianeECOR)
    
        medianePROD = statistics.median(listePRODFloat)
        listeMedPROD.append(medianePROD)
        
        medianeNA = statistics.median(listeNAFloat)
        listeMedNA.append(medianeNA)
        
        medianeEHNE = statistics.median(listeENHEFloat)
        listeMedEHNE.append(medianeEHNE)
        
        
        medianeBOMB = statistics.median(listeBOMBFloat)
        listeMedBOMB.append(medianeBOMB)
        
        medianeALP = statistics.median(listeALPFloat)
        listeMedALP.append(medianeALP)
        
        medianeNAR = statistics.median(listeNARFloat)
        listeMedNAR.append(medianeNAR)
        
        
    tabQUE = tabQUE.assign(QUE=listeMedQUE)
    tabSUB = tabSUB.assign(SUB=listeMedSUB)
    tabNIV = tabNIV.assign(NIV=listeMedNIV)
    tabECOR = tabECOR.assign(ECOR=listeMedECOR)
    tabPROD = tabPROD.assign(PROD=listeMedPROD)
    tabNA = tabNA.assign(NA=listeMedNA)
    tabEHNE = tabEHNE.assign(EHNE=listeMedEHNE)
    tabBOMB = tabBOMB.assign(BOMB=listeMedBOMB)
    tabALP = tabALP.assign(ALP=listeMedALP)
    tabNAR = tabALP.assign(NAR=listeMedNAR)
        


#graphique
    
  
    tabQUE.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabSUB.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabNIV.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabECOR.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabPROD.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabNA.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabEHNE.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabBOMB.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabALP.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabNAR.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    
    tabQUE.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation QUE avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TGL/{nomSortieGraph}_QUE.png", dpi = 300)
    
  

    
    tabSUB.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation SUB avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
    
    plt.savefig(f"sortie/sortieT31TGL/{nomSortieGraph}_SUB.png", dpi = 300)
    
  
    tabNIV.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation NIV avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
    
    plt.savefig(f"sortie/sortieT31TGL/{nomSortieGraph}_NIV.png", dpi = 300)
    
  
    tabECOR.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation ECOR avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TGL/{nomSortieGraph}_ECOR.png", dpi = 300)
    
  
    
    tabPROD.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation PROD avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TGL/{nomSortieGraph}_PROD.png", dpi = 300)
    
    
    tabNA.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation NA avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TGL/{nomSortieGraph}_NA.png", dpi = 300)
    
    tabEHNE.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation EHNE avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TGL/{nomSortieGraph}_EHNE.png", dpi = 300)
   
    
    tabBOMB.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation BOMB avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TGL/{nomSortieGraph}_BOMB.png", dpi = 300)
    
    tabALP.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation ALP avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TGL/{nomSortieGraph}_ALP.png", dpi = 300)
    
    tabNAR.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation NAR avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT31TGL/{nomSortieGraph}_NAR.png", dpi = 300)
    
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



for index in range(3, nombreIndices):
     
    
    tabNAR = pd.DataFrame(index = datesListe, columns =["NAR"])
    tabBRAC = pd.DataFrame(index = datesListe, columns =["BRAC"])
    tabBOMB = pd.DataFrame(index = datesListe, columns =["BOMB"])
    tabSUB = pd.DataFrame(index = datesListe, columns =["SUB"])
    tabPROD = pd.DataFrame(index = datesListe, columns =["PROD"])
  

    listeMedSUB = []
    listeMedPROD = []
    listeMedNAR = []
    listeMedBRAC = []
    listeMedBOMB = []

    for dt in range(index, len(csvfile), nombreIndices):
        
        nomSortieGraph = csvfile.iloc[index,2]
   
        listeSUB = []
        listePROD = []
        listeNAR = []
        listeBRAC = []
        listeBOMB = []

   
        

    
        
        for c in range(3, len(csvfile.columns)):
            
            
        
                
                
            if csvfile.iloc[2,c] == "SUB":
                listeSUB.append(csvfile.iloc[dt,c])
                

                
            elif csvfile.iloc[2,c] == "PROD":
                listePROD.append(csvfile.iloc[dt,c])
                
        
            elif csvfile.iloc[2,c] == "NAR":
                listeNAR.append(csvfile.iloc[dt,c])
                
            
                
            elif csvfile.iloc[2,c] == "BRAC":
                listeBRAC.append(csvfile.iloc[dt,c])
                
        
            elif csvfile.iloc[2,c] == "BOMB":
                listeBOMB.append(csvfile.iloc[dt,c])
                
   
        
        
        
        
        

      
        listeSUBFloat = list(map(float, listeSUB))
        listePRODFloat = list(map(float, listePROD))
        listeNARFloat = list(map(float, listeNAR))
        listeBRACFloat = list(map(float, listeBRAC))
        listeBOMBFloat = list(map(float, listeBOMB))
        
        
   
    
        medianeSUB = statistics.median(listeSUBFloat)
        listeMedSUB.append(medianeSUB)
    
        medianePROD = statistics.median(listePRODFloat)
        listeMedPROD.append(medianePROD)
        
        medianeNAR = statistics.median(listeHUMFloat)
        listeMedNAR.append(medianeNAR)
        
        medianeBRAC = statistics.median(listeBRACFloat)
        listeMedBRAC.append(medianeBRAC)
        
        medianeBOMB = statistics.median(listeBOMBFloat)
        listeMedBOMB.append(medianeBOMB)
        
       
  
    tabSUB = tabSUB.assign(SUB=listeMedSUB)
    tabPROD = tabPROD.assign(PROD=listeMedPROD)
    tabHUM = tabNAR.assign(NAR=listeMedNAR)
    tabBRAC = tabBRAC.assign(BRAC=listeMedBRAC)
    tabBOMB = tabBOMB.assign(BOMB=listeMedBOMB)
  


#graphique
    
  
    
    tabSUB.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabPROD.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabNAR.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabBRAC.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabBOMB.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
   
    
    
  
    
    tabSUB.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation SUB avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
    
    plt.savefig(f"sortie/sortieT32TLP/{nomSortieGraph}_SUB.png", dpi = 300)
    

    
  
    
    tabPROD.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation PROD avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT32TLP/{nomSortieGraph}_PROD.png", dpi = 300)
    
    
    tabNAR.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation NAR avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT32TLP/{nomSortieGraph}_NAR.png", dpi = 300)
    
    
    tabBRAC.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation BRAC avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT32TLP/{nomSortieGraph}_BRAC.png", dpi = 300)
    
    tabBOMB.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation BOMB avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT32TLP/{nomSortieGraph}_BOMB.png", dpi = 300)
    
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



for index in range(3, nombreIndices):
     
    tabQUE = pd.DataFrame(index = datesListe, columns =["QUE"])
    tabNIV = pd.DataFrame(index = datesListe, columns =["NIV"])
    tabNAR = pd.DataFrame(index = datesListe, columns =["NAR"])
    tabBOMB = pd.DataFrame(index = datesListe, columns =["BOMB"])
    tabALP = pd.DataFrame(index = datesListe, columns =["ALP"])
    tabSUB = pd.DataFrame(index = datesListe, columns =["SUB"])
    tabECOR = pd.DataFrame(index = datesListe, columns =["ECOR"])
    tabPROD = pd.DataFrame(index = datesListe, columns =["PROD"])
  



    listeMedQUE = []
    listeMedSUB = []
    listeMedNIV = []
    listeMedECOR = []
    listeMedPROD = []
    listeMedNAR = []
    listeMedBOMB = []
    listeMedALP = []
    
    for dt in range(index, len(csvfile), nombreIndices):
        
        nomSortieGraph = csvfile.iloc[index,2]
        
        listeQUE = []
        listeSUB = []
        listeNIV = []
        listeECOR = []
        listePROD = []
        listeNAR = []
        listeNA = []
        listeENHE = []
        listeBOMB = []
        listeALP = []
   
        

    
        
        for c in range(3, len(csvfile.columns)):
            
            
            
            if csvfile.iloc[2,c] == "QUE":
                listeQUE.append(csvfile.iloc[dt,c])
                

                
            elif csvfile.iloc[2,c] == "SUB":
                listeSUB.append(csvfile.iloc[dt,c])
                
                
                
            elif csvfile.iloc[2,c] == "NIV":
                listeNIV.append(csvfile.iloc[dt,c])
                
                
                
            elif csvfile.iloc[2,c] == "ECOR":
                listeECOR.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "PROD":
                listePROD.append(csvfile.iloc[dt,c])
                
        
            elif csvfile.iloc[2,c] == "NAR":
                listeNAR.append(csvfile.iloc[dt,c])
                
            
         
            elif csvfile.iloc[2,c] == "BOMB":
                listeBOMB.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "ALP":
                listeALP.append(csvfile.iloc[dt,c])
                
        
        
        
        
        
        

        
        listeQUEFloat = list(map(float, listeQUE))
        listeSUBFloat = list(map(float, listeSUB))
        listeNIVFloat = list(map(float, listeNIV))
        listeECORFloat = list(map(float, listeECOR))
        listePRODFloat = list(map(float, listePROD))
        listeNARFloat = list(map(float, listeNA))
        listeBOMBFloat = list(map(float, listeBOMB))
        listeALPFloat = list(map(float, listeALP))
        
   
        medianeQUE = statistics.median(listeQUEFloat)
        listeMedQUE.append(medianeQUE)
    
    
        medianeSUB = statistics.median(listeSUBFloat)
        listeMedSUB.append(medianeSUB)
    
        medianeNIV = statistics.median(listeNIVFloat)
        listeMedNIV.append(medianeNIV)
    
        medianeECOR = statistics.median(listeECORFloat)
        listeMedECOR.append(medianeECOR)
    
        medianePROD = statistics.median(listePRODFloat)
        listeMedPROD.append(medianePROD)
        
        medianeNAR = statistics.median(listeNARFloat)
        listeMedNAR.append(medianeNAR)
        
        medianeBOMB = statistics.median(listeBOMBFloat)
        listeMedBOMB.append(medianeBOMB)
        
        medianeALP = statistics.median(listeALPFloat)
        listeMedALP.append(medianeALP)
        
        
    tabQUE = tabQUE.assign(QUE=listeMedQUE)
    tabSUB = tabSUB.assign(SUB=listeMedSUB)
    tabNIV = tabNIV.assign(NIV=listeMedNIV)
    tabECOR = tabECOR.assign(ECOR=listeMedECOR)
    tabPROD = tabPROD.assign(PROD=listeMedPROD)
    tabNAR = tabNAR.assign(HUM=listeMedNAR)
    tabBOMB = tabBOMB.assign(BOMB=listeMedBOMB)
    tabALP = tabALP.assign(ALP=listeMedALP)
        
        


#graphique
    
  
    tabQUE.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabSUB.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabNIV.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabECOR.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabPROD.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabNAR.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabBOMB.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabALP.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    
    tabQUE.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation QUE avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT32TLQ/{nomSortieGraph}_QUE.png", dpi = 300)
    
  

    
    tabSUB.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation SUB avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
    
    plt.savefig(f"sortie/sortieT32TLQ/{nomSortieGraph}_SUB.png", dpi = 300)
    
  
    tabNIV.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation NIV avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
    
    plt.savefig(f"sortie/sortieT32TLQ/{nomSortieGraph}_NIV.png", dpi = 300)
    
  
    tabECOR.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation ECOR avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT32TLQ/{nomSortieGraph}_ECOR.png", dpi = 300)
    
  
    
    tabPROD.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation PROD avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT32TLQ/{nomSortieGraph}_PROD.png", dpi = 300)
    
    
    tabNAR.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation NAR avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT32TLQ/{nomSortieGraph}_NAR.png", dpi = 300)
    
   

    
    tabBOMB.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation BOMB avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT32TLQ/{nomSortieGraph}_BOMB.png", dpi = 300)
    
    tabALP.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation ALP avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT32TLQ/{nomSortieGraph}_ALP.png", dpi = 300)
    
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



for index in range(3, nombreIndices):
     
    tabQUE = pd.DataFrame(index = datesListe, columns =["QUE"])
    tabNIV = pd.DataFrame(index = datesListe, columns =["NIV"])
    tabNAR = pd.DataFrame(index = datesListe, columns =["NAR"])
    tabALP = pd.DataFrame(index = datesListe, columns =["ALP"])
    tabENHE = pd.DataFrame(index = datesListe, columns =["ENHE"])
    tabBOMB = pd.DataFrame(index = datesListe, columns =["BOMB"])
    tabPROD = pd.DataFrame(index = datesListe, columns =["PROD"])
  



    listeMedQUE = []
    listeMedNIV = []
    listeMedPROD = []
    listeMedNAR = []
    listeMedENHE = []
    listeMedBOMB = []
    listeMedALP = []
    
    for dt in range(index, len(csvfile), nombreIndices):
        
        nomSortieGraph = csvfile.iloc[index,2]
        
        listeQUE = []
        listeNIV = []
        listePROD = []
        listeNAR = []
        listeENHE = []
        listeBOMB = []
        listeALP = []
   
        

    
        
        for c in range(3, len(csvfile.columns)):
            
            
            
            if csvfile.iloc[2,c] == "QUE":
                listeQUE.append(csvfile.iloc[dt,c])
            
                
                
            elif csvfile.iloc[2,c] == "NIV":
                listeNIV.append(csvfile.iloc[dt,c])
                
                
                
                
            elif csvfile.iloc[2,c] == "PROD":
                listePROD.append(csvfile.iloc[dt,c])
                
        
            elif csvfile.iloc[2,c] == "NAR":
                listeNAR.append(csvfile.iloc[dt,c])
                
            
                
            
            elif csvfile.iloc[2,c] == "ENHE":
                listeENHE.append(csvfile.iloc[dt,c])
                
         
            elif csvfile.iloc[2,c] == "BOMB":
                listeBOMB.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "ALP":
                listeALP.append(csvfile.iloc[dt,c])
                
        
        
        
        
        
        

        
        listeQUEFloat = list(map(float, listeQUE))
        listeNIVFloat = list(map(float, listeNIV))
        listePRODFloat = list(map(float, listePROD))
        listeENHEFloat = list(map(float, listeENHE))
        listeBOMBFloat = list(map(float, listeBOMB))
        listeALPFloat = list(map(float, listeALP))
        listeNARFloat = list(map(float, listeNAR))
   
        medianeQUE = statistics.median(listeQUEFloat)
        listeMedQUE.append(medianeQUE)
    
    
        medianeNIV = statistics.median(listeNIVFloat)
        listeMedNIV.append(medianeNIV)
    
    
        medianePROD = statistics.median(listePRODFloat)
        listeMedPROD.append(medianePROD)
        
        medianeNAR = statistics.median(listeNARFloat)
        listeMedNAR.append(medianeNAR)
        
        medianeEHNE = statistics.median(listeENHEFloat)
        listeMedEHNE.append(medianeEHNE)
        
        
        medianeBOMB = statistics.median(listeBOMBFloat)
        listeMedBOMB.append(medianeBOMB)
        
        medianeALP = statistics.median(listeALPFloat)
        listeMedALP.append(medianeALP)
        
        
    tabQUE = tabQUE.assign(QUE=listeMedQUE)
    tabNIV = tabNIV.assign(NIV=listeMedNIV)
    tabPROD = tabPROD.assign(PROD=listeMedPROD)
    tabEHNE = tabEHNE.assign(EHNE=listeMedEHNE)
    tabBOMB = tabBOMB.assign(BOMB=listeMedBOMB)
    tabALP = tabALP.assign(ALP=listeMedALP)
    tabNAR = tabALP.assign(NAR=listeMedNAR)
        


#graphique
    
  
    tabQUE.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabNIV.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabPROD.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabEHNE.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabBOMB.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabALP.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    tabNAR.fillna(value=None, method="ffill", axis=None, inplace=True, limit=None, downcast=None)
    
    tabQUE.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation QUE avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT32TLR/{nomSortieGraph}_QUE.png", dpi = 300)
    
  
  
    tabNIV.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation NIV avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
    
    plt.savefig(f"sortie/sortieT32TLR/{nomSortieGraph}_NIV.png", dpi = 300)
    

    
  
    
    tabPROD.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation PROD avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT32TLR/{nomSortieGraph}_PROD.png", dpi = 300)
    
    
    
    tabEHNE.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation EHNE avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT32TLR/{nomSortieGraph}_EHNE.png", dpi = 300)
   
    
    tabBOMB.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation BOMB avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT32TLR/{nomSortieGraph}_BOMB.png", dpi = 300)
    
    tabALP.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation ALP avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT32TLR/{nomSortieGraph}_ALP.png", dpi = 300)
    
    tabNAR.plot()
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil du type de végétation NAR avec l'indice \n"+nomSortieGraph+" pour l'année "+annee)
    plt.legend(loc="lower right")
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    plt.savefig(f"sortie/sortieT32TLR/{nomSortieGraph}_NAR.png", dpi = 300)