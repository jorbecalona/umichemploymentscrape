# map_fun = '''function(doc) {
#     if (doc.type == 'Person')
#         emit(doc.name, null);
# }'''

# for row in db.query(map_fun):
#     print(row.key)

import json
from pprint import pprint

def getJobsFromJson(fileName='jobs.json', printme=False):
    json_data=open('jobs.json')
    data = json.load(json_data)
    if printme:
        pprint(data)
    json_data.close()
    return data