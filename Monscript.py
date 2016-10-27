#coding: utf-8

import csv
import requests
from bs4 import BeautifulSoup

#ce script moissonera les données des contrats de 10 000$ et plus conclus par Travaux publics et Services gouvernementaux Canada ou en son nom.

url1="http://www.tpsgc-pwgsc.gc.ca/cgi-bin/proactive/cl.pl?lang=fra;SCR=L;Sort=0;PF=CL201617Q1.txt"
#je crée une variable qui deviendra un fichier csv une fois "imprimé"
fichier="contrats-travaux-public.csv"
#je m'identifie au site Internet pour ne pas avoir l'air louche.
entetes = {
	"User-Agent":"Mélina Soucy - Requête envoyée dans le cadre d'un cours de journalisme informatique Ã  l'UQAM (EDM5240)",
	"From":"melinasoucy0695@gmail.com"
}
#on établi la connexion avec l'url grâce à requests. On accède ainsi au contenu en disant: "Hey, c'est Mélina, je viens en paix"
contenu = requests.get(url1, headers=entetes)
#on demande à la belle soupe d'analyser le contenu textuel du site (html) et de le mettre dans une nouvelle variable: page.
page = BeautifulSoup(contenu.text,"html.parser")
#Je teste la page.
#print(page)
#on crée cette variable pour éviter d'avoir les entêtes des tableaux dans nos données moissonnées.
i=0
#On crée une boucle avec la commande find_all qui va retracer tous les hyperliens de chacune des pages html de la variable page.
for ligne in page.find_all("tr"):
    if i != 0:
        #print(ligne)
        lien = ligne.a.get("href")
        #print(lien)
        hyperlien ="http://www.tpsgc-pwgsc.gc.ca/cgi-bin/proactive/"+lien
        #print(hyperlien)
        contenu2 = requests.get(hyperlien,headers=entetes)
        page2 = BeautifulSoup(contenu2.text, "html.parser")
        
        contrat = []
        #premier item de la liste
        contrat.append(hyperlien)
#on crée une deuxième boucle pour s'assurer d'avoir tous les hyperliens dans les pages html précédentes
        for item in page2.find_all("tr"):
            # print(item)
            if item.td is not None:
                contrat.append(item.td.text)
            
    #certains tableaux sont vides, il faut donc tenir compte de cette observation pour que le script fonctionne       
            else:
                contrat.append(None)
            
            print(contrat)
        

        petit = open(fichier,"a")
        jeremy = csv.writer(petit)
        jeremy.writerow(contrat)
        
    i =+ 1
    #le fichier csv produit par ce code donne tous les url de chacun des contrats octroyés par l'organisme Travaux publics et Services gournementaux Canada
