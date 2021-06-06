# gdpr-web-tracking-regulatory-compliance: A framework of tools and algorithms allowing compliance tests for web tracking techniques under EU data protection regulation (GDPR).
# Author: ©David Martínez. 
# consent-detector.py: It opens all the original sample websites and performs screenshots showing the user consent requirement forms. It generates the folder "consent-detector-results" with the screenshots results.
# TFM algorithm implementation: detector de consentiment.


# Dependencies.
import os
import shutil
import json
import requests
import time
import string
from pathlib import Path
from requests.exceptions import ConnectionError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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


# Function that populates strings.
def populate_strings(keywords):
    keywords_upper = [x.upper() for x in keywords]
    keywords_cap = [x.capitalize() for x in keywords]
    keywords_cap_every = [string.capwords(x) for x in keywords]
    return keywords + keywords_upper + keywords_cap + keywords_cap_every


def make_expression(strings,strings_no):
    strings = populate_strings(strings)
    strings_no = populate_strings(strings_no)
    conditions1 = " or ".join(["contains(text(), '%s')" % keyword for keyword in strings])
    conditions2 = " or ".join(["contains(@aria-label,'%s')" % keyword for keyword in strings])
    conditions3 = " or ".join(["contains(@title,'%s')" % keyword for keyword in strings])
    conditionsNo = " and not".join(["(contains(text(), '%s'))" % keyword for keyword in strings_no])
    return "//*[(%s or %s or %s) and not %s]" % (conditions1,conditions2,conditions3,conditionsNo)


# Function that opens the website and searches for the CMP first and second layers. It performs screenshots.
def detect_consent(url, website, expression):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=chrome_options,executable_path='chromium.chromedriver')
    driver.set_page_load_timeout(10)
    driver.set_window_size(1920, 1080)
    first_ok = False
    second_ok = False
    try:
        driver.get(url)
        time.sleep(2)
        driver.save_screenshot("./consent-detector-results/"+website+"/first-level.png")
        first_ok = True
        elements = driver.find_elements_by_xpath(expression)
        for element in elements:
            try:
                time.sleep(0.2)
                driver.execute_script("window.scroll(0, %s)" % (element.location['y']))
                time.sleep(2)
                element.click()
                time.sleep(0.2)
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(0.2)
                driver.save_screenshot("./consent-detector-results/"+website+"/second-level.png")
                second_ok = True
            except Exception as e:
                pass
        driver.delete_all_cookies()
        driver.quit()
    except Exception as e:
        driver.quit()

    if first_ok and second_ok:
        return True
    else:
        return False


# Main code.
websites = read_websites()['websites']
strings = read_strings()['strings']['consent-detector']
expression = make_expression(strings['personalize_strings'],strings['no_personalize_strings'])

# Create output directory.
dirpath = Path('consent-detector-results')
if dirpath.exists() and dirpath.is_dir():
    shutil.rmtree(dirpath)

os.mkdir('consent-detector-results')

offline_websites = []
total = len(websites)
current = 1
for website in websites:
    url = 'https://'+website
    os.mkdir('consent-detector-results/'+website)
    if is_online(url):
        ok = detect_consent(url, website, expression)
        if ok:
            print('[SUCCESS] - Website',website,'(',current,'/',total,'): CMP screenshots performed.')
        else:
            print('[WARN] - Website',website,'(',current,'/',total,'): Problem performing screenshots.')
    else:
        print('[ERROR] - Website',website,'(',current,'/',total,'): Impossible to establish a connection.')
        offline_websites.append(website)
    current += 1

print('\nOffline websites detected (',len(offline_websites),'): ',offline_websites)
print('Screenshots available in folder: "consent-detector-results"')
