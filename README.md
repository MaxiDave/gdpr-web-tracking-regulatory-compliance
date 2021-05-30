# gdpr-web-tracking-regulatory-compliance

A framework of tools and algorithms allowing compliance tests for web tracking techniques under EU data protection regulation (GDPR).

## License

MIT License. See LICENSE.

## Assets

The implemented algorithms use the following assets:

- *./assets/easylist.txt:* Protection filter rules (https://easylist.to/). EasyList is the primary filter list that removes most adverts from international webpages, including unwanted frames, images and objects. It is the most popular list used by many ad blockers and forms the basis of over a dozen combination and supplementary filter lists.
- *./assets/easyprivacy.txt:* Protection filter rules (https://easylist.to/). EasyPrivacy is an optional supplementary filter list that completely removes all forms of tracking from the internet, including web bugs, tracking scripts and information collectors, thereby protecting your personal data.
- *./assets/fanboy-annoyance.txt:* Protection filter rules (https://easylist.to/). Fanboy's Annoyance List blocks Social Media content, in-page pop-ups and other annoyances; thereby substantially decreasing web page loading times and uncluttering them. EasyList Cookie List and Fanboy's Social Blocking List are already included, there is no need to subscribe to them if you already have Fanboy's Annoyance List.
- *./assets/fingerprinting_domains.json:* List of known fingerprinting script MD5 hashes, extracted from (Iqbab et al., 2020) (https://arxiv.org/abs/2008.04480).
- *./assets/strings.json:* Strings used to match text patterns, used to detect the policies, buttons, etc. It can be personalized in order to work with websites in other languages.

## Original sample

The original samples in this repository are the same as the ones used in the master's degree final project (original_sample.json). It also includes the full sample categorization results (original_sample_categorized.json).

## Scripts

This public repository contains the following scripts that are the implementations of a master's degree final project algorithms. All of them are implemented on *python*.

- *./scripts/website-categorizer.py:* Tries to categorize automatically the original sample websites based on string matches on website metadata. It checks patterns on the domain name, website title, 'keywords' and 'description' HTML metadata. It generates the file "categorized_websites.json" with the results. It implements the *categoritzador* algorithm of the master's degree final project.
- *./scripts/policy-detector.py:* It searches text patterns on the original sample websites in order to locate their privacy policy and the cookie policy. It generates the file "policy_detected.json" with the results. It implements the *detector de polítiques* algorithm of the master's degree final project.
- *./scripts/consent-detector.py:* It opens all the original sample websites and performs screenshots showing the user consent requirement forms. It generates the folder "consent-detector-results" with the screenshots results. It implements the *detector de consentiment* algorithm of the master's degree final project.
- *./scripts/wec-executor.py:* Simple script that automates the WEC execution for the original website sample and organize the results. All inspections will be saved on "wec-evidences" folder, ready to be used on the *cookies-detector.py* and *web-beacons-detector.py* scripts.
- *./script/cookies-detector.py:* This script takes the WEC execution results and first locate first-party cookies and third-party cookies. Next, it uses the assets protection filters in order to detect tracking cookies. Finally, it stores the results on the "cookies-detector-results" folder and shows on terminal lots of processed data information. The results contain JSON files with cookies information and also the automatic generation of 4 diagrams, including cookie types, tracking cookies frequency histogram, the top 10 of websites with more tracking cookies, and the top 10 of tracking cookie domains. It implements the *detector de cookies* algorithm of the master's degree final project. This script needs to be executed after the WEC inspection 'wec-executor.py', so it's necessary to have an output folder named 'wec-evidences' with the generated inspections.
- *./script/web-beacons-detector.py:* This script takes the WEC execution results and locate the used web beacons. It stores the results on the "beacons-detector-results" folder and shows on terminal lots of processed data information. The results contain JSON files with web beacons information and also the automatic generation of 3 diagrams, including web beacons frequency histogram, the top 10 of websites with more web beacons, and the top 10 of tracking web beacon domains. It implements the *detector de web beacons* algorithm of the master's degree final project. This script also needs to be executed after the WEC inspection 'wec-executor.py', so it's necessary to have an output folder named 'wec-evidences' with the generated inspections.
## Usage

First, clone this repository in your machine and install *python3* (https://realpython.com/installing-python/) and the required dependencies:

```
pip3 install os shutil json requests time string pathlib selenium statistics pandas seaborn matplotlib adblockparser bs4
```

Next, execute the desired script from the *scripts* folder.

If you want to use the *web-executor.py* script, you need to install the *website evidence collector* (WEC) software (follow the instructions from: https://github.com/EU-EDPS/website-evidence-collector).

You are ready to rock!
