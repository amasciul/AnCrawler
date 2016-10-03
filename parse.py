import json
from pprint import pprint

with open("/Users/Alexandre/deputes.json") as data_file:
    data = json.load(data_file)

    for d in data["export"]["acteurs"]["acteur"]:

        print(d)

        lastname = d["etatCivil"]["ident"]["nom"]
        firstname = d["etatCivil"]["ident"]["prenom"]
        title = d["etatCivil"]["ident"]["civ"]

        print("%s %s %s" % (title, firstname, lastname))
