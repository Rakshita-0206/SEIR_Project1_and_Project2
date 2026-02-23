import sys
import urllib.request
import gzip

# this function get 2 url from command line
def url_storing ():
    args = sys.argv  
    if len(args)<3:
        print("Please provide two URL")
        sys.exit()
    url1=args[1]
    url2=args[2]
    print("Url1 given", url1)
    print("URL2 given", url2)
    return url1, url2

# this fetch the html from url
def request_html(url):
    request = urllib.request.Request(url)
    request.add_header("User-Agent", "Mozilla/5.0")  #this is done because , website should not block us for the request we sent.

    response = urllib.request.urlopen(request)

    html = response.read()
    try:
        html = html.decode("utf-8")
    except:
        html = html.decode("latin-1")

    return html

# this find the tittle from html (h1 or title tag)
def extract_tittle(html):
    tittle=""
    for i in range(len(html)):
        # check for h1 tag
        if html[i:i+2] == "<h" and html[i+2]=="1":
            k = i
            # find end of opening tag
            while k < len(html) and html[k] != ">":
                k += 1
            j = k + 1 # start of content, from here we start collecting the text of the tittle 
            
            tittle = ""  
            while j < len(html):
                if html[j:j+5] == "</h1>" or html[j:j+5]=="</H1>":
                    if tittle:
                        return tittle
                tittle = tittle + html[j]
                j += 1

        #sometimes some website may use tittle also so ya , for that we need to use this 
        if html[i:i+7] == "<title>" or html[i:i+7] == "<TITLE>":
            j = i + 7
            tittle = ""
            while j < len(html):
                if html[j:j+8] == "</title>" or html[j:j+8] == "</TITLE>":
                    return tittle
                tittle = tittle + html[j]
                j += 1
    
    return "contain no tittle"  #if we got nothing, then we need to return the no tittle found.

# this extract only text from body (removing all the html tags)
def extract_body(html):    
    body_content=""
    for i in range(len(html)):  
        # find body tag start
        if html[i:i+5]=="<BODY" or html[i:i+5]=="<body":   
        
            k=i
            # finding the end of body opening tag
            while k<len(html) and html[k]!=">":
                k=k+1
            k=k+1  
    
            # get everything until closing body
            while k<len(html):
                if html[k:k+7]=="</body>" or html[k:k+7]=="</BODY>":
                    break
                body_content=body_content+html[k]
                k=k+1
            
            # remove all tags from body content, to get the clean text
            required_content=""
            inside_tag=False
            for j in range(len(body_content)):
                if body_content[j]=="<":
                    inside_tag=True
                elif body_content[j]==">":
                    inside_tag=False
                elif not inside_tag:
                    required_content=required_content+body_content[j]
            
            return required_content
    
    return "contain no body"

# this extract all links from anchor tags
def extract_link1(html):
    link_list=[]
    
    for i in range(len(html)):
        # finding the anchor tag
        if html[i:i+2]=="<a" or html[i:i+2]=="<A":
            # look for href after it 
            for j in range(i+2, len(html)):
                if html[j:j+4]=="href" or html[j:j+4]=="HREF":
                    k=j+4
                    # find = sign after that only link start
                    while k<len(html) and html[k]!="=":
                        k=k+1
                    k=k+1
                    # skip spaces, if present in the starting of the link
                    while k<len(html) and html[k]==" ":
                        k=k+1
                    # here we are checking for the quotes, because link is written in between the quotes
                    if k<len(html) and (html[k]=='"' or html[k]=="'"):
                        starting_quote=html[k]
                        k=k+1
                        link=""
                        # get url until closing quote  
                        while k<len(html) and html[k]!=starting_quote:
                            link=link+html[k]
                            k=k+1
                        
                        if link!="":
                            link_list.append(link)
                        break
    return link_list

# this count how many times each word appear
def count_word(text):
    
    text = text.lower()  # make all small letter, not case sensitive so ya 
    words = text.split()  
    dict_word = {}
    for word in words:
        # remove punctuation from word
        clean_word = ""
        for char in word:
            if char.isalnum():  # keep only a-z and 0-9, cleaning remove unnecessary part
                clean_word = clean_word + char
        
        if clean_word != "":  # if word exist after cleaning , putting in the dictionary
            if clean_word in dict_word:
                dict_word[clean_word] = dict_word[clean_word] + 1
            else:
                dict_word[clean_word] = 1
    
    return dict_word     

# this make 64 bit hash using formula given in the assignment
def cal_hash(word):
    hash_sum = 0
    for i in range(len(word)):
        asci_val = ord(word[i])  # ascii value of char, it is find by "ord",need asci value calculating hash value 
        hash_fun = asci_val * (53 ** i)  
        hash_sum = hash_sum + hash_fun  
    
    hash_final = hash_sum % (2**64)  
    return hash_final
    
# this make simhash for whole document    
def hash_for_doc(word_dict):
    v = []  # array of 64 numbers
    for i in range(64):
        v.append(0)  #  fill with zeros in the array 
    

    for word in word_dict:
        frequency = word_dict[word]  
        hash_value = cal_hash(word) 
        # convert hash to 64 bit binary
        binary_str = bin(hash_value)[2:]
        while len(binary_str) < 64:
            binary_str = "0" + binary_str
        
        # update v array based on bits present in the binary_str
        for j in range(64):
            if binary_str[j] == '1':
                v[j] = v[j] + frequency  # add if bit is 1
            else:
                v[j] = v[j] - frequency  # subtract if bit is 0 
    
    # make final hash from v array
    final_hash = 0
    for j in range(64):
        if v[j] > 0:  # if positive then bit is 1
            # calculate 2^j, then add in the final hash 
            power = 1
            for k in range(j):
                power = power * 2
            final_hash = final_hash + power  # add to final, at last this only we return 
    
    return final_hash

# this compare two simhash and count common bits
def compare_simhash(word_dict1, word_dict2):
    # getting the simhash for both documents
    finger_print_1=hash_for_doc(word_dict1)
    finger_print_2=hash_for_doc(word_dict2)
    
    # convert both to 64 bit binary
    bin1_d1 = bin(finger_print_1)[2:]
    while len(bin1_d1) < 64:
        bin1_d1 = "0" + bin1_d1
    
    bin2_d2 = bin(finger_print_2)[2:]
    while len(bin2_d2) < 64:
        bin2_d2= "0" + bin2_d2
    
    # count how many bits are same , these only says how much similar are the documents 
    similar_bit = 0
    for i in range(64):
        if bin1_d1[i] == bin2_d2[i]:
            similar_bit = similar_bit + 1
    return similar_bit

# main function, combining everything we wrote above to get desired result 
def main_fun():
    
    url1, url2 = url_storing()
    
    
    html1 = request_html(url1)
    body1 = extract_body(html1)
    dict1 = count_word(body1)
    sim1 = hash_for_doc(dict1)  # not used but ok written extra 
    
    
    print("Title:", extract_tittle(html1))
    print("Body:", body1)
    print("Links:")
    links1 = extract_link1(html1)
    for link in links1:
        print(link)

 
    html2 = request_html(url2)
    body2 = extract_body(html2)
    dict2 = count_word(body2)
    sim2 = hash_for_doc(dict2)  # not used but ok written extra 
    

    print("Title:", extract_tittle(html2))
    print("Body:", body2)
    print("Links:")
    links2 = extract_link1(html2)
    for link in links2:
        print(link)
    

    common = compare_simhash(dict1, dict2)
    print(common)

# this part is for running  the program
if __name__ == "__main__":

    main_fun()

