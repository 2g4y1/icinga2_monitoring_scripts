#!/usr/bin/env python
# Testet with Panasonic PT-VZ570 and DZ870E  
# Check webinterface for warnings.
# Usage: check_panasonic_projector.py IP Username


import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("hostname", help="Hostname or IP Address")
parser.add_argument("username", help="Username")

args = parser.parse_args()
get_string = 'http://' + args.hostname + '/cgi-bin/selfcheck.cgi'
r = requests.get(get_string, auth=(args.username, '') )

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.HTML_data = []

    def handle_data(self, data):
        self.HTML_data.append(data)

parser = MyHTMLParser()
parser.feed(r.text)

beamer_status = parser.HTML_data[3:-1]

if 'OK' in beamer_status[1]: #Fan
    if 'OK' in beamer_status[7]: #Lamp remain time
        if 'OK' in beamer_status[9]: #Lamp Status
            if 'OK' in beamer_status[13]: #Air Filter
                print('OK - ' + args.hostname + ' is fine.')
                exit(0)
            elif 'FAILED' in beamer_status[13]:
                print('CRITICAL - ' + args.hostname + ' Air filter failure')
                exit(1)
        elif 'FAILED' in beamer_status[9]:
            print('CRITICAL - ' + args.hostname + ' Lamp status failure')
            exit(1)
    elif 'FAILED' in beamer_status[7]:
        print('CRITICAL - ' + args.hostname  +' Lamp time error')
        exit(1)
elif 'FAILED' in beamer_status[1]:
    print('CRITICAL - ' + args.hostname + ' Fan failure')
    exit(1)
