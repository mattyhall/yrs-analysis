from pymongo import MongoClient
import matplotlib.pyplot as plt
from collections import OrderedDict

client = MongoClient()
db = client.repo_database
projects = db.projects_data

languages_usage = {}
for project in projects.find():
    for language in project['languages']:
        if not language in languages_usage: languages_usage[language] = 0
        languages_usage[language] += 1
languages_usage = OrderedDict(sorted(languages_usage.items(), key=lambda x: x[1], reverse=True))
print(languages_usage)

languages = languages_usage.keys()
amounts = languages_usage.values()
fig = plt.figure()
ax = plt.subplot(111)
ind = [x*50 for x in range(len(languages))]
ax.bar(ind, amounts, width=50, align='center')
ax.set_xticks(ind)
ax.set_xticklabels(list(languages))
fig.autofmt_xdate()
plt.show()