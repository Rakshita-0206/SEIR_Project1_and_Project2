## This is about how my code works and what it will do

# How to Run
python fetch_page.py url1 url2  

# What My Program Does
- Takes two url from command line
- Fetches both webpages
- Prints Title, Body and Links for both pages
- Counts word frequency in body text
- Makes 64 bit hash for each word using p=53
- Makes SimHash for both documents
- Prints how many bits are same in both SimHash

# My Functions
- url_storing() - get two url from user
- request_html() - fetch webpage
- extract_title() - find title from h1 or title tag
- extract_body() - get only text remove all tags
- extract_link1() - find all links from anchor tag
- count_word() - count frequency of each word
- cal_hash() - make 64 bit hash using polynomial formula
- hash_for_doc() - make SimHash for whole document
- compare_simhash() - compare two SimHash and count common bits
- main_fun() - run everything

