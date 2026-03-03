import requests
import sys
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print("Please give one URL to run this program.")
    sys.exit(0)

site_re = sys.argv[1]  

if not site_re.startswith("http"):
    site_re = "https://" + site_re

# some times our request is blocked by server, to avoid that we pretend like firefox,chrome etc
fake_name = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(site_re, headers=fake_name)
parts_of_website = BeautifulSoup(response.text, "html.parser")

# tittle in the website 
print("Title:")
heading = parts_of_website.find("title")
if heading is not None and heading.string:
    print(heading.string.strip())
else:
    print("website donot have the tittle ")

# body text in the website 
print("\nBody Text:")
body = parts_of_website.find("body")
if body is not None:
    text = body.get_text().strip()
    
    if "JavaScript" in text:
        print("website is not static so need to use api")
    
    lines = text.split("\n")
    req_cleaned = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line != "":
            req_cleaned.append(line)
        i += 1
    print(" ".join(req_cleaned))
else:
    print("it donot contain any body text ")

# Outlinks present in the website. 
print("\n Outlinks:")
all_links = parts_of_website.find_all("a")
count = 0
j = 0
while j < len(all_links):
    link = all_links[j].get("href")
    if link is not None and link.startswith("http"):
        count += 1
        print(link)
    j += 1

if count == 0:
    print("there is no links found in the website ")