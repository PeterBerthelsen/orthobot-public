import requests
import re
import os
import utils
from bs4 import BeautifulSoup

def get_readings_urls(domain:str, page:str):
    #Base URL is required for concatenating with server-side URLs
    #Readings URL is required for the actual parsing of the list
    print(
        "Initiating get_readings_urls with payload "
        + "domain:" + domain
        + " page:" + page
    )
    baseURL = domain
    readingsURL = domain + "/" + page
    #The following requests the Readings URL, parses down to the list of
    #   readings in the ul and populates the readingsURLs with the full link
    #   to be parsed in the future
    readingsURLs = []
    r = requests.get(readingsURL)
    soup = BeautifulSoup(r.text, features="html.parser")
    section = soup.find_all('section')
    list = section[0].find_all('ul')
    items = list[0].find_all('li')
    for li in items:
        #Once the list is identified, this loop identifies each 'a href' and
        #   adds them (internal links) to the base URL and records the full
        #   link in the readingsURLs list
        reading = li.find_all('a')
        for a in reading:
            readingsURLs.append(baseURL + a.get('href'))
    return readingsURLs

def get_readings_titles(list):
    passage_list = []
    #The list variable passed and contains passages from get_readings_text
    #   For each reading, the title and text is grabbed
    for addr in list:
        #Requests pulls the url, then BeautifulSoup looks for the article tag,
        #   drawing out the reading passage and liturgical title, formatting,
        #   and concatenating them
        r = requests.get(addr)
        soup = BeautifulSoup(r.text, features="html.parser")
        article = soup.find_all("article")
        title = article[0].find_all("h2")[0].text.strip().replace("  "," ")
        passage_list.append(title)
    return passage_list

def get_readings_text(list):
    #Passage list is populated via BeautifulSoup and formatted
    #   into a list for later use
    print(
        "Initiating get_readings_text with payload"
        + "list: " + str(list)
    )
    passage_list = []
    #The list variable passed and contains passages from get_readings_text
    #   For each reading, the title and text is grabbed
    for addr in list:
        #Requests pulls the url, then BeautifulSoup looks for the article tag,
        #   drawing out the reading passage and liturgical title, formatting,
        #   and concatenating them
        r = requests.get(addr)
        soup = BeautifulSoup(r.text, features="html.parser")
        article = soup.find_all("article")
        title = article[0].find_all("h2")[0].text.strip()
        #title contains scripture reference and liturgical text - the liturgical
        #   text is wrapped in (), so the string is split by it
        title_array = title.split(" (")
        passage = title_array[0].strip()
        #liturgical text is then stripped of the ")" and any open spaces are reduced
        #   this primarily happens with Vespers readings (1st, 2nd, 3rd...)
        liturgical_text = title_array[1].strip()[:-1].replace("  "," ",1)
        #Some readings (Vespers), have "reading" in the text. If so,
        #   the word is not added to the header
        if "reading" in liturgical_text:
            reading_header = "Today's " + liturgical_text + " is " + passage
        else:
            reading_header = "Today's " + liturgical_text + " reading is " + passage
        passage_dd = article[0].find_all("dd")
        passage_text = ""
        #BeautifulSoup then pulls the dd tags containing the text of the passage
        #   concatenating them together
        for dd in passage_dd:
            passage_text = passage_text + dd.text.strip() + " "
        #The title and passage text are put into a list, which populates the full
        #   list, which will be processed later
        passage_list.append([reading_header, passage_text])
        print("get_readings_text | added: " + str(liturgical_text))
    return passage_list

def get_saints_info(domain:str, page:str):
    #Base URL is required for concatenating with server-side URLs
    #Saints URL is required for the actual parsing of the list
    print(
        "Initiating get_saints_info with payload "
        + "domain:" + domain
        + " page:" + page
    )
    baseURL = domain
    saintsURL = domain + "/" + page
    #The following requests the Saints URL, parses down to the list of
    #   saints in the ul and populates the saintsURLs with the full link
    #   to be parsed in the future
    saints_info = []
    r = requests.get(saintsURL)
    soup = BeautifulSoup(r.text, features="html.parser")
    #locates the article tags, which house individual saint/feast celebrations
    article = soup.find_all('article')
    for art in article:
        saint_info = []
        #Saint/feast name is housed in <h2> tag, pulls & appends it to saint_info
        saint_name = art.find('h2').text.strip()
        saint_info.append(saint_name + "^")
        #url to individual saint/feast page is received, and appended
        saint_page = baseURL + art.find_all('a')[1].get('href')
        saint_info.append(saint_page + "^")
        #print("get_saints_info | " + "added: " + saint_name)
        #if there is an image associated with this <article> tag...
        if art.find('img') is not None:
            #parse the HTML of that saint/feast's page
            r = requests.get(saint_page)
            soup = BeautifulSoup(r.text, features="html.parser")
            image = soup.find_all('span')[0]
            #gather link (.jpg) of image file from page
            icon = image.find('a').get('href')
            #append image URL to saint_info
            saint_info.append(icon + "^")
        else:
            pass
        #By default, each <article> tag has 3 links (2 to the individual page,
        #   and 1 to the image) - if more links are present, they are for the
        #   troparion & kontakion
        if len(art.find_all('a')) > 2:
            #the troparion will be the link at index 2
            saint_tak = baseURL + art.find_all('a')[2].get('href')
            r = requests.get(saint_tak)
            soup = BeautifulSoup(r.text, features="html.parser")
            hymns = soup.find_all('article')
            #troparion & kontakion are stored in <article> tags. index 0 is
            #   the "read the life" link, troparion & kontakion are index 1+
            for hymn in hymns[1:]:
                try:
                    saint_info.append(hymn.text.strip() + "^")
                    #print(hymn.text.strip())
                except:
                    pass
        else:
            #If no troparion or kontakion is found...
            pass
        #append individual saint_info to collective saints_info list
        saints_info.append(saint_info)
    #once all saints' info is collected, return the full list for processing
    return saints_info

def get_fasting_info(domain:str, page:str):
    #Base URL is required for concatenating with server-side URLs
    #Fasting URL is required for the actual parsing of the list
    print(
        "Initiating get_fasting_info with payload "
        + "domain:" + domain
        + " page:" + page
    )
    baseURL = domain
    fastingURL = domain + "/" + page
    fasting_details = []
    r = requests.get(fastingURL)
    soup = BeautifulSoup(r.text, features="html.parser")
    detail = soup.find('div', class_="oc-fasting").find('p').text.split("|")
    if detail[0] =='Fast Free':
        detail[0] = 'Today is Fast Free'
    for item in detail:
        fasting_details.append([item.strip()])
        print("get_fasting_info | added: " + item)
    return fasting_details


readings_tweet_thread = utils.extract_line_from_file("data","readings.txt","|",-1)
print(readings_tweet_thread)
