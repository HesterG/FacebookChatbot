# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)
from where import getLocation
from opentime import getOpentime
from timetable import getCourseTimetable
from search_book import search_book
from library_data import *

import datetime
import requests
import json 

"""
helper function for search_book to match a course name
"""
def course_match(courses, name):
    for course in courses:
        if name in course["code"]:
            return True 
    return False 

# Libraries
LIST_OF_LIBRARIES = [
    "kf - Academic Success Centre, Koffler Centre",
    "koffler - Academic Success Centre, Koffler Centre",
    "astronomy - Astronomy \u0026amp; Astrophysics Library",
    "chem - Chemistry Library (A D Allen)",
    "allen - Chemistry Library (A D Allen)",
    "art - Department of Art Library",
    "engineering - Engineering \u0026amp; Computer Science Library",
    "aerospace - Engineering \u0026amp; Computer Science Library - Aerospace Resource Centre",
    "medicine - Family \u0026amp; Community Medicine Library",
    "newman - Industrial Relations and Human Resources Library (Newman)",
    "law - Law Library (Bora Laskin)",
    "map - Map and Data Library: Collection Access",
    "music - Music Library",
    "new - New College Library (Ivey)",
    "petro - Petro Jacyk Central \u0026amp; East European Resource Centre",
    "regis - Regis College Library",
    "hk - Richard Charles Lee Canada-Hong Kong Library",
    "smc - St. Michael's College - John M. Kelly Library",
    "kelly - St. Michael's College - John M. Kelly Library",
    "trinity -  Trinity College Library (John W Graham Library)",
    "emmanuel - Victoria University - Emmanuel College Library",
    "ba - Bahen Centre",
    "rom - Royal Ontario Museum Library \u0026amp; Archives",
    "oi - OISE Library",
    "gerstein - Gerstein Science Information Centre",
    "ej - E J Pratt Library",
    "rb - Robarts Library",
];

# All values in "DICT_OF_LIBRARIES" must also be in "LIST_OF_LIBRARIES" */
DICT_OF_LIBRARIES = {
    "kf": "Academic Success Centre, Koffler Centre",
    "koffler": "Academic Success Centre, Koffler Centre",
    "academic": "Academic Success Centre, Koffler Centre",
    "astronomy": "Astronomy \u0026amp; Astrophysics Library",
    "astrophysics": "Astronomy \u0026amp; Astrophysics Library",
    "chem": "Chemistry Library (A D Allen)",
    "chemistry": "Chemistry Library (A D Allen)",
    "allen": "Chemistry Library (A D Allen)",
    "art": "Department of Art Library",
    "engineering": "Engineering \u0026amp; Computer Science Library",
    "aerospace": "Engineering \u0026amp; Computer Science Library - Aerospace Resource Centre",
    "family": "Family \u0026amp; Community Medicine Library",
    "medicine": "Family \u0026amp; Community Medicine Library",
    "newman": "Industrial Relations and Human Resources Library (Newman)",
    "law": "Law Library (Bora Laskin)",
    "map": "Map and Data Library: Collection Access",
    "music": "Music Library",
    "new": "New College Library (Ivey)",
    "ivey": "New College Library (Ivey)",
    "petro": "Petro Jacyk Central \u0026amp; East European Resource Centre",
    "regis": "Regis College Library",
    "richard": "Richard Charles Lee Canada-Hong Kong Library",
    "hk": "Richard Charles Lee Canada-Hong Kong Library",
    "robarts": "Robarts Library",
    "rl": "Robarts Library",
    "rom": "Royal Ontario Museum Library \u0026amp; Archives",
    "rare": "Thomas Fisher Rare Book Library",
    "smc": "St. Michael's College - John M. Kelly Library",
    "trinity": "Trinity College Library (John W Graham Library)",
    "oi": "OISE Library",
    "kelly": "St. Michael's College - John M. Kelly Library",
    "rb": "Robarts Library",
    "gerstein": "Gerstein Science Information Centre",
    "ej": "Victoria University - E J Pratt Library",
    "emmanuel": "Victoria University - Emmanuel College Library"
};

def getSuggestedLibraries():
    return '<br/>'.join(LIST_OF_LIBRARIES)

@app.route('/')
def getHomePage():
    return "Welcome to the homepage!"

@app.route('/<query>')
def output(query):
    tokens = query.split(' ')
    first = tokens[0]
    # TODO SUPPORT MULTIPLE
    # rest = tokens[1:]

    if (len(tokens) == 1): # If there is only one token
        if (first.upper() == 'LIB' or first.upper() == 'LIBRARY'):
            return "Please enter the library you are looking for.(ie. lib rb)<br/>" + getSuggestedLibraries()
        elif first.upper() == 'TIMETABLE':
            return "What course do you want to find?<br/>"
        elif (first.upper() == 'WHERE' or first.upper() == "LOC" or first.upper() == "LOCATION" or first == "找"):
            return "Which building do you want to find?<br/>"
        elif (first.upper() == 'BOOK' or first.upper() == 'BOOKS'):
            return "Please enter the book you are looking for.<br/>"
        else:
            return 'Not implemented yet'

    if len(tokens) >= 2 and (first.upper() == 'WHERE' or first.upper() == "LOC" or first.upper() == "LOCATION" or first == "找"):
        return getLocation(tokens[1])

    if len(tokens) >= 2 and (first.upper() == 'TIMETABLE'):
        return getCourseTimetable(tokens[1:])

    if len(tokens) >= 2 and (first.upper() == 'LIB' or first.upper() == "LIBRARY"):
        return getOpentime(tokens[1])
    
    if len(tokens) >= 2 and (first.upper() == 'BOOK' or first.upper() == 'BOOKS'):
        return search_book(tokens[1:])
    
    else:
        return 'Not implemented yet'

@app.route('/books/<book>')
def search_book(book):
    url = "https://cobalt.qas.im/api/1.0/textbooks?key=LrCC7Jj8knSAMPWPsDhf8l9h90QCMOsx"
    response = requests.get(url).text
    books = json.loads(response)
    # print(b)
    # print(type(b))
    for item in books:
        # print(item["courses"])
        if item["title"] == book or course_match(item["courses"], book):
            text = ""
            for key in item:
                if key != "courses":
                    text += key+": "+str(item[key])+"<br/>" 
            return text
    return "cannot find book"


if __name__ == '__main__':
    app.debug = True
    app.run()


