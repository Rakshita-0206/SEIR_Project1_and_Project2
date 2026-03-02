import requests
import sys
from bs4 import BeautifulSoup

# get url from user
if len(sys.argv) < 2:
    print("you need to provide the url, otherwise this will not work")
    sys.exit()

url = sys.argv[1]
print("processing the provided url",url)
if not url.startswith("http"):
    url = "https://" + url

# get page
page_data = requests.get(url)
page_soup = BeautifulSoup(page_data.text, 'html.parser')

print("\n" + "TITLE fetching ")
title_tag = page_soup.find('title')
if title_tag and title_tag.string:
    print(title_tag.string.strip())
else:
    print("no tittle this website contain")

# 2. body
print("\n" + "BODY")
body_tag = page_soup.find('body')
if body_tag:
    body_text = body_tag.get_text()
    clean_lines = []
    for line in body_text.split('\n'):
        line = line.strip()
        if line:
            clean_lines.append(line)
    print(" ".join(clean_lines))
else:
    print("this website not contain any body")

#extracting the link 
print("\n" + "Links of the website")
link_num = 0
for i in page_soup.find_all('a'):
    link = i.get('href')
    if link and link.startswith('http'):
        link_num = link_num + 1
        print(str(link_num) + ". " + link)

if link_num == 0:
    print("no links found in this website")