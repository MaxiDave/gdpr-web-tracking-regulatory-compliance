# gdpr-web-tracking-regulatory-compliance: A framework of tools and algorithms allowing compliance tests for web tracking techniques under EU data protection regulation (GDPR).
# Author: ©David Martínez. 
# GdC-computation.py: This script takes the results of both theoretical and practical analysis in order to compute the GdC value. It does not generate output files, it prints to the console the sets A, B, Ao, and Bo and also the GdC value.

#  IMPORTANT: It needs, in the same directory of this script, the file "theoretical_analysis.json" (manually created from the evaluation of the "policy-detector" and "consent-detector" scripts output), the subdirectory "cookies-detector-results" with the results of the "cookies-detector" script, and the subdirectory "beacons-detector-results" with the results of the "web-beacons-detector" script.

import json

try:
    # First open all necessary files.
    with open('./theoretical_analysis.json') as f:
        theoretical_analysis = json.load(f)
    with open('./cookies-detector-results/cookie-results.json') as f:
        cookie_results = json.load(f)
    with open('./beacons-detector-results/beacons-results.json') as f:
        beacons_results = json.load(f)

    # Next generate the A and B sets from the 'theoretical_analysis'.
    A = set()
    B = set()
    for website, analysis in theoretical_analysis.items():
        # Some analyzed websites in the theoretical analysis may not be in the practical analysis (WEC cannot be executed).
        if website in cookie_results.keys() and website in beacons_results.keys():
            if analysis['consent_type'] == "none":
                A.add(website)
            elif analysis['consent_type'] not in ['no_option','confirm']:
                if not analysis['has_cookies_wall'] and not analysis['default_active']:
                    B.add(website)

    # Now generate the Ao and Bo sets from the 'cookie_results' and 'beacons_results'.
    Ao = set()
    for website in A:
        beacons = beacons_results[website]
        tracking_cookies = any(cookie['tracking'] for cookie in cookie_results[website])
        if not tracking_cookies and len(beacons) == 0:
            Ao.add(website)
    Bo = set()
    for website in B:
        beacons = beacons_results[website]
        tracking_cookies = any(cookie['tracking'] for cookie in cookie_results[website])
        if not tracking_cookies and len(beacons) == 0:
            Bo.add(website)

    # Finally compute the GdC value.
    gdc = (len(Ao.union(Bo))/len(A.union(B)))
        
    # Print the results.
    print('*************************')
    print('A :=',A)
    print('*************************')
    print('B :=',B)
    print('*************************')
    print('Ao :=',Ao)
    print('*************************')
    print('Bo :=',Bo)
    print('*************************\n')

    print('*************************')
    print('|A| :=',len(A))
    print('|B| :=',len(B))
    print('|Ao| :=',len(Ao))
    print('|Bo| :=',len(Bo))
    print('*************************')
    print('GdC :=',gdc)
    print('*************************\n')

except Exception as e:
    print(e)
    print('[ERROR] - Some input files are missing. Please read the documentation.')