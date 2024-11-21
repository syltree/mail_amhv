#!/usr/bin/python3

"""
Librairie pour l'envoie des mails 
Fonction à invoquer: envoieMail
"""

# IMPORTS
#########

import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import re
import os

"""
pip install PyEmail 
"""


# envoie %Mail
def envoieMail(destinataire,nom_pdf,password,sender_user,cc_mail):
    
    # Extrait le nom de contact
    if nom_pdf!="":
        m = re.search(r'inscription_(.+)\.pdf', nom_pdf)
        nom_contact = m.groups(0)[0]
        _, filename_fin = os.path.split(nom_pdf)
    else:
        nom_contact=""
        m=""
    
    
    fournisseur = '@'+sender_user.split('@')[1]
    
    smtp_server = "smtp." + fournisseur[1:]
    port = 587
    sender_email = sender_user
    receiver_email = destinataire  # Enter receiver address
    # Create a secure SSL context
    context = ssl.create_default_context()
    print("Envoie du mail a: " + receiver_email +" par serveur:"+smtp_server)

    # Try to log in to server and send email
    try:

        subject = "Sujet"
        body = """Texte"""

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Cc"] = cc_mail
        #message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        if nom_pdf!="":
            filename = nom_pdf  # In same directory as script

            # Open PDF file in binary mode
            with open(filename, "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email    
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                "attachment; filename= " + filename_fin,
            )

            # Add attachment to message and convert message to string
            message.attach(part)
        
        text = message.as_string()

        # Log in to server using secure context and send email

        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, [receiver_email, cc_mail], text)
            server.quit()

        return True, "Mail envoyé"

    except Exception as e:
        # Print any error messages to stdout
        print("Erreur: ")
        print(e)
        return False, "Erreur"


# Fin envoieMail


if __name__ == '__main__':
    # Simulation de variables globales
    if len(sys.argv) != 4:
        print("## Erreur %d ## usage %s @mail_dest fic_PDF sender_user" % (len(sys.argv),sys.argv[0]))
        sys.exit()

    destinataire = sys.argv[1]
    print(destinataire)
    fic = sys.argv[2]   
    print(fic)
    sender = sys.argv[3]
    print(sender)
    password = input("pwd pour %s ? " % sender)

    # Test envoi PDF
    res, mess = envoieMail(destinataire, "",password,  sender,sender)
    if res:
        print(mess)
    else:
        print("## Erreur ##", mess)

