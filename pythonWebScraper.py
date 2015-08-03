import requests
from bs4 import BeautifulSoup
import re
import csv

url = 'http://www.socialbakers.com/statistics/twitter/profiles/mexico/'
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html)
dropdowntable = soup.findAll("a", " ")

links = []
for li in dropdowntable:
    links.append(li['href'])

with open('twitterUsernames.csv', 'w') as csvfile:
    fieldnames = ['Category', 'Sub-Category', 'Sub Sub-Category', 'Twitter Username']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for eachlink in links:
        urlnew = "http://www.socialbakers.com" + eachlink
        response2ndlevel = requests.get(urlnew)
        html2ndlevel = response2ndlevel.content
        soup2ndlevel = BeautifulSoup(html2ndlevel)

        twitternames = soup2ndlevel.findAll('h2')
        rangefornames = range(4,len(twitternames))

        for num in rangefornames:
            name = re.search(r"\(([^)]+)\)", str(twitternames[num]))
            if name:
                name = name.group(1)
                nametoadd = name.translate(None,"@")
                categories = re.sub('/statistics/twitter/profiles/mexico/', " ", eachlink).rstrip('/').split("/")
                if len(categories) == 3:
                    writer.writerow({'Category' : categories[0], 'Sub-Category' : categories[1], "Sub Sub-Category" : categories[2], 'Twitter Username' : nametoadd })
                else:
                    writer.writerow({'Category' : categories[0], 'Sub-Category' : categories[1], "Sub Sub-Category" : "No Sub Sub-Category", 'Twitter Username' : nametoadd })

print "All Finished"
