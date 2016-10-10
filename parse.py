#!/usr/bin/python3

import ijson
import json
import sys
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


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def parse_amendments(file_path):
    uid, deposit_date, summary = "default_uid", "default_deposit_date", "default_summary"
    with open(file_path) as data_file:
        parser = ijson.parse(data_file)
        for prefix, event, value in parser:
            if prefix == 'textesEtAmendements.texteleg.item.amendements.amendement.uid':
                uid = value
            elif prefix == 'textesEtAmendements.texteleg.item.amendements.amendement.corps.exposeSommaire':
                summary = strip_tags(value).strip()
            elif prefix == 'textesEtAmendements.texteleg.item.amendements.amendement.item.dateDepot':
                deposit_date = value
            elif (prefix, event) == ('textesEtAmendements.texteleg.item.amendements.amendement', 'end_map'):
                print("%s;%s;%s" % (uid, deposit_date, summary))


def print_json(data):
    print(json.dumps(data))


def print_help():
    print("Usage:")
    print(__file__ + " members path/to/file")
    print(__file__ + " amendments path/to/file")


run(sys.argv)
