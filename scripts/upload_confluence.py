import os
import requests

BASE = os.environ.get('CONFLUENCE_BASE')
USER = os.environ.get('CONFLUENCE_USER')
TOKEN = os.environ.get('CONFLUENCE_TOKEN')
SPACE = os.environ.get('CONFLUENCE_SPACE', 'DEV')
TITLE = os.environ.get('CONFLUENCE_PAGE_TITLE', 'Automated Test Report')
HTML_PATH = os.environ.get('HTML_REPORT', 'report\\report.html')

session = requests.Session()
session.auth = (USER, TOKEN)
headers = {'Content-Type': 'application/json'}

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

search_url = f"{BASE}/rest/api/content?title={TITLE}&spaceKey={SPACE}&expand=version"
r = session.get(search_url)
r.raise_for_status()
results = r.json().get('results', [])

if results:
    page = results[0]
    page_id = page['id']
    version = page['version']['number'] + 1
    update_url = f"{BASE}/rest/api/content/{page_id}"
    body = {
        'id': page_id,
        'type': 'page',
        'title': TITLE,
        'space': { 'key': SPACE },
        'body': { 'storage': { 'value': html, 'representation': 'storage' } },
        'version': { 'number': version }
    }
    session.put(update_url, json=body).raise_for_status()
    print('Updated Confluence page')
else:
    create_url = f"{BASE}/rest/api/content/"
    body = {
        'type': 'page', 'title': TITLE, 'space': {'key': SPACE},
        'body': { 'storage': { 'value': html, 'representation': 'storage' } }
    }
    session.post(create_url, json=body).raise_for_status()
    print('Created Confluence page')
