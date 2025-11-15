'''
This python file reads text or PDF files within current directory,
parse the contents according to a special rule to interpret where the new line character might be,
and output to a .htm file.

This script is made so that the pdf content can be used by the html-content-only translator
'''

import os
import re
from pypdf import PdfReader

workingDirectory = os.path.realpath(__file__).split(__file__)[0]

# Switch to the directory where the file is located
if len(workingDirectory) > 0:
    workingDirectory = os.chdir(workingDirectory)

# Supported file type
textTypes = (".txt", ".htm", ".html", ".pdf")
targets = []

# A unique header to remind the script that this file has been modified
header = "<!-- PDF to HTML Modified :3 -->\n<!-- Script by ThDilos -->\n<!DOCTYPE html>\n\t<head></head>\n\t<body>\n\t\t<p>"
foot = "\n\t\t</p>\n\t</body>\n</html>"


# The special rule concluded from experience
patterns = {
    r"([^\r\n])\r?\n([a-z])": r"\1 \2",
    r"\n": r"\n\t\t</p>\n\t\t<br \>\n\t\t<p>\n\t\t\t"
}

# Output the transformed string according to the rule
def transform(string):
    for key, val in patterns.items():
        string = re.sub(key, val, string)
    return string

# Check in current directory: if a txt file is not modified yet (Not containing phrase "# PDF to HTML Modified :3")
for file in os.listdir():
    if file.endswith(textTypes) and os.path.getsize(file) > 0:
        if not file.endswith(".pdf"):
            with open(file, "rb") as textFile:
                currentheader = textFile.readline().decode('utf-8')
                if currentheader != "<!-- PDF to HTML Modified :3 -->\n":
                    targets.append(file)
        # Too lazy to add the PDF check, just include any pdf within target
        else:
            targets.append(file)

if len(targets) == 0:
    print("No File that's ending with " + str(textTypes) + " found at \""+ os.getcwd() + "\"")
else:
    for textFile in targets:
        # The new file's file name (would override the original file that also ends with .htm tho) 
        filenames = textFile.split(".")
        filenames.pop()
        filename = '.'.join(filenames) + ".htm"

        with open(filename, "w") as f:
            wholePassage = ""
            newPassage = ""
            # Use the PdfReader from pypdf library to extract text
            if textFile.endswith(".pdf"):
                reader = PdfReader(textFile)
                for page in reader.pages:
                    wholePassage += page.extract_text()
                newPassage = (header + transform(wholePassage) + foot)
            # Use traditional file reader
            else:
                file = open(textFile, "+br")
                wholePassage = file.read().decode('utf-8')
                file.seek(0)
                file.close()
                newPassage = (header + transform(wholePassage) + foot).encode()

            f.write(newPassage)
        print("Modified " + textFile + " successfully! :3\nResult file saved as " + filename + "\n\n")

# Make sure the command line does not auto close
input("Press Enter to Continue\n")