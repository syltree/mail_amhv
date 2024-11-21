# -*- coding: utf-8 -*-

from datetime import datetime
# from pylatex import Document, Section, Subsection, Command
# from pylatex.utils import italic, NoEscape
# Installer le compilateuir latex: sudo apt-get install texlive-pictures texlive-science texlive-latex-extra latexmk

# fonctionne avec le resultat telecharger en csv avec le séparateur ";"  et en mode separe

import sys
from mail import envoieMail
import argparse
import os
import subprocess
import time
import configparser
import re



ListeMailEnvoye="ListeMailEnvoye.txt"
FicConfig="config.ini"
FicAccess="acces.ini"    

def ecrire_log(data):
    fichierLog.write(data + "\n")

def ecire_resume(data):
  fichierResume.write(data+"\n")


# Debut prog
if __name__ == '__main__':
    # Lecture des arguments en ligne de commande
    parser = argparse.ArgumentParser(usage="Envoie un mail aux destainataires du fichier mail.txt ou du fichier spécifié")
    parser.add_argument('-f', type=str, default='./mail.txt', help="Spécifie le fichier mail à traiter, les mails sont soit séparés par un ; soit à la ligne ")
    
    args = parser.parse_args()
    filepath = args.f
    
    fichierLog = open("Log_appel_mail.txt", "a")

    ecrire_log(
        "\n\n\n ***********************   " + datetime.today().strftime("%Y-%m-%d %H:%M") + "   ************ \n\n\n")


    # Recuperation des données des fichiers de config
    pwd_sender=""
    config_acces = configparser.ConfigParser()
    if os.path.exists(FicAccess):
        config_acces.read(FicAccess)
        try:
            pwd_sender=config_acces['acces']['password']
        except KeyError:
            pwd_sender=""
    maConfig = configparser.ConfigParser()
    if not os.path.exists(FicConfig):
        print("ERREUR ---- pas de fichier de configuration")
        quit()
    maConfig.read(FicConfig)
    try:
        sender=maConfig['Mail']['sender']
    except KeyError:
        pwd_sender=""
        ecrire_log("ERREUR - Sender non défini dans le fichier init")
    
    try:
        cc=maConfig['Mail']['cc']
    except KeyError:
        cc=""
        ecrire_log("Attention -- Pas de champs cc dans le fichier de config pour le mail")
    
    
    # Demande le password si pas déjà défini
    if pwd_sender=="":
            pwd_sender = input('Mot de passe pour expéditeur %s ? ' % sender)
    
    fichierSource = open(filepath, "r", encoding='UTF-8')
    
    fichierResume=open(ListeMailEnvoye,"a")
           

        # On traite la ligne
    line = fichierSource.readline()
    count = 0
    while line:  # On parcours l'ensemble des lignes
        
        ecrire_log("Nouvelle ligne" + line)
        liste_data = line.split(";")
        
        
        for data in liste_data:  # On parcours les mail de la ligne
            count = count + 1  # compte le nb de mail par envoyé
            mailDestinataire=data
            mailDestinataire=mailDestinataire.rstrip()
            valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', mailDestinataire)
            if not(valid): 
                print("Invalid email address: "+mailDestinataire)
                ecrire_log(mailDestinataire + " Non conforme")
            else:
            
                # Envoie du mail      
                ecrire_log("Envoie du mail à: " + mailDestinataire + " copie: "+cc)
                status, msg = envoieMail(mailDestinataire,"",pwd_sender,sender_user=sender,cc_mail=cc)
                if status:
                            ecrire_log("envoie mail OK ; tempo  ...")
                            ecire_resume(mailDestinataire+"  send the "+datetime.today().strftime("%Y-%m-%d %H:%M"))
                            # Petite tempo pour ne pas risquer de générer un DOS sur le serveur
                            time.sleep(4)
                else:
                            ecrire_log("ERREUR ----- : " + msg)
                            print("Erreur:", msg)
                            _ = input("Appuyer sur Entrée pour continuer ...")
            
                   
                # fin for, colonne suivante
            # Fin test mail valid
       
        
        line = fichierSource.readline()
# fin while, ligne suivante
fichierSource.close()
