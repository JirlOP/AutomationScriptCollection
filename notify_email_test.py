#! /bin/env python3

"""Script to send emails to users with their credentials"""
# Run example
# python -u [python filename] --smtp_server [smtpserver] --smtp_port [smtpport] --smtp_user [smtpuser] --users_file [csvfilepath] --feedback_email [email]
# python3 -u [python filename] --smtp_server [smtpserver] --smtp_port [smtpport] --smtp_user [smtpuser] --users_file [csvfilepath] --feedback_email [email]

import argparse
import csv
from logging import getLogger
from smtplib import SMTP
from email.mime.text import MIMEText

logger = getLogger()

def notify_users(smtp_server, smtp_port, smtp_user, smtp_password, users_csv_file,
                 feedback_email):
    users = None
    logger.debug(f"Reading users from file {users_csv_file}")
    with open(users_csv_file, "r") as f:
        users = csv.DictReader(f)
        #logger.debug(f"csv read: {json.dumps(users, indent=2)}")

        for user in users:
            name = user["Nombre"]
            username = user["Carne"]
            password = user["ClaveAD"]
            email_to = user["DireccionCorreo"]
            logger.debug(f"emailing {name} at {email_to}")

            text = f"""
Buenas {name},

Como estudiante de la Escuela de Ciencias de la Computación e Informática se le envían las credenciales de su cuenta ECCI:

- Usuario: {username}
- Contraseña: {password}

Con estas credenciales podrá hacer uso de los laboratorios de cómputo de la Escuela, servicio de VPN para acceso a los laboratorios virtuales, plataforma de comunicación, entre otras facilidades.

Se le recomienda cambiar la contraseña brindada después de haber iniciado sesión en alguno de los laboratorios de la Escuela.

En caso de presentar problemas por favor comunicarlos por este medio.

Saludos,
Gestores de Tecnologías de Información
Escuela de Ciencias de la Computación e Informática
Universidad de Costa Rica
            """
            msg = MIMEText(text)
            msg["subject"] = "[ECCI Importante] Información de su cuenta ECCI"
            msg["from"] = "Gestores TI - ECCI<gti.ecci@ucr.ac.cr>"
            msg["to"] = f"{name}<{email_to}>"
            with SMTP(smtp_server, smtp_port) as smtp:
                smtp.starttls()
                smtp.login(smtp_user, smtp_password)
                smtp.sendmail(smtp_user, [email_to, feedback_email], msg.as_string())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smtp_server", type = str, default = "smtp.ucr.ac.cr",
                        help = "SMTP server IP/URL")
    parser.add_argument("--smtp_port", type = int, default = 587,
                        help = "SMTP server's port number")
    parser.add_argument("--smtp_user", type = str, default = "gti.ecci@ucr.ac.cr",
                        help = "SMTP User(an email address)")
    parser.add_argument("--users_file", type = str, required = True,
                        help = "File with users info")
    parser.add_argument("--feedback_email", type = str, default = "gti.ecci@ucr.ac.cr",
                        help = "Email address to send feedback to")
    args = parser.parse_args()

    smtp_password = input("Enter SMTP Password: ")

    notify_users(args.smtp_server, args.smtp_port, args.smtp_user, smtp_password,
                 args.users_file, args.feedback_email)

if __name__ == "__main__":
    main()
