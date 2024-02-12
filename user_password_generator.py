#! /bin/env python3

"""Script to generate passwords for users in a csv file."""

# Run example
# python -u [python filename] --filepath [csvfilepath]
# python3 -u [python filename] --filepath [csvfilepath]

import argparse
import csv
import secrets
import shutil
import string
from tempfile import NamedTemporaryFile

DIGITS_MAX = 2
PASSWORD_LENGTH = 8
SPECIAL_CHARACTERS_MAX = 2
SPECIAL_CHARACTERS = "!$&?"

def generate_password():
    password = ""
    alphabet = string.ascii_letters + string.digits + SPECIAL_CHARACTERS
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(PASSWORD_LENGTH))
        if (any(letter.islower() for letter in password) and
            any(letter.isupper() for letter in password) and
            sum(char.isdigit() for char in password) == DIGITS_MAX and
            sum(not char.isdigit() and not char.isalpha() for char in password)
                == SPECIAL_CHARACTERS_MAX):
            break
    return password


def set_passwords(csvfilename):
    if csvfilename == "":
        raise NameError("File path cannot be empty")

    temp_file = NamedTemporaryFile(mode = 'w', delete = False, newline='')

    with open(csvfilename, 'r', encoding = "utf8") as csvfile, temp_file:
        reader = csv.DictReader(csvfile)
        fieldnames = ['Carne', 'Nombre', 'ClaveAD', 'DireccionCorreo']
        writer = csv.DictWriter(temp_file, fieldnames = fieldnames)
        writer.writeheader()
        for row in reader:
            row['ClaveAD'] = generate_password()
            writer.writerow(row)

    shutil.move(temp_file.name, csvfilename)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filepath", type = str, default = "",
                        help = "Path to csv file with users")
    args = parser.parse_args()
    set_passwords(args.filepath)

if __name__ == "__main__":
    main()


#Me falta agarrar errores y ver como funciona el argparse