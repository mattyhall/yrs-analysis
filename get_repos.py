from pymongo import MongoClient
import requests
import getpass
import time

def get_languages(url, auth):
    while True:
        r = requests.get(url, auth=auth)
        json = r.json()
        if json.get('documentation_url', '') == 'http://developer.github.com/v3/#rate-limiting':
            print("Language rate limit reached, sleeping")
            time.sleep(30)
            continue
        return json

user = 'mattyhall'
password = getpass.getpass()
url = 'https://api.github.com/search/repositories?q=YRS&page={0}'

client = MongoClient()
db = client.repo_database
repos = db.repos
repos.drop()

i = 0
while True:
    r = requests.get(url.format(i), auth=(user, password))
    json = r.json()
    if json.get('items', None) is None:
        if json.get('documentation_url', '') == 'http://developer.github.com/v3/#rate-limiting':
            print('Rate limit exceeded, sleeping')
            time.sleep(30)
            continue
        break
    print('Got page', str(i))
    for repo in json['items']:
        languages = []
        if repo['language'] != None:
            languages = get_languages(repo['languages_url'], (user, password))
        repo['languages'] = languages
        repos.insert(repo)
    i += 1
print(repos.count())