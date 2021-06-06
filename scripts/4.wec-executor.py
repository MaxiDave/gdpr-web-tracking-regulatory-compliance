# gdpr-web-tracking-regulatory-compliance: A framework of tools and algorithms allowing compliance tests for web tracking techniques under EU data protection regulation (GDPR).
# Author: ©David Martínez. 
# wec-executor.py: Simple script that automates the WEC execution for the original website sample and organize the results. All inspections will be saved on "wec-evidences" folder, ready to be used on the cookies-detector.py and web-beacons-detector.py scripts.

# IMPORTANT: 'website-evidence-collector' must to be installed in your computer.
#   More information: https://github.com/EU-EDPS/website-evidence-collector

# Dependencies.
import os
import shutil
import json
import subprocess
from pathlib import Path

# Functions.

# Parses and returns the original sample JSON.
def read_websites():
    try:
        with open('../original_sample.json') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(e)


# Main code.
websites = read_websites()['websites']

# Create a directory to store evidence (inspection).
dirpath = Path('wec-evidences')
if dirpath.exists() and dirpath.is_dir():
    shutil.rmtree(dirpath)
else:
    os.mkdir('wec-evidences')

# Loop through all websites and run the WEC.
error = []
total = len(websites)
current = 1
for website in websites:

    # Run the WEC.
    url = 'https://'+website

    try:
        subprocess.check_output(
            "website-evidence-collector -q --overwrite "+url+" -- --ignore-certificate-errors",
            shell=True,
            timeout = 20
        )
    except:
        # Do nothing. If error, ('./output/inspection.json' file will be missing).
        pass

    # Check if inspection file exists, if not try with HTTP.
    ok = True
    if not os.path.isfile('./output/inspection.json'):
        # Run the WEC.
        url = 'http://'+website

        try:
            subprocess.check_output(
                "website-evidence-collector -q --overwrite "+url+" -- --ignore-certificate-errors",
                shell=True,
                timeout = 20
            )
        except:
            # Do nothing. If error, ('./output/inspection.json' file will be missing).
            pass

        # Check if inspection file exists, if not show error.
        if not os.path.isfile('./output/inspection.json'):
            print('  - Cannot inspect webpage: '+website)
            print('[ERROR] - Website',website,'(',current,'/',total,'): Error while inspecting.')
            error.append(website)
            ok = False
    
    if ok:
        # All ok, now create a subfolder inside 'wec-evidences' with the site and copy the 'inspection.json' file and the top and bottom screenshots.
        os.makedirs('wec-evidences/'+website)
        os.rename("./output/inspection.json", "./wec-evidences/"+website+'/inspection.json')
        if os.path.isfile('./output/screenshot-top.png'):
            os.rename("./output/screenshot-top.png", "./wec-evidences/"+website+'/screenshot-top.png')
        if os.path.isfile('./output/screenshot-bottom.png'):
            os.rename("./output/screenshot-bottom.png", "./wec-evidences/"+website+'/screenshot-bottom.png')
        print('[SUCCESS] - Website',website,'(',current,'/',total,'): WEC inspection performed.')
    current += 1

    # Remove the output folder (if exist).
    if os.path.isdir('./output'):
        shutil.rmtree('./output')

print('\nUninspected websites (',len(error),'): ',error)
print('All inspections available in folder: "wec-evidences"')

