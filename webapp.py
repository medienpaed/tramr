#!/usr/bin/python
# -*- coding: UTF-8 -*-

# importing the requests library
import requests
import xml.etree.ElementTree as ET
from auth import *
from datetime import datetime
from datetime import timedelta
from flask import Flask, render_template

app = Flask(__name__)
anzeige = "0.0"

# import json

# defining
API_ENDPOINT = "https://api.opentransportdata.swiss/trias"

DistanzLochergut = 200.0
DistanzSihlpost = 330.0

Sihlpost = '8591367'
Lochergut = '8591259'
Klusplatz = '8591233'
Albisrieden = '8591036'

headers = {'Content-Type': 'application/xml',
           'Authorization': auth
           }

# Functions

def makexml(id):
    # data to be sent to api
    xml = '<?xml version="1.0" encoding="UTF-8"?> \
      <Trias version="1.1" xmlns="http://www.vdv.de/trias" xmlns:siri="http://www.siri.org.uk/siri" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> \
      <ServiceRequest> \
      <RequestPayload> \
      <StopEventRequest> \
      <Location> \
      <LocationRef> \
        <StopPointRef>'+id+'</StopPointRef> \
      </LocationRef> \
      </Location> \
      <Params> \
      <NumberOfResults>12</NumberOfResults> \
      <StopEventType>departure</StopEventType> \
      <IncludePreviousCalls>false</IncludePreviousCalls> \
      <IncludeOnwardCalls>false</IncludeOnwardCalls> \
      <IncludeRealtimeData>true</IncludeRealtimeData> \
      </Params> \
      </StopEventRequest> \
      </RequestPayload> \
      </ServiceRequest> \
      </Trias> '
    return xml

def uhr(str):
    ergebnis = datetime.strptime(str, "%Y-%m-%dT%H:%M:%SZ")
    return ergebnis

def nexttram(zeit,ort,wohin):
    naechstes = 999.0
    # sending post request and saving response as response object
    r = requests.post(url = API_ENDPOINT, data = makexml(ort), headers = headers)
    # extracting response text und Umwandlung in Baum
    root = ET.fromstring(r.text)

    # alle durchgehen und Restzeit berechnen
    a = 0
    for StopEvent in root.iter('{http://www.vdv.de/trias}StopEvent'):
        ToGo = timedelta.total_seconds(uhr(StopEvent[0][0][2][0].text)-uhr(root[0][0].text))-zeit
#        if (StopEvent[1][9].text == wohin) and (ToGo>0):
#            print(StopEvent[1][10][0].text[9:],ToGo)
        if ((StopEvent[1][9].text == wohin) and (ToGo>0) and (a==0)) :
            naechstes = ToGo
            a=a+1
    return naechstes

@app.route('/lochergut')
def zeit_lochergut():
    anzeige = str(nexttram(DistanzLochergut,Lochergut,Klusplatz))
    return render_template('tramr.html', anzeige=anzeige, titel='Lochergut')

@app.route('/sihlpost')
def zeit_sihlpost():
    anzeige = str(nexttram(DistanzSihlpost,Sihlpost,Albisrieden))
    return render_template('tramr.html', anzeige=anzeige, Titel='Sihlpost')

@app.route('/')
def web_start():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
