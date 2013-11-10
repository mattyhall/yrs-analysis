from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

base_url = 'http://hacks.youngrewiredstate.org/'
r = requests.get(base_url+'/events/YRS2013')
main_page = BeautifulSoup(r.text)
centre_hrefs = [element.get('href') for element in main_page.select("ul.centre_list > li > a")]
project_hrefs = []
for centre in centre_hrefs:
    r = requests.get(base_url + centre)
    centre_page = BeautifulSoup(r.text)
    project_hrefs += [element.get('href') for element in centre_page.select("div.right > h3 > a")]
github_hrefs = []
for project in project_hrefs:
    r = requests.get(base_url + project)
    project_page = BeautifulSoup(r.text)
    github = project_page.select("div.inner > ul > li.icon_github")
    if len(github) != 0:
        href = github[0].findChild('a').get('href')
        finalist = False
        if len(project_page.select("div.award")) != 0:
            finalist = True
        github_hrefs.append({'finalist': finalist, 'herf': href})
print(github_hrefs)
client = MongoClient()
db = client.repo_database
github_projects = db.github_projects
github_projects.drop()
github_projects.insert(github_hrefs)