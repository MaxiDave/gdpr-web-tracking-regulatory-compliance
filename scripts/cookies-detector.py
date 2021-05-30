# gdpr-web-tracking-regulatory-compliance: A framework of tools and algorithms allowing compliance tests for web tracking techniques under EU data protection regulation (GDPR).
# Author: ©David Martínez. 
# cookies-detector.py: This script takes the WEC execution results and first locate first-party cookies and third-party cookies. Next, it uses the assets protection filters in order to detect tracking cookies. Finally, it stores the results on the "cookies-detector-results" folder and shows on terminal lots of processed data information. The results contain JSON files with cookies information and also the automatic generation of 4 diagrams, including cookie types, tracking cookies frequency histogram, the top 10 of websites with more tracking cookies, and the top 10 of tracking cookie domains.
# TFM algorithm implementation: detector de cookies.

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
from adblockparser import AdblockRules

# Load the 3 protection filter rule set as global variables.
easylist = open('../assets/easylist.txt', 'r')
rules_easylist =  AdblockRules(easylist.readlines())

easyprivacy = open('../assets/easyprivacy.txt', 'r')
rules_easyprivacy =  AdblockRules(easyprivacy.readlines())

fanboyannoyance = open('../assets/fanboy-annoyance.txt', 'r')
rules_fanboyannoyance = AdblockRules(fanboyannoyance.readlines())

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

# Function that returns true if the string should be blocked for tracking behaviors.
def should_block(url):
    if rules_easylist.should_block(url, {'third-party': True, 'script': True}):
        return True
    elif rules_easyprivacy.should_block(url, {'third-party': True, 'script': True}):
        return True
    elif rules_fanboyannoyance.should_block(url, {'third-party': True, 'script': True}):
        return True
    else:
        return False


# Checks if the cookie is a tracking cookie according to the blocking filters.
def isTrackingCookie(cookie):
    for file in cookie['files']:
        if should_block(file):
            return True
    return should_block(cookie['domain'])


# Function that draws a cookie types diagram.
def draw_cookie_types(tracking_websites, use_thirdparty, use, nouse):

    # To analyze the websites that use cookies and what types.
    consent_results = {
        'Tracking cookies': len(tracking_websites),
        'Third-party cookies': len(use_thirdparty),
        'Cookies': len(use),
        'Without cookies': len(nouse)
    }

    # Create a data frame
    df = pd.DataFrame ({
            'Group':  consent_results.keys(),
            'Value': consent_results.values()
    })

    # Sort the table
    df = df.sort_values(by=['Value'],ascending=False)
    #ordered_categories = df.Group.tolist()

    sns.set_style("whitegrid")
    plt.rcParams['axes.axisbelow'] = True
    plt.barh(y=df.Group, width=df.Value, align="center",color=colors);

    # Add title
    plt.xlabel("Websites",fontsize='x-large')
    plt.yticks(fontsize='x-large')
    plt.gca().invert_yaxis()

    fig = plt.gcf()
    fig.set_size_inches(12, 2)
    plt.savefig('./cookies-detector-results/diagram-cookie-types.pdf', format="PDF", bbox_inches='tight')
    plt.clf()

# Function that draws a tracking cookies histogram diagram.
def draw_tracking_cookies_histogram(number_of_tracking_cookies):
    plt.hist(number_of_tracking_cookies,color=colors[0])
    fig = plt.gcf()
    fig.set_size_inches(12, 10)
    plt.xlabel("Tracking cookies",fontsize=20)
    plt.ylabel("Websites",fontsize=20)
    plt.axvline(n_mean, color='k', linestyle='dashed', linewidth=1)
    plt.savefig('./cookies-detector-results/diagram-tracking-cookies-histogram.pdf', format="PDF", bbox_inches='tight')
    plt.clf()

# Function that draws the top 10 websites with more tracking cookies diagram.
def draw_top10_tracking_cookies_websites(cookie_dict):
    top_pages = {}
    for website in cookie_dict.keys():
        tracking_list = list(filter(lambda x: x['tracking'], cookie_dict[website]))
        top_pages[website] = len(tracking_list)

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
    plt.xlabel("Tracking cookies",fontsize='xx-large')
    plt.yticks(fontsize='x-large')
    plt.gca().invert_yaxis()

    fig = plt.gcf()
    fig.set_size_inches(12, 6)
    plt.savefig('./cookies-detector-results/diagram-top10-website-tracking-cookies.pdf', format="PDF", bbox_inches='tight')
    plt.clf()


# Function that draws the top 10 tracking domains diagram.
def draw_top10_tracking_domains(cookie_parties):
    thirdParty_domains = {}
    for c_parties in cookie_parties.values():
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
    plt.savefig('./cookies-detector-results/diagram-top10-tracking-domains.pdf', format="PDF", bbox_inches='tight')
    plt.clf()


# Main code: Cookie analysis.
#  - For each WEC inspected website, get the list of first-party and third-party cookies.
#  - For each WEC inspected website, get the list of tracking cookies according to protection filter rules.
#  - For each WEC inspected website, get the list of third-party cookie domains.

# Dictionary where to store the cookies for each website.
cookie_dict = {}
cookie_parties = {}

# Iterate through each website inspection and load its data.
for subdir, dirs, files in os.walk('./wec-evidences'):
    for dire in dirs:
        with open(subdir+'/'+dire+'/inspection.json') as f:
           data = json.load(f)

        # Iterate through cookies and get interesting information.
        cookies = []
        for cookie in data['cookies']:
            cookie_obj = {
                'name': cookie['name'],
                'domain': cookie['domain'],
                'expires': cookie['expires']
            }
            if cookie_obj['expires'] != -1 and 'expiresDays' in cookie:
                cookie_obj['expiresDays'] = cookie['expiresDays']
            files = []
            if 'log' in cookie and 'stack' in cookie['log']:
                for item in cookie['log']['stack']:
                    if 'fileName' in item and item['fileName'] not in files:
                        files.append(item['fileName'])
            cookie_obj['files'] = files
            
            # Check if the cookie is considered tracking cookie.
            cookie_obj['tracking'] = isTrackingCookie(cookie_obj)
            
            cookies.append(cookie_obj)
        cookie_dict[dire] = cookies

        # List of first party and three party cookies.
        parties = {
            'firstParty': data['hosts']['cookies']['firstParty'],
            'thirdParty': data['hosts']['cookies']['thirdParty'],
        }
        cookie_parties[dire] = parties

# Create output directory.
dirpath = Path('cookies-detector-results')
if dirpath.exists() and dirpath.is_dir():
    shutil.rmtree(dirpath)

os.mkdir('cookies-detector-results')

# Store the results to json files.
with open("./cookies-detector-results/cookie-results.json", 'w') as outfile:
    json.dump(cookie_dict, outfile)
with open("./cookies-detector-results/domain-cookie-results.json", 'w') as outfile:
    json.dump(cookie_parties, outfile)

print('\nNumber of WEC inspected websites:',len(cookie_dict.keys()))

# Obtain how many websites use tracking cookies.
tracking_websites = []
notracking_websites = []
use_thirdparty = []
nouse_thirdparty = []
use = []
nouse = []
for website in cookie_dict.keys():
    tracking = any(cookie['tracking'] for cookie in cookie_dict[website])
    if tracking:
        tracking_websites.append(website)
    else:
        notracking_websites.append(website)
        
    if len(cookie_parties[website]['thirdParty']) > 0:
        use_thirdparty.append(website)
    else:
        nouse_thirdparty.append(website)
        
    if len(cookie_parties[website]['thirdParty']) == 0 and len(cookie_parties[website]['firstParty']) == 0:
        nouse.append(website)
    else:
        use.append(website)

total = len(notracking_websites)+len(tracking_websites)
print('\nNumber of websites with no cookies (no consent):',len(nouse))
print('Number of websites with cookies (no consent):',len(use))
print('Percentage of websites that use cookies:',len(use)*100/total)
print()
print('Number of websites without third-party cookies (no consent):',len(nouse_thirdparty))
print('Number of websites with third-party cookies (no consent):',len(use_thirdparty))
print('Percentage of websites that use third-party cookies without consent:',len(use_thirdparty)*100/total)
print()
print('Number of websites without tracking cookies (no consent):',len(notracking_websites))
print('Number of websites with tracking cookies (no consent):',len(tracking_websites))
print('Percentage of websites that use tracking cookies without consent:',len(tracking_websites)*100/total)
print()

# Frequency histogram data.
number_of_tracking_cookies = []
max_track_website = ""
max_track = 0
for website in cookie_dict.keys():
    tracking_list = list(filter(lambda x: x['tracking'], cookie_dict[website]))
    number_of_tracking_cookies.append(len(tracking_list))
    if(len(tracking_list) > max_track):
        max_track = len(tracking_list)
        max_track_website = website

n_mean = sum(number_of_tracking_cookies) / len(number_of_tracking_cookies)
print('Mean of tracking cookies for each website:',n_mean)
print('std tracking cookies for each website:',statistics.stdev(number_of_tracking_cookies))
print('Website with more tracking cookies (',max_track,'):',max_track_website)

# Draw cookie type diagram.
draw_cookie_types(tracking_websites, use_thirdparty, use, nouse)
print('\n - Generated cookie type diagram: "diagram-cookie-types.pdf"')

# Draw tracking cookies frequency histogram.
draw_tracking_cookies_histogram(number_of_tracking_cookies)
print(' - Generated tracking cookies histogram: "diagram-tracking-cookies-histogram.pdf"')

# Draw tracking cookies top10 websites.
draw_top10_tracking_cookies_websites(cookie_dict)
print(' - Generated top10 tracking cookies websites: "diagram-top10-website-tracking-cookies.pdf"')

# Draw tracking domains top10.
draw_top10_tracking_domains(cookie_parties)
print(' - Generated top10 tracking domains: "diagram-top10-tracking-domains.pdf"')
