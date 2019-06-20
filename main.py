import sys
import time
import requests
import re
from bs4 import BeautifulSoup

MAX_VISITS = 100

def get_to_philosophy(url):
    counter = 0

    while counter < MAX_VISITS:
        print(str(counter) + ". " + url)
        if url == 'http://en.wikipedia.org/wiki/Philosophy':
            print("Reached the Philosophy page!")
            break
        #get the page
        r = requests.get(url)
        #get the html text
        html_text = BeautifulSoup(r.text, features="lxml")
        #a Wikipedia article main body is always in a div with id: mw-content-text
        #extract the main article body
        content = html_text.find(id='mw-content-text')
        #html tages to be removed: table, span
        tags_to_remove = content.find_all(['table', 'span'])
        if tags_to_remove != None:
            for tag_to_remove in tags_to_remove:
                tag_to_remove.extract()
        #get the p tags 
        paragraph = content.find('p', {"class": ""})
        #extract all links in the first paragraph
        all_links_tags = paragraph.find_all('a')
        #get the first Wikipedia link
        first_link = ''
        for link_tag in all_links_tags:
            link = link_tag.get('href')
            if link != None and bool(re.match(r'^/wiki/*', link)):
                first_link = link
                break

        url = 'http://en.wikipedia.org' + first_link
        counter += 1
        time.sleep(0.5)

    if counter == MAX_VISITS:
        print("Exceeded 100 visits!")

if __name__ == '__main__':
    if len(sys.argv)==1:
        print("Add a wikipedia link as a parameter!")
    else:
        url = sys.argv[1]
        get_to_philosophy(url)