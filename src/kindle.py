#!/usr/local/bin/python3
import logging
import os
import subprocess
import ntpath
import yagmail
from shutil import copyfile
from io import StringIO
import sys

old_stdout = sys.stdout

# Mute output of ebook-convert

logging.disable(logging.CRITICAL)

def email(attachments):

    # Open the file which contains the emails to send to

    with open("../config.txt", "r+") as emails:
        files = os.listdir("./../Converted Books")
        recipients = emails.read().split(",")

        # Send separate emails for all of the attachments to the recipients

        for attachment in attachments:
            yag = yagmail.SMTP(os.getenv("EMAIL"),oauth2_file="./../credentials.json")
            contents = ['', attachment]
            print("Sending email...")
            yag.send(recipients, 'Send book to Kindle', contents)
            print("Email sent.")

# Convert all unconverted .epub files to Kindle compatible .mobi files (in a directory)

def convert():

    # List of file types that are convertible

    convertible = [".epub", ".cbr"]

    # Open the file which contains all of the files that have been converted

    with open("../done.txt", "r+") as done:
        files = os.listdir("./../Books")
        attachments = []

        # Iterate over the files in the directory "Books"

        for file in files:
            old_path = "./../Books/" + file
            filename, ext = os.path.splitext(ntpath.basename(old_path))

            # If we are allowed to convert the files

            if ext in convertible:
                done.seek(0)
                new_path = "./../Converted Books/" + filename + ".mobi"

                # Convert the .epub to .mobi using calibre's ebook-convert command
                # if file hasn't been converted yet

                if file not in done.read() and file[0] != ".":
                    ebook_convert_path = "/Applications/calibre.app/Contents/MacOS/ebook-convert"
                    print("Converting file...")
                    command = ebook_convert_path + " \"" + os.path.abspath(old_path) + "\" \"" + os.path.abspath(new_path) + "\""
                    listCommand = [ebook_convert_path, os.path.abspath(old_path), os.path.abspath(new_path)]
                    result = StringIO()
                    sys.stdout = result
                    output = subprocess.check_output(command, shell=True)
                    sys.stdout = old_stdout
                    attachments.append(new_path)
                    done.write(file + "\n")
                    done.seek(0)
                    print("Converted.")

                else:
                    continue

            # If we don't need to convert the file, just add its path into the list attachments

            else:
                done.seek(0)
                new_path = "./../Converted Books/" + filename + ext

                if file not in done.read() and file[0] != ".":
                    attachments.append(new_path)
                    done.write(file + "\n")
                    done.seek(0)
                    copyfile(old_path, new_path)

        # Email our Kindle address with the current attachments

        email(attachments)


convert()


