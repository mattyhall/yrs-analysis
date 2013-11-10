from pymongo import MongoClient
import matplotlib.pyplot as plt
from collections import OrderedDict
from datetime import datetime

client = MongoClient()
db = client.repo_database
projects = db.projects_data

def bar_char(xvals, yvals, xlabel='', ylabel='', name='', save=False):
    fig = plt.figure(figsize=(20,10))
    ax = plt.subplot(111)
    ind = range(len(xvals))
    ax.bar(ind, yvals, align='center')
    ax.set_xticks(ind)
    ax.set_xticklabels(list(xvals))
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.autofmt_xdate()
    if save:
        plt.savefig('images/'+name, bbox_inches='tight')
    else:
        plt.show()

def language_usage_plot(projects, save=False):
    languages_usage = {}
    for project in projects.find():
        for language in project['languages']:
            if not language in languages_usage: languages_usage[language] = 0
            languages_usage[language] += 1
    languages_usage = OrderedDict(sorted(languages_usage.items(), key=lambda x: x[1], reverse=True))
    print(languages_usage)
    languages = languages_usage.keys()
    amounts = languages_usage.values()
    bar_char(languages, amounts, 'Languages', 'Number of projects', name='projects_per_language.png', save=save)

def language_bytes_plot(projects, save=False):
    language_bytes = {}
    for project in projects.find():
        print(project['name'], project['languages'], project['url'])
        for language, count in project['languages'].items():
            if not language in language_bytes: language_bytes[language] = 0
            language_bytes[language] += count
    language_bytes = OrderedDict(sorted(language_bytes.items(), key=lambda x: x[1], reverse=True))
    print(language_bytes)
    languages = language_bytes.keys()
    amounts = language_bytes.values()
    bar_char(languages, amounts, 'Languages', 'Number of bytes', name='bytes_per_language.png', save=save)

def last_updated_plot(projects, save=False):
    projs = []
    for project in projects.find():
        updated_at = datetime.strptime(project['updated_at'], '%Y-%m-%dT%H:%M:%Sz')
        projs.append({'name': project['name'], 'updated_at': updated_at})
    months = ['August', 'September', 'October', 'November']
    count = []
    for m in range(8, 12):
        count.append(len([p for p in projs if p['updated_at'] >= datetime(2013, m, 1)]))
    bar_char(months, count, "Month", "Number of projects updated", name='projects_updated_month.png', save=save)

def number_stars_plot(projects, save=False):
    proj_stars = {}
    for project in projects.find():
        if project['stargazers_count'] != 0:
            proj_stars[project['name']] = project['stargazers_count']
    proj_stars = OrderedDict(sorted(proj_stars.items(), key=lambda x: x[1], reverse=True))
    projs = proj_stars.keys()
    stars = proj_stars.values()
    bar_char(projs, stars, 'Project', 'Number of stars', name='project_stars.png', save=save)

def number_of_contributors_plot(projects, save=False):
    proj_contributors = {}
    for project in projects.find():
        if project['contributors'] > 1:
            proj_contributors[project['name']] = project['contributors']
    proj_contributors = OrderedDict(sorted(proj_contributors.items(), key=lambda x: x[1], reverse=True))
    projs = proj_contributors.keys()
    stars = proj_contributors.values()
    bar_char(projs, stars, 'Project', 'Number of contributors', name='project_contributors.png', save=save)

language_usage_plot(projects, True)
language_bytes_plot(projects, True)
last_updated_plot(projects, True)
number_stars_plot(projects, True)
number_of_contributors_plot(projects, True)