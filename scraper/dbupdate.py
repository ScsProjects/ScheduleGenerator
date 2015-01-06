#!/usr/bin/env python3

"""Concordia Schedule Scraper"""
"""Main Script"""

__author__ = "Jeremy Brown"
__copyright__ = "2014 ScsProjects"
__license__ = "MIT"

# TO DO
# - Make date and times system-readable
# - Merge awkward format of times and locations
# - Link associated lectures and tutorials/labs/etc. (re?)

import sgscraper
import sgparser
#from pymongo import MongoClient

#client = MongoClient()
#db = client.schedule_generator
#courses = db.courses

# List of departments and their respective codes as identified by the webpage
departments = {'as': '01',
                'jmsb': '03',
                'encs': '04',
                'fa': '06',
                'el': '09'}

# Run through the course pages of all departments
for key, value in departments.items(): # python2: departments.iteritems()
    strainer = SoupStrainer(id="ctl00_PageBody_tblBodyShow1")
    soup_table = create_soup(value, strainer)
    # Select courses table
    courses_table = soup_table.find_all("tr", bgcolor="LightBlue")
    
    # Iterates through all the first rows of a course (LightBlue rows)
    #course_list = []
    for c in courses_table:
        course_model = parse_course(c)
        write_obj_file(course_model)
        #course_list.append(course_model)
        
    #courses.insert(course_list)