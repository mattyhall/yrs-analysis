from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import getpass

CACHED = True

def get_github_projects(db):
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
        name = project_page.select('div.heading > h1')[0].text
        github = project_page.select("div.inner > ul > li.icon_github")
        if len(github) != 0 and 'github.com' in github[0].findChild('a').get('href'):
            href = github[0].findChild('a').get('href')
            finalist = False
            if len(project_page.select("div.award")) != 0:
                finalist = True
            github_hrefs.append({'finalist': finalist, 'href': href, 'name': name})
    print(github_hrefs)
    github_projects = db.github_projects
    github_projects.drop()
    github_projects.insert(github_hrefs)

def get_languages(url, auth):
    r = requests.get(url, auth=auth)
    return r.json()

def get_contibutors(url, auth):
    r = requests.get(url, auth=auth)
    return (len(r.json()))

def get_repo_information(db):
    password = getpass.getpass()
    base_url = 'https://api.github.com/'
    github_projects = db.github_projects
    auth = ('mattyhall', password)
    projects = []
    projects_data_tbl = db.projects_data
    projects_data_tbl.drop()
    for project in github_projects.find():
        href = project['href']
        finalist = project['finalist']
        project_data = {'github_url': href, 'finalist': finalist}
        raw_url = href.split('/')
        repo_url = '/'.join([x for x in raw_url if x != ''][-2:])
        r = requests.get(base_url + 'repos/' + repo_url, auth=auth)
        json = r.json()
        if json.get('message', '') != 'Not Found':
            project_data.update(json)
            languages = get_languages(project_data['languages_url'], auth)
            contributors = get_contibutors(project_data['contributors_url'], auth)
            project_data['languages'] = languages
            project_data['contributors'] = contributors
            projects.append(project_data)
    projects_data_tbl.insert(projects)


client = MongoClient()
db = client.repo_database
if not CACHED:
    get_github_projects(db)
get_repo_information(db)