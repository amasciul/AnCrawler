#!/usr/bin/python3

import sys, json, ijson
from html.parser import HTMLParser

def run(args):
    if len(args) < 3:
        print_help()
        return

    if args[1] == "members":
        parse_members(args[2])
    elif args[1] == "amendments":
        parse_amendments(args[2])
    else:
        print_help()

def parse_members(file_path):
    print("file:" + file_path)
    with open(file_path) as data_file:
        data = json.load(data_file)

        for d in data["export"]["acteurs"]["acteur"]:

            uid = d["uid"]["#text"]

            lastname = d["etatCivil"]["ident"]["nom"]
            firstname = d["etatCivil"]["ident"]["prenom"]
            title = d["etatCivil"]["ident"]["civ"]

            mandat = d["mandats"]["mandat"]
            if (len(mandat) > 0 and "election" in mandat[0].keys()):
                department = mandat[0]["election"]["lieu"]["departement"]

            print("%s;%s;%s;%s;%s" % (uid, title, firstname, lastname, department))

def parse_amendments(file_path):
    print("file:" + file_path)
    count = 0
    with open(file_path) as data_file:
        parser = ijson.parse(data_file)
        for prefix, event, value in parser:
            if (prefix) == ('textesEtAmendements.texteleg.item.amendements.amendement.uid'):
                uid = value
                for sub_prefix, sub_event, sub_value in parser:
                    if (sub_prefix) == ('textesEtAmendements.texteleg.item.amendements.amendement.corps.exposeSommaire'):
                        break
                print("%s;%s" % (uid, strip_tags(sub_value)))
    print(count)


def print_json(data):
    print(json.dumps(data))

def print_help():
    print("Usage:")
    print(__file__ + " members path/to/file")
    print(__file__ + " amendments path/to/file")

run(sys.argv)
