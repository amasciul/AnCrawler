import json

def parse():
    with open("/Users/Alexandre/deputes.json") as data_file:
        data = json.load(data_file)

        for d in data["export"]["acteurs"]["acteur"]:

            uid = d["uid"]["#text"]

            lastname = d["etatCivil"]["ident"]["nom"]
            firstname = d["etatCivil"]["ident"]["prenom"]
            title = d["etatCivil"]["ident"]["civ"]

            mandat = d["mandats"]["mandat"]
            if (len(mandat) > 0 and "election" in mandat[0].keys()):
                department = mandat[0]["election"]["lieu"]["departement"]

            print("%s %s %s %s %s" % (uid, title, firstname, lastname, department))

def print_json(data):
    print(json.dumps(data))

parse()
