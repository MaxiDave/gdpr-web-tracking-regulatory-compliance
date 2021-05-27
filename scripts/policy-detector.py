# gdpr-web-tracking-regulatory-compliance: A framework of tools and algorithms allowing compliance tests for web tracking techniques under EU data protection regulation (GDPR).
# Author: ©David Martínez. 
# policy-detector.py: Implementation of the policy detector algorithm. 

## 1. 

# Dependencies.
import os
import json
import requests
from requests.exceptions import ConnectionError

# Functions.

# Checks if an URL exists.
def is_online(url):
    try:
        request = requests.get(url)
    except ConnectionError:
        return False
    else:
        return True


# Parses and returns the original sample JSON.
def read_websites():
    try:
        with open('../original_sample.json') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(e)

# Parses and returns the strings JSON.
def read_strings():
    try:
        with open('../assets/strings.json') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(e)


# Main code.
websites = read_websites()['websites']
strings = read_strings()

policies_dict = {}
offline_websites = []
for website in websites:
    url = 'https://'+website
    if is_online(url):
        website_value = {}
        #website_value['privacy_policy'] = detect_privacy_policy(url, website, strings)
        #website_value['cookie_policy'] = detect_cookie_policy(url, website, strings)
    else:
        offline_websites.append(website)

print(offline_websites)
print(len(offline_websites))