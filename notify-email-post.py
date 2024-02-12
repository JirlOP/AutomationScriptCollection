#! /bin/env python3

import argparse
import csv
import string
from logging import basicConfig, DEBUG, getLogger
from smtplib import SMTP
from email.mime.text import MIMEText

basicConfig(filename='notify-email.log', filemode='w', level=DEBUG)
logger = getLogger()

def notify_users(smtp_server, smtp_port, smtp_user, smtp_password, users_csv_file):
    users = None
    logger.debug(f"Reading users from file {users_csv_file}")
    with open(users_csv_file, "r") as f:
        users = csv.DictReader(f, delimiter=";")
    #logger.debug(f"csv read: {json.dumps(users, indent=2)}")

        for user in users:
            name = user["Nombre"]
            username = user["Carne"]
            password = user["Password"]
            email_to = user["DireccionCorreo"]
            logger.debug(f"emailing {name} at {email_to}")

            text = f"""
Buenas {name},

Como estudiante del Posgrado de Computación e Informática que está matriculado en cursos de nivelación de la Escuela de Ciencias de la Computación e Informática, se le envían las credenciales de su cuenta ECCI:

- Usuario: {username}
- Contraseña: {password}

Con estas credenciales podrá hacer uso de los laboratorios de cómputo de la Escuela, entre otras facilidades.

Al iniciar sesión en alguno de los laboratorios el sistema le solicitará cambiar la contraseña brindada.

En caso de presentar problemas por favor comunicarlos por este medio.

Saludos,
Gestores de Tecnologías de Información
Escuela de Ciencias de la Computación e Informática
Universidad de Costa Rica
        """
            msg = MIMEText(text)
            msg["subject"] = "[ECCI Importante] Información de su cuenta ECCI"
            msg["from"] = "Gestores TI - ECCI<gti.ecci@ucr.ac.cr>"
            msg["to"] = f"{email_to}"
            with SMTP(smtp_server, smtp_port) as smtp:
                smtp.starttls()
                smtp.login(smtp_user, smtp_password)
                smtp.sendmail("gti.ecci@ucr.ac.cr", [email_to, "ariel.mora@ucr.ac.cr"], msg.as_string())
                # smtp.sendmail("gti.ecci@ucr.ac.cr", ["ariel.mora@ucr.ac.cr"], msg.as_string())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smtp_server", type=str, default="smtp.ucr.ac.cr", help="SMTP server IP/URL")
    parser.add_argument("--smtp_port", type=int, default=587, help="SMTP serverr's port number")
    parser.add_argument("--smtp_user", type=str, required=True, help="SMTP User")
    parser.add_argument("--users_file", type=str, required=True, help="File with users info")
    args = parser.parse_args()

    smtp_password = input("Enter SMTP Password: ")

    notify_users(args.smtp_server, args.smtp_port, args.smtp_user, smtp_password, args.users_file)

if __name__ == "__main__":
    main()
