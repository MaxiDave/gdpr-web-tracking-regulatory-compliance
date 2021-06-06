# gdpr-web-tracking-regulatory-compliance: A framework of tools and algorithms allowing compliance tests for web tracking techniques under EU data protection regulation (GDPR).
# Author: ©David Martínez. 
# policy-detector.py: It searches text patterns on the original sample websites in order to locate their privacy policy and the cookie policy. It generates the file "policy_detected.json" with the results.
# TFM algorithm implementation: detector de polítiques.


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
        requests.get(url, timeout = 10)
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


def make_expression(strings):
    strings = populate_strings(strings)
    conditions1 = " or ".join(["contains(text(), '%s')" % keyword for keyword in strings])
    conditions2 = " or ".join(["contains(@aria-label,'%s')" % keyword for keyword in strings])
    conditions3 = " or ".join(["contains(@title,'%s')" % keyword for keyword in strings])
    return "//*[(%s or %s or %s)]" % (conditions1,conditions2,conditions3)


# Function that opens the website and searches for the policy.
def detect_policy(url, website, strings, expression, name):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=chrome_options,executable_path='chromium.chromedriver')
    driver.set_page_load_timeout(10)
    driver.set_window_size(1920, 1080)
    privacy_object = {}
    try:
        driver.get(url)
        time.sleep(2)
        expression2 = make_expression(strings["close_popups_strings"])
        elements = driver.find_elements_by_xpath(expression2)
        for element in elements:
            try:
                element.click()
            except:
                pass
        time.sleep(2)
        driver.save_screenshot("./policy-detector-results/"+website+"/mainpage.png")
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
                body = driver.find_element_by_tag_name('body')
                privacy_object["status"] = 0
                privacy_object["text"] = body.text
                privacy_object["url"] = driver.current_url
                driver.save_screenshot("./policy-detector-results/"+website+"/"+name+"_policy.png")
                if any(string in privacy_object["text"] for string in strings['old_policies_strings']):
                    privacy_object["old"] = True
                else:
                    privacy_object["old"] = False
            except Exception as e:
                pass
        driver.delete_all_cookies()
        driver.quit()
    except Exception as e:
        driver.quit()

    if "status" not in privacy_object:
        privacy_object["status"] = 1

    return privacy_object


# Main code.
websites = read_websites()['websites']
strings = read_strings()['strings']['policy-detector']
expression_policy = make_expression(strings['privacy_policy_detect'])
expression_cookie_policy = make_expression(strings['cookie_policy_detect'])

# Create output directory.
dirpath = Path('policy-detector-results')
if dirpath.exists() and dirpath.is_dir():
    shutil.rmtree(dirpath)

os.mkdir('policy-detector-results')

policies_dict = {}
offline_websites = []
total = len(websites)
current = 1
for website in websites:
    url = 'https://'+website
    if is_online(url):
        os.mkdir('policy-detector-results/'+website)
        website_value = {}
        website_value['privacy_policy'] = detect_policy(url, website, strings, expression_policy, "privacy")
        if website_value['privacy_policy']['status'] == 0:
            print('[SUCCESS] - Website',website,'(',current,'/',total,'): Has privacy policy.')
        else:
            print('[WARN] - Website',website,'(',current,'/',total,'): No privacy policy detected.')
        website_value['cookie_policy'] = detect_policy(url, website, strings, expression_cookie_policy, "cookie")
        if website_value['cookie_policy']['status'] == 0:
            print('[SUCCESS] - Website',website,'(',current,'/',total,'): Has independent cookie policy.')
        else:
            print('[WARN] - Website',website,'(',current,'/',total,'): No independent cookie policy detected.')
        policies_dict[website] = website_value
    else:
        print('[ERROR] - Website',website,'(',current,'/',total,'): Impossible to establish a connection.')
        offline_websites.append(website)
    current += 1

# Store the result json file.
with open("policy_detected.json", 'w') as outfile:
    json.dump(policies_dict, outfile)

print('\nOffline websites detected (',len(offline_websites),'): ',offline_websites)
print('Generated policies file: "policy_detected.json"')
