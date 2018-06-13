"""
Shows basic usage of the Drive v3 API.

Creates a Drive v3 API service and prints the names and ids of the last 10 files
the user has access to.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import database

# Setup the Drive v3 API
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v3', http=creds.authorize(Http()))

# Call the Drive v3 API
results = service.files().list(
    pageSize=100, fields="nextPageToken, files(id, name, parents)").execute()
all_items = results.get('files', [])

def searchFile(query, index = 0):
    _query = "name = '{}'".format(query)

    results = service.files().list(
    pageSize=10, fields="nextPageToken, files(id, name, parents)", q=_query).execute()
    items = results.get('files', [])
    if not items:
        print("No files found with the name {}.".format(query))
    else:
        return items[index]

try:
    d_fold = searchFile('d')['id']
    nod_fold = searchFile('no d')['id']
except Exception as e:
    print("Failed to load folders. Check internet connection <{}>".format(e))
    exit()

def load_images():
    d_cat = []
    nod_cat = []

    for item in all_items:

        try: parents = item['parents'];
        except: continue;

        if d_fold in parents:
            file = service.files().get(fileId=item['id']).execute()
            d_cat.append(file)
        if nod_fold in parents:
            file = service.files().get(fileId=item['id']).execute()
            nod_cat.append(file)

    return [d_cat, nod_cat]

def get_url(ID):
    base = "https://drive.google.com/uc?id="
    return base + ID

load_images()
