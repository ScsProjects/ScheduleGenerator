"""Concordia Schedule Scraper"""
"""Data parser"""

__author__ = "Jeremy Brown"
__copyright__ = "2014 ScsProjects"
__license__ = "MIT"

def parse_course(c):
    """
    Extracts all that data related to a given course with the course's first row in the html as a reference
    Returns a dictionary containing the structured data
    """
    course_model = {}
    # Data in first row
    course_model['code'] = str(c.contents[2].contents[0].contents[0].string).strip()
    course_model['name'] = str(c.contents[3].contents[0].contents[0].string).strip()
    course_model['credits'] = str(c.contents[4].contents[0].contents[0].string).strip()

    row = c.next_sibling
    
    course_model['times'] = []
    
    # Data in following rows of the same course
    while (type(row) == Tag and row.has_attr('bgcolor') and row['bgcolor'] != "LightBlue" and not (row['bgcolor'] == "White" and not row.has_attr('align'))):
        row_data = row.contents

        # Prerequisite row, if present
        if str(row_data[2].contents[0].string).find("Prerequisite:") != -1:
            course_model['prereq'] = str(row_data[3].contents[0].string).strip()

        # Special note row, if present
        elif str(row_data[2].contents[0].string).find("Special Note:") != -1:
            course_model['special_note'] = str(row_data[3].contents[0].string).strip()

        # Row containing a session, name, time, location, prof
        elif len(row_data) > 5 and row_data[2].contents[0].contents and len(row_data) > 5 and (str(row_data[2].contents[0].contents[0].string) == "/1" or str(row_data[2].contents[0].contents[0].string) == "/2" or str(row_data[2].contents[0].contents[0].string) == "/3" or str(row_data[2].contents[0].contents[0].string) == "/4"):
            time = parse_time(row_data)
            course_model['times'].append(time)

        row = row.next_sibling
    return course_model


def parse_time(row_data):
    """
    Structures the data related to the course time from the passed row_data
    """
    time = {}
    # Course session
    time['session'] = str(row_data[2].contents[0].contents[0].string).strip()

    # Course time name
    time['name'] = ""
    for d in row_data[3].contents[0].find_all('b'):
        time['name'] += str(d.string + " ").strip()
    if "*Cancelled*" in time['name']:
        time['cancelled'] = True

    # Course time
    if len(row_data[4].contents[0].find_all('b')[0].contents) > 1:
        time['time'] = str(row_data[4].contents[0].contents[0].contents[0].string + " ").strip()
        time['time'] += str(row_data[4].contents[0].contents[0].contents[2].string).strip()
    else:
        time['time'] = str(row_data[4].contents[0].contents[0].string).strip()

    # Course location
    if len(row_data[5].contents[0].contents[0].contents) > 1:
        time['location'] = str(row_data[5].contents[0].contents[0].contents[0].string).strip()
        time['location'] += str(row_data[5].contents[0].contents[0].contents[2].string).strip()
    else:
        time['location'] = str(row_data[5].contents[0].contents[0].string).strip()

    # Course Prof
    if len(row_data) > 6:
        time['professors'] = []
        if (len(row_data[6].contents[0].contents[0].contents) > 1):
            for g in range(0, len(row_data[6].contents[0].contents[0].contents)):
                if (g % 2 == 0):
                    time['professors'].append(str(row_data[6].contents[0].contents[0].contents[g]).strip())
        else: 
            time['professors'].append(str(row_data[6].contents[0].contents[0].string).strip())
    return time