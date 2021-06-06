# gdpr-web-tracking-regulatory-compliance: A framework of tools and algorithms allowing compliance tests for web tracking techniques under EU data protection regulation (GDPR).
# Author: ©David Martínez. 
# web-beacons-detector.py: This script takes the WEC execution results and locate the used web beacons. It stores the results on the "beacons-detector-results" folder and shows on terminal lots of processed data information. The results contain JSON files with web beacons information and also the automatic generation of 3 diagrams, including web beacons frequency histogram, the top 10 of websites with more web beacons, and the top 10 of tracking web beacon domains.
# TFM algorithm implementation: detector de web beacons.

# IMPORTANT: This script needs to be executed after the WEC inspection 'wec-executor.py', so it's necessary to have an output folder named 'wec-evidences' with the generated inspections.

# Dependencies.
import os
import shutil
import json
import statistics
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# Define the color palette for diagrams.
colors=[
    "#88CCEE",
    "#CC6677",
    "#DDCC77",
    "#117733",
    "#AA4499",
    "#44AA99",
    "#999933",
    "#882255",
    "#661100",
    "#6699CC",
    "#888888"
]

# Functions.

# Function that draws a beacons histogram diagram.
def draw_beacons_histogram(number_of_beacons):
    plt.hist(number_of_beacons,color=colors[0])
    fig = plt.gcf()
    fig.set_size_inches(12, 10)
    plt.xlabel("Web beacons",fontsize=20)
    plt.ylabel("Websites",fontsize=20)
    plt.axvline(n_mean, color='k', linestyle='dashed', linewidth=1)
    plt.savefig('./beacons-detector-results/diagram-beacons-histogram.pdf', format="PDF", bbox_inches='tight')
    plt.clf()

# Function that draws the top 10 websites with more beacons diagram.
def draw_top10_beacons_websites(beacons_dict):
    top_pages = {}
    for website,beacons in beacons_dict.items():
        top_pages[website] = len(beacons)

    # Create a data frame
    df = pd.DataFrame ({
            'Group': top_pages.keys(),
            'Value': top_pages.values()
    })

    # Sort the table
    df = df.sort_values(by=['Value'],ascending=False)
    df = df.head(10)

    sns.set_style("whitegrid")
    plt.rcParams['axes.axisbelow'] = True
    plt.barh(y=df.Group, width=df.Value, align="center",color=colors)

    # Add title
    plt.xlabel("Web beacons",fontsize='xx-large')
    plt.yticks(fontsize='x-large')
    plt.gca().invert_yaxis()

    fig = plt.gcf()
    fig.set_size_inches(12, 6)
    plt.savefig('./beacons-detector-results/diagram-top10-website-beacons.pdf', format="PDF", bbox_inches='tight')
    plt.clf()


# Function that draws the top 10 tracking domains diagram.
def draw_top10_tracking_domains(beacons_parties):
    thirdParty_domains = {}
    for c_parties in beacons_parties.values():
        for c_party in c_parties['thirdParty']:
            if c_party in thirdParty_domains:
                thirdParty_domains[c_party] += 1
            else:
                thirdParty_domains[c_party] = 1

    # Create a data frame
    df = pd.DataFrame ({
            'Group': thirdParty_domains.keys(),
            'Value': thirdParty_domains.values()
    })

    # Sort the table
    df = df.sort_values(by=['Value'],ascending=False)
    df = df.head(10)

    sns.set_style("whitegrid")
    plt.rcParams['axes.axisbelow'] = True
    plt.barh(y=df.Group, width=df.Value, align="center",color=colors)

    # Add title
    plt.xlabel("Websites",fontsize='xx-large')
    plt.yticks(fontsize='x-large')
    plt.gca().invert_yaxis()

    fig = plt.gcf()
    fig.set_size_inches(12, 6)
    plt.savefig('./beacons-detector-results/diagram-top10-tracking-domains.pdf', format="PDF", bbox_inches='tight')
    plt.clf()


# Main code: Web beacon analysis.
#  - For each WEC inspected website, get the list of beacons.
#  - For each WEC inspected website, get the list of third-party beacon domains.

# Dictionary where to store the beacons for each website.
beacons_dict = {}
beacons_parties = {}

# Iterate through each website inspection and load its data.
for subdir, dirs, files in os.walk('./wec-evidences'):
    for dire in dirs:
        with open(subdir+'/'+dire+'/inspection.json') as f:
           data = json.load(f)

        # Iterate through beacons and get interesting information.
        beacons = []
        for beacon in data['beacons']:
            beacon_obj = {
                'listName': beacon['listName'],
                'url': beacon['url']
            }
            beacons.append(beacon_obj)
        beacons_dict[dire] = beacons

        # List of first party and three party beacons.
        parties = {
            'firstParty': data['hosts']['beacons']['firstParty'],
            'thirdParty': data['hosts']['beacons']['thirdParty'],
        }
        beacons_parties[dire] = parties

# Create output directory.
dirpath = Path('beacons-detector-results')
if dirpath.exists() and dirpath.is_dir():
    shutil.rmtree(dirpath)

os.mkdir('beacons-detector-results')

# Store the results to json files.
with open("./beacons-detector-results/beacons-results.json", 'w') as outfile:
    json.dump(beacons_dict, outfile)
with open("./beacons-detector-results/domain-beacons-results.json", 'w') as outfile:
    json.dump(beacons_parties, outfile)

print('\nNumber of WEC inspected websites:',len(beacons_dict.keys()))

# Frequency histogram data.
number_of_beacons = []
max_beacon_website = ""
max_track = 0
for website,beacons in beacons_dict.items():
    number_of_beacons.append(len(beacons))
    if(len(beacons) > max_track):
        max_track = len(beacons)
        max_beacon_website = website

n_mean = sum(number_of_beacons) / len(number_of_beacons)
print('Mean of web beacons for each website:',n_mean)
print('std web beacons for each website:',statistics.stdev(number_of_beacons))
print('Website with more web beacons (',max_track,'):',max_beacon_website)

# Draw beacons frequency histogram.
draw_beacons_histogram(number_of_beacons)
print('\n - Generated beacons histogram: "diagram-beacons-histogram.pdf"')

# Draw beacons top10 websites.
draw_top10_beacons_websites(beacons_dict)
print(' - Generated top10 beacons websites: "diagram-top10-website-beacons.pdf"')

# Draw tracking domains top10.
draw_top10_tracking_domains(beacons_parties)
print(' - Generated top10 tracking domains: "diagram-top10-tracking-domains.pdf"')
