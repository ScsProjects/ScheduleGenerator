# 
# Concordia Schedule Scraper
# Author: Jeremy Brown, Lance Lafontaine.
# 
# Basis for the scraper.
# Grabs the HTML for the course page of all 5 departments.
# Outputs to separate files
# Isolates all course information found within all <b></b> tags of each document.
# 
# Class Schedule Site POST Parameters
# Year: '2013', '2014'
# Session: 1 (Summer), 2 (Fall), 3 (Fall & Winter), 4 (Winter), 'A' (All sessions)
# Level: 'U' (Undergraduate), 'G' (Graduate), 'A' (All Levels)
# Departments: '01' (Arts & Science), '03' (JMSB), '04' (ENCS), '06' (Fine Arts), '09' (School of Extended Learning)
# 

from bs4 import BeautifulSoup
from urllib.request import urlopen # python2: from urllib2 import urlopen
from urllib.parse import urlencode

BASE_URL = "http://fcms.concordia.ca/fcms/asc002_stud_all.aspx"

def gen_values(dept, year='2014', session='A', level='A'):
    values = {'__EVENTTARGET': 'ctl00$PageBody$btn_ShowScCrs',
              '__VIEWSTATE': '/wEPDwULLTE5NzE0Mjg1OTMPZBYCZg9kFgQCAw9kFgJmD2QWAgIBD2QWAgICDw8WAh4EVGV4dAUJMjAxNC0yMDE1ZGQCBQ9kFgICAQ9kFgQCAQ9kFgJmD2QWAmYPZBYCZg9kFgICAQ9kFgYCAQ9kFgICAg9kFgJmDxAPFgYeDURhdGFUZXh0RmllbGQFBWRlc2NyHg5EYXRhVmFsdWVGaWVsZAUJQ09ERVZBTFVFHgtfIURhdGFCb3VuZGdkEBUCBzIwMTQtMTUHMjAxMy0xNBUCBDIwMTQEMjAxMxQrAwJnZxYBZmQCAw9kFgICAg9kFgJmDxAPFgofAQUIRkFDX0RFUFQfAgUJQ09ERVZBTFVFHwNnHglCYWNrQ29sb3IKpAEeBF8hU0ICCGQQFTwOQVJUUyAmIFNDSUVOQ0UYLSBBcHBsaWVkIEh1bWFuIFNjaWVuY2VzCS0gQmlvbG9neRwtIENoZW1pc3RyeSBhbmQgQmlvY2hlbWlzdHJ5LC0gQ2xhc3NpY3MsIE1vZGVybiBMYW5ndWFnZXMgYW5kIExpbmd1aXN0aWNzFy0gQ29tbXVuaWNhdGlvbiBTdHVkaWVzIS0gRGVhbiBvZiBBcnRzICYgU2NpZW5jZSAoT2ZmaWNlKQstIEVjb25vbWljcwstIEVkdWNhdGlvbgktIEVuZ2xpc2gTLSBFdHVkZXMgRnJhbmNhaXNlcxItIEV4ZXJjaXNlIFNjaWVuY2UlLSBHZW9ncmFwaHksIFBsYW5uaW5nIGFuZCBFbnZpcm9ubWVudAktIEhpc3RvcnkbLSBJbnRlcmRpc2NpcGxpbmFyeSBTdHVkaWVzDC0gSm91cm5hbGlzbRYtIExpYmVyYWwgQXJ0cyBDb2xsZWdlHi0gTG95b2xhIEludGVybmF0aW9uYWwgQ29sbGVnZRwtIE1hdGhlbWF0aWNzIGFuZCBTdGF0aXN0aWNzDC0gUGhpbG9zb3BoeQktIFBoeXNpY3MTLSBQb2xpdGljYWwgU2NpZW5jZQwtIFBzeWNob2xvZ3kKLSBSZWxpZ2lvbiItIFNjaG9vbCBvZiBDYW5hZGlhbiBJcmlzaCBTdHVkaWVzKC0gU2Nob29sIG9mIENvbW11bml0eSBhbmQgUHVibGljIEFmZmFpcnMRLSBTY2llbmNlIENvbGxlZ2UvLSBTaW1vbmUgZGUgQmVhdXZvaXIgSW5zdGl0dXRlICYgV29tZW5zIFN0dWRpZXMcLSBTb2Npb2xvZ3kgYW5kIEFudGhyb3BvbG9neRUtIFRoZW9sb2dpY2FsIFN0dWRpZXMeSk9ITiBNT0xTT04gU0NIT09MIE9GIEJVU0lORVNTDS0gQWNjb3VudGFuY3kPLSBFeGVjdXRpdmUgTUJBCS0gRmluYW5jZRgtIEdlbmVyYWwgQWRtaW5pc3RyYXRpb24sLSBHb29kbWFuIEluc3RpdHV0ZSBpbiBJbnZlc3RtZW50IE1hbmFnZW1lbnQMLSBNYW5hZ2VtZW50Cy0gTWFya2V0aW5nMS0gU3VwcGx5IENoYWluIGFuZCBCdXNpbmVzcyBUZWNobm9sb2d5IE1hbmFnZW1lbnQeRU5HSU5FRVJJTkcgJiBDT01QVVRFUiBTQ0lFTkNFMC0gQnVpbGRpbmcsIENpdmlsLCBhbmQgRW52aXJvbm1lbnRhbCBFbmdpbmVlcmluZyMtIENlbnRyZSBmb3IgRW5naW5lZXJpbmcgaW4gU29jaWV0eSstIENvbXB1dGVyIFNjaWVuY2UgYW5kIFNvZnR3YXJlIEVuZ2luZWVyaW5nOS0gQ29uY29yZGlhIEluc3RpdHV0ZSBmb3IgSW5mb3JtYXRpb24gU3lzdGVtcyBFbmdpbmVlcmluZxUtIERlYW4gb2YgRW5naW5lZXJpbmclLSBFbGVjdHJpY2FsIGFuZCBDb21wdXRlciBFbmdpbmVlcmluZyctIE1lY2hhbmljYWwgYW5kIEluZHVzdHJpYWwgRW5naW5lZXJpbmcJRklORSBBUlRTDy0gQXJ0IEVkdWNhdGlvbg0tIEFydCBIaXN0b3J5CC0gQ2luZW1hFC0gQ29udGVtcG9yYXJ5IERhbmNlGS0gQ3JlYXRpdmUgQXJ0cyBUaGVyYXBpZXMdLSBEZXNpZ24gYW5kIENvbXB1dGF0aW9uIEFydHMLLSBGaW5lIEFydHMHLSBNdXNpYw0tIFN0dWRpbyBBcnRzCS0gVGhlYXRyZRtTQ0hPT0wgT0YgRVhURU5ERUQgTEVBUk5JTkcdLSBTY2hvb2wgb2YgRXh0ZW5kZWQgTGVhcm5pbmcVPAIwMQQwMTQwBDAxNTEEMDE1MwQwMTA5BDAxMDMEMDEwMQQwMTMzBDAxMzQEMDEwNAQwMTA1BDAxNTIEMDEzNQQwMTA2BDAxODEEMDEwNwQwMTgyBDAxNjIEMDE1NgQwMTEwBDAxNTcEMDEzNgQwMTM3BDAxMzgEMDE4MAQwMTg1BDAxODQEMDE4NgQwMTM5BDAxMTICMDMEMDMwMgQwMzA5BDAzMDQEMDMwMAQwMzEwBDAzMDMEMDMwNQQwMzA2AjA0BDA0MDcEMDQwOAQwNDA1BDA0MDkEMDQwMAQwNDAzBDA0MDQCMDYEMDYxNwQwNjAzBDA2MDQEMDYxMAQwNjE4BDA2MTEEMDYwMAQwNjA1BDA2MDkEMDYwOAIwOQQwOTAwFCsDPGdnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2RkAgkPZBYCAgEPZBYCZg9kFgICAg9kFgRmD2QWAmYPEA8WBh8BBQlDTEFTU0RBWVMfAgUJQ0xBU1NEQVlTHwNnZBAVLAEgBy0tLS0tLS0HLS0tLS0tRActLS0tLVMtBy0tLS0tU0QHLS0tLUYtLQctLS0tRlMtBy0tLS1GU0QHLS0tSi0tLQctLS1KRi0tBy0tLUpGU0QHLS1XLS0tLQctLVctRi0tBy0tV0otLS0HLS1XSkYtLQctLVdKRlMtBy1ULS0tLS0HLVQtLUYtLQctVC1KLS0tBy1ULUpGLS0HLVRXLS0tLQctVFctRi0tBy1UV0otLS0HLVRXSkYtLQdNLS0tLS0tB00tLS1GLS0HTS0tSi0tLQdNLS1KRi0tB00tLUpGU0QHTS1XLS0tLQdNLVctRi0tB00tV0otLS0HTS1XSkYtLQdNLVdKRlNEB01ULS0tLS0HTVQtSi0tLQdNVC1KRi0tB01UVy0tLS0HTVRXSi0tLQdNVFdKLS1EB01UV0pGLS0HTVRXSkYtRAdNVFdKRlMtB01UV0pGU0QVLAEgBy0tLS0tLS0HLS0tLS0tRActLS0tLVMtBy0tLS0tU0QHLS0tLUYtLQctLS0tRlMtBy0tLS1GU0QHLS0tSi0tLQctLS1KRi0tBy0tLUpGU0QHLS1XLS0tLQctLVctRi0tBy0tV0otLS0HLS1XSkYtLQctLVdKRlMtBy1ULS0tLS0HLVQtLUYtLQctVC1KLS0tBy1ULUpGLS0HLVRXLS0tLQctVFctRi0tBy1UV0otLS0HLVRXSkYtLQdNLS0tLS0tB00tLS1GLS0HTS0tSi0tLQdNLS1KRi0tB00tLUpGU0QHTS1XLS0tLQdNLVctRi0tB00tV0otLS0HTS1XSkYtLQdNLVdKRlNEB01ULS0tLS0HTVQtSi0tLQdNVC1KRi0tB01UVy0tLS0HTVRXSi0tLQdNVFdKLS1EB01UV0pGLS0HTVRXSkYtRAdNVFdKRlMtB01UV0pGU0QUKwMsZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2cWAWZkAgEPZBYCZg8QZGQWAWZkAgMPDxYCHgdWaXNpYmxlaGRkZJTK9VTOWW8tCPl00UdYB+JgPGvE',
              '__EVENTVALIDATION': '/wEWigECi5Sl6QYCl7jOgwoC1K/Vsw0C1K/hiAoCuLveuQMCubveuQMCu7veuQMCurveuQMC6LveuQMChvmOqwgCtPmOqwgCsvmOqwgC14/UggkC0bPysw0C9tz4+Q8C9tyQjw0C7c7n6ggC7c6/GQLtzofDAgK8idTaAQK8ieC1DgLtzsv1CALtztfQAQL23ITUBAK8iYyQBwLtzuOLDgKVhPTtAwLtzo/mBgKVhIDICAKLxea/DgL23NShCwKC99XzDwL23OAcAryJmMsPAryJpKYEAryJ8M8BApWE6LILApWExPoGApWEuJ4OApWE0NUPAryJnKoOAoL3jYkNAteP7IIJAu3Oq74LAu3O/+oIAu3Ow/UIAu3O8+gFAoL37fMPAu3OtxkC7c7v0AEC7c77iw4C14/oggkC7c6D5gYC7c7vDwLtzuvQAQLtzvvqCALtzo/oBQLtzrMZAu3O3/UIAteP4IIJAoL39fEIAu3OyxoC7c7X9QgCgvfh8w8CgvfBmgoCgveNrgQC7c6H6AUC7c7j0AEC7c7z6ggC7c7nDwLXj7SBCQLtztvoBQKbtugpApu2+MgOAvXPtacDAtuBhIkCAtvurucOArXj1tEPAtqLiocLArXj7t4PAtqLooQLAtzj1tEPAtzj7t4PAsGIooQLArXjiqEOAtzjiqEOAsGI5tUFAt+fnaoNAsacnaoNAt+f0fsPAsac0fsPAsac6fgPArXjus0MAtzjus0MArXj/poPAtzj/poPAt+fgYYCAsacgYYCAt+fxdcMAsacxdcMAtX61tEPArz61tEPAtX6iqEOArz6iqEOAqGj5tUFAv+3naoNAqa3naoNAv+30fsPAqa30fsPAouRsNEMAtX6us0MAtX6/poPArz6/poPAv+3gYYCAv+3xdcMAqyOjMwNAqa3xdcMAouRjMwNAqa3jdcMAouR1M0NAufcmKoFAuezssQJAoSzssQJAouzssQJAo6zssQJAoGzssQJAr2zssQJAoqzssQJAruzssQJAonkuM8PAprElP0FArX3q6sKAr+cuY0NAsHjxcUKAqXjxcUKAqzjxcUKAtLvmtQCAtzW0NEHiGwkOD99KdufYM7srdXkhETn2mA=',
              'ctl00$PageBody$ddlYear': year,
              'ctl00$PageBody$ddlSess': session,
              'ctl00$PageBody$ddlLevl': level,
              'ctl00$PageBody$ddlDept': dept,
             }
    binary_values = urlencode(values).encode('ascii')
    return binary_values

def write_list_file(name, list):
    output_file = open(name, 'w')
    for item in list:
      output_file.write("%s\n" % item) # Add's a new line character at the end of each list item.
    output_file.close()

departments = {'as': '01',
                'jmsb': '03',
                'encs': '04',
                'fa': '06',
                'el': '09'}

for key, value in departments.items(): # python2: departments.iteritems()
    html = urlopen(BASE_URL, gen_values(value)).read()
    soup = BeautifulSoup(html, "lxml",)

    soup.prettify()

    # Outputs formatted site html to files
    write_list_file("%s.html" % key, soup.find_all("b")) #find_all() method returns a list. 


