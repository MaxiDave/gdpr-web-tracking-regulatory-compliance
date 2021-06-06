# gdpr-web-tracking-regulatory-compliance: A framework of tools and algorithms allowing compliance tests for web tracking techniques under EU data protection regulation (GDPR).
# Author: ©David Martínez. 
# website-categorizer.py: Tries to categorize automatically the original sample websites based on string matches on website metadata. It generates the file "categorized_websites.json" with the results.
#     It checks patterns on the domain name, website title, 'keywords' and 'description' HTML metadata. 
# TFM algorithm implementation: categoritzador.

# Dependencies.
import json
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

# Functions.

# Checks if an URL exists.
def is_online(url):
    try:
        requests.get(url, timeout=10)
    except:
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


# Function that returns true if the website content 'soup' contains some of the strings 'meta_strings'.
def website_contains(soup, meta_strings):
    tags = []
    if(soup.find("title")):
        tags = [soup.find("title").text.lower()]
    meta_tags = soup.find_all("meta", {"name": lambda x: x in ["description","Description","keywords","Keywords"]})
    meta_property_tags = soup.find_all("meta", {"property": lambda x: x in ["og:description","og:keywords"]})
    try:
        tags += list(map(lambda x: x.attrs['content'].lower(), meta_tags))
    except Exception as e:
        tags += []
    try:
        tags += list(map(lambda x: x.attrs['content'].lower(), meta_property_tags))
    except Exception as e:
        tags += []
    for string in meta_strings:
        for tag in tags:
            if(isinstance(tag, str) and string in tag):
                return True
    return False


# Process incompatible categories
def merge_categories(categories):
    if('adults' in categories):
        return ["adults"]
    elif('shopping' in categories):
        return ["shopping"]
    elif('streaming' in categories):
        return ["streaming"]
    else: 
        return categories


# Function that receives a website and tries to categorize it.
def detect_categories(website, url, strings):
    try:
        # 1. Process the website.
        page_data = requests.get(url, timeout=3.05)
        soup = BeautifulSoup(page_data.content, 'html.parser')
        if soup == "error":
            raise Exception('Error')
        # 2. Detect categories.
        categories = []
        for cat,cat_strings in strings.items():
            meta_strings = cat_strings['meta_strings']
            domain_strings = cat_strings['domain_strings']
            if any(string in website for string in domain_strings) or website_contains(soup, meta_strings):
                categories.append(cat)
        # 3. Return the merged categories.
        return merge_categories(categories)
    except Exception as e:
        print(e)
        return []


# Obtain the websites list and "website-categorizer" strings.
websites = read_websites()['websites']
strings = read_strings()['strings']['website-categorizer']

# Categorize websites.
categorizer_dict = {}
offline_websites = []
uncategorized_websites = []
total = len(websites)
current = 1
for website in websites:
    url = 'https://'+website
    if is_online(url):
        website_categories = detect_categories(website, url, strings)
        if len(website_categories) > 0:
            print('[SUCCESS] - Website',website,'(',current,'/',total,'): ',website_categories)
        else:
            print('[WARN] - Website',website,'(',current,'/',total,'): Cannot parse categories automatically.')
            uncategorized_websites.append(website)
        categorizer_dict[website] = website_categories
    else:
        print('[ERROR] - Website',website,'(',current,'/',total,'): Impossible to establish a connection.')
        offline_websites.append(website)
    current += 1

# Store the result json file.
with open("categorized_websites.json", 'w') as outfile:
    json.dump(categorizer_dict, outfile)

# Print messages.
ok = total-len(uncategorized_websites)
print('\nCategorized',ok,'of',total,'websites. Success ratio:',ok*100/total,'%')
print('Offline websites detected (',len(offline_websites),'): ',offline_websites)
print('Unable to categorize websites (',len(uncategorized_websites),'): ', uncategorized_websites)
print('Generated categorization file: "categorized_websites.json"')