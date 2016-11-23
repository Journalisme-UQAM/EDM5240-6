#coding: utf-8

import csv
import requests
from bs4 import BeautifulSoup

url="http://www.tpsgc-pwgsc.gc.ca/cgi-bin/proactive/cl.pl?lang=fra;SCR=L;Sort=0;PF=CL201617Q1.txt"
fichier="contrats-travaux-public-JHR.csv"

entetes = {
	"User-Agent":"Mélina Soucy - Requête envoyée dans le cadre d'un cours de journalisme informatique Ã  l'UQAM (EDM5240)",
	"From":"melinasoucy0695@gmail.com"
}

contenu = requests.get(url, headers=entetes)
page = BeautifulSoup(contenu.text,"html.parser")

i=0

for ligne in page.find_all("tr"):
    if i != 0:
        #print(ligne)
        lien = ligne.a.get("href")
        # print(lien) # Si tu fais afficher la variable «lien», tu vois qu'elle est complète: «http://www.tpsgc-pwgsc.gc.ca/cgi-bin/proactive/cl.pl?lang=fra;SCR=D;Sort=0;PF=CL201617Q1.txt;LN=1642»
        # Il n'est donc pas nécessaire de l'ajouter avec un début d'URL, je place donc la ligne suivant en commentaire
        # hyperlien ="http://www.tpsgc-pwgsc.gc.ca/cgi-bin/proactive/"+lien
        #print(hyperlien)
        contenu2 = requests.get(lien,headers=entetes) # J'ai changé «hyperlien» par «lien»
        page2 = BeautifulSoup(contenu2.text, "html.parser")
        
        contrat = []
        contrat.append(lien) # J'ai changé «hyperlien» par «lien» ici aussi
        # Tout ce qui suit fonctionne désormais
        for item in page2.find_all("tr"):
            # print(item)
            if item.td is not None:
                contrat.append(item.td.text)
            else:
                contrat.append(None)
            
            # print(contrat)

        petit = open(fichier,"a")
        jeremy = csv.writer(petit)
        jeremy.writerow(contrat)

# Dans un des scripts que je vous ai envoyés, j'ai fait une erreur.
# Quand on écrit « =+1 », on dit «la variable est égale à (plus) 1».
# C'est « +=1 » qu'il faut écrire pour augmenter de 1 la valeur d'une variable dans une boucle.
    # i =+ 1
    i += 1