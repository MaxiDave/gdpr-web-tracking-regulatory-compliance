# gdpr-web-tracking-regulatory-compliance

A framework of tools and algorithms allowing compliance tests for web tracking techniques under EU data protection regulation (GDPR).

## License

MIT License. See LICENSE.

## Files

- [Download Final Project Report (in Catalan)](TFM_Report.pdf)
- [Download Final Project Presentation (in Catalan)](TFM_Presentation.mp4)
- [Download Repository Video Guide (in Catalan)](video_guide.mp4)

## Assets

The implemented algorithms use the following assets:

- *./assets/easylist.txt:* Protection filter rules (https://easylist.to/). EasyList is the primary filter list that removes most adverts from international webpages, including unwanted frames, images and objects. It is the most popular list used by many ad blockers and forms the basis of over a dozen combination and supplementary filter lists.

- *./assets/easyprivacy.txt:* Protection filter rules (https://easylist.to/). EasyPrivacy is an optional supplementary filter list that completely removes all forms of tracking from the internet, including web bugs, tracking scripts and information collectors, thereby protecting your personal data.

- *./assets/fanboy-annoyance.txt:* Protection filter rules (https://easylist.to/). Fanboy's Annoyance List blocks Social Media content, in-page pop-ups and other annoyances; thereby substantially decreasing web page loading times and uncluttering them. EasyList Cookie List and Fanboy's Social Blocking List are already included, there is no need to subscribe to them if you already have Fanboy's Annoyance List.

- *./assets/fingerprinting_domains.json:* List of known fingerprinting script MD5 hashes, extracted from (Iqbab et al., 2020) (https://arxiv.org/abs/2008.04480).

- *./assets/strings.json:* Strings used to match text patterns, used to detect the policies, buttons, etc. It can be personalized in order to work with websites in other languages.

## Original sample

The original samples in this repository are the same as the ones used in the master's degree final project (original_sample.json).

## Scripts

This public repository contains the following scripts that are the implementations of a master's degree final project algorithms. All of them are implemented on *python*.

- *./scripts/website-categorizer.py:* Tries to categorize automatically the original sample websites based on string matches on website metadata. It uses the 'requests' library to download the websites HTML and the 'BeautifulSoup' library to parse the data. The algorithm checks patterns (see *./assets/strings.json*) on the domain name, website title, 'keywords' and 'description' HTML metadata. It generates the file "categorized_websites.json" with the results, containing an object with the website domains as keys and the list of their categories as values. It implements the *categoritzador* algorithm of the master's degree final project.

- *./scripts/policy-detector.py:* It uses the *selenium* library in order to emulate a Chromium browser and perform automated tasks. It searches text patterns (see *./assets/strings.json*) on the original sample websites in order to locate their privacy policy and the cookie policy. It generates the file "policy_detected.json" with the results, that contains an object list for each website, with information if the policies exist (status: 0) or not (status: 1), if old policies are detected (old: true) and the content of the policies if exist (text: *content*). It also generates the folder "policy-detector-results" with the screenshots of the website main pages and their policy pages if exist. It implements the *detector de polítiques* algorithm of the master's degree final project.

- *./scripts/consent-detector.py:* It uses the *selenium* library in order to emulate a Chromium browser and perform automated tasks. It opens all the original sample websites and performs two screenshots for each website showing the user consent requirement forms, including the first and second layer. It generates the folder "consent-detector-results" with the screenshots results under website domain name subdirectories. It implements the *detector de consentiment* algorithm of the master's degree final project.

- *./scripts/wec-executor.py:* Simple script that automates the WEC execution for the original website sample and organizes the results (*inspection.json* file for each website). All inspections will be saved on "wec-evidences" folder, with the inspector results under website domain name subdirectories. The result data is ready to be used on the *cookies-detector.py* and *web-beacons-detector.py* scripts.

- *./script/cookies-detector.py:* This script takes the WEC execution results and first locate first-party cookies and third-party cookies. Next, it uses the assets protection filters in order to detect tracking cookies (using the library *adblockparser*). Finally, it stores the results on the "cookies-detector-results" folder and shows on terminal lots of processed data information. The results contain JSON files with cookies information and also the automatic generation of 4 diagrams, including cookie types, tracking cookies frequency histogram, the top 10 of websites with more tracking cookies, and the top 10 of tracking cookie domains. It implements the *detector de cookies* algorithm of the master's degree final project. This script needs to be executed after the WEC inspection 'wec-executor.py', so it's necessary to have an output folder named 'wec-evidences' with the generated inspections.

- *./script/web-beacons-detector.py:* This script takes the WEC execution results and locate the used web beacons. It stores the results on the "beacons-detector-results" folder and shows on terminal lots of processed data information. The results contain JSON files with web beacons information and also the automatic generation of 3 diagrams, including web beacons frequency histogram, the top 10 of websites with more web beacons, and the top 10 of tracking web beacon domains. It implements the *detector de web beacons* algorithm of the master's degree final project. This script also needs to be executed after the WEC inspection 'wec-executor.py', so it's necessary to have an output folder named 'wec-evidences' with the generated inspections.

- *./script/GdC-computation.py*: This script takes the results of both theoretical and practical analysis in order to compute the GdC value. It does not generate output files, it prints to the console the sets A, B, Ao, and Bo and also the GdC value. It needs, in the same directory, the file "theoretical_analysis.json" (manually created from the evaluation of the "policy-detector" and "consent-detector" scripts output), the subdirectory "cookies-detector-results" with the results of the "cookies-detector" script, and the subdirectory "beacons-detector-results" with the results of the "web-beacons-detector" script.

## Results

This public repository also contains the results for the original sample (original_sample.json):

- *./results/running-screenshots:* This subdirectory contains several screenshots showing the scripts execution over the original sample:
  - **website-categorizer-1.png**: Image showing the beginning of the "website-categorizer" algorithm execution.
  - **website-categorizer-2.png**: Image showing the end of the "website-categorizer" algorithm execution. The full script execution on the testing environment took around 13 minutes.
  - **policy-detector.png**: Image showing the *policy-detector* algorithm execution. It shows the executing terminal and an example of the privacy policy screenshot. The full script execution on the testing environment took around 3 hours.
  - **consent-detector.png**: Image showing the *consent-detector* algorithm execution. It shows the executing terminal and an example of a website user consent request screenshots (first layer and second layer consent configuration). The full script execution on the testing environment took around 3 hours.
  - **wec-executor.png**: Image showing the *wec-executor* algorithm execution. It shows the executing terminal. The full script execution on the testing environment took around one and a half hours.
  - **cookies-detector.png**: Image showing the *cookies-detector* algorithm execution. It shows all the information printed on the terminal and the cookie types diagram generated. The full script execution on the testing environment took around 4 minutes.
  - **web-beacons-detector.png**: Image showing the *web-beacons-detector* algorithm execution. It shows all the information printed on the terminal and the generated JSON results. The full script execution on the testing environment took around 3 seconds.
  - **gdc-computation-1.png**: Image showing the beginning of the "GdC-computation" script execution. It shows the A and B full sets. 
  - **gdc-computation-2.png**: Image showing the end of the "GdC-computation" script execution. It shows the Ao and Bo sets; the |A|, |B|, |Ao|, and |Bo| values; and finally the GdC value. The full script execution on the testing environment took less than a second.

- *./results/categorized.json*: Original sample categorization. It contains the full *website-categorizer.py* results populated by the manual inspection of non categorized websites. Performance: 76.51 %.

- *./results/policy_detected.json*: File with some of the results of the "policy-detector" algorithm (data) over the original sample. It does not contain the complete output of the algorithm as it contains a lot of data.

- *./results/policy-detector-results*: This subdirectory contains some of the results of the "policy-detector" algorithm  (screenshots) over the original sample. It does not contain the complete output of the algorithm as it contains a lot of data.

- *./results/consent-detector-results*: This subdirectory contains some of the results of the "consent-detector" algorithm (screenshots) over the original sample. It does not contain the complete output of the algorithm as it contains a lot of data.

- *./results/theoretical_analysis.json:* Original sample theoretical analysis results. This file has to be created manually (it's the only manual process). It contains the *policy-detector.py* and *consent-detector.py* results after a manual revision of the algorithms output for the original sample. It's formed by an object with all the analyzed websites in both algorithms as keys. As values, it contains an object with the following keys and values:
  - **has_privacy_policy**: This key has a boolean value (*true* or *false*). It's *true* if the *policy-detector.py* automatically detected that the website has privacy policy or if the manual revision detected that the website has it, *false* otherwise.
  - **has_cookies_policy**: This key has a boolean value (*true* or *false*). It's *true* if the *policy-detector.py* automatically detected that the website has cookie policy or if the manual revision detected that the website has it, *false* otherwise.
  - **privacy_old**:  This key has a boolean value (*true* or *false*). It's *true* if the *policy-detector.py* automatically detected that the website has an old privacy or cookie policy or if the manual revision detected it, *false* otherwise.
  - **consent_type**: This key has a string value, with one of the 7 considered ways to obtain user consent: 'none','no_option','confirm','binary','checkboxes','slider' or 'vendor'. This value has to be manually generated based on the *consent-detector.py* result screenshots analysis.
  - **has_cookies_wall**: This key has a boolean value (*true* or *false*). It's *true* if the manual revision of the *consent-detector.py* website screenshot results shows that the website uses cookie walls, *false* otherwise. This value has to be manually generated based on the *consent-detector.py* result screenshots analysis.
  - **default_active**: This key has a boolean value (*true* or *false*). It's *true* if the manual revision of the *consent-detector.py* website screenshot results shows that the website presents default activated tracking cookies, *false* otherwise. This value has to be manually generated based on the *consent-detector.py* result screenshots analysis.

- *./results/wec-evidences*: This subdirectory contains the full inspection data obtained from the WEC execution ("wec-executor" algorithm) over the original sample, ordered by subdirectories with all the 421 websites names (79 websites could not be inspected by the WEC). This subdirectory is huge (441.4 MB).

- *./results/cookies-detector-results:* This subdirectory contains the full results obtained from the execution of the "cookies-detector" algorithm over the data inspected by the WEC (*./results/wec-evidences*).

- *./results/beacons-detector-results:* This subdirectory contains the full results obtained from the execution of the "web-beacons-detector" algorithm over the data inspected by the WEC (*./results/wec-evidences*).

## Installation

First, clone this repository in your machine, install *python3* (https://realpython.com/installing-python/) and the required dependencies:

```
pip3 install requests pathlib selenium statistics pandas seaborn matplotlib adblockparser bs4
```

Next, execute the desired script from the *scripts* folder.

If you want to use the *web-executor.py* script, you need to install the *website evidence collector* (WEC) software (follow the instructions from: https://github.com/EU-EDPS/website-evidence-collector).

If you want to use the theoretical analysis scripts, such as *policy_detector.py* or *consent-detector.py*, you need to install the Chromium Driver (follow the instructions from: https://makandracards.com/makandra/29465-install-chromedriver-on-linux).

You are ready to rock!
