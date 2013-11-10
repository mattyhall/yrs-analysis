from pymongo import MongoClient

client = MongoClient()
db = client.repo_database
repos = db.repos
languages = []
for repo in repos.find():
    if repo['language'] is not None:
        print(repo['html_url'], repo['languages'])