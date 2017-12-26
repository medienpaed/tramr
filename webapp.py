#!/usr/bin/python
# -*- coding: UTF-8 -*-

# importing the requests library
import requests
import xml.etree.ElementTree as ET
import sqlite3
from auth import *
from datetime import datetime
from datetime import timedelta
from flask import Flask, render_template, g, request, jsonify

app = Flask(__name__)

DATABASE = 'database.db'

# defining

anzeige = "0.0"

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

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

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
    naechstes = 9999.0
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

def id2halt(haltnummer):
    haltname = query_db('select * from Bahnhof where StationID = ?', [haltnummer], one=True)
    return haltname[1]

def haltsearch(query):
    halt = query_db('select * from Bahnhof where Station LIKE ?', [query], one=False)
    return halt

@app.route('/abfrage', methods=['POST'])
def abfrage():
    result = haltsearch(request.form['haltstring'])
    return jsonify({'text':'haltstring'})

@app.route('/<halt_id>/<ziel_id>/<int:zeit>')
def zeit_ausgabe(halt_id, ziel_id, zeit):
    anzeige = str(nexttram(zeit,halt_id,ziel_id))
    titelstring = id2halt(halt_id).split('$')[0]
    return render_template('tramr.html', anzeige=anzeige, titel=titelstring)

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
    return render_template('index.html',ausgabe_start='')

if __name__ == '__main__':
    app.run()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
