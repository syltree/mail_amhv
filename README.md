# mail_amhv
Envoie automatique de mail

Programme python avec script d'envoie de mail et script d'appel
L'option -f permet de choisir le fichier de type texte contenant les adresse mails, par défaut le fichier est mail.txt
Le fichier de config config.init contient l'emetteur "sender=" et le champs "cc="
Les logs sont disponibles dans le fichier Log_appel_mail.txt, le fichier n'est jamais nettoyé.
Le fichier ListeMailEnvoye.txt contient l'ensemble des mails envoyés avec la date d'envoie. Il n'est jamais nettoyé.

Le script mail.py permet d'envoyer un fichier joint, passé en, paramètre
