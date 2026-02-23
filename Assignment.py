import requests
from bs4 import BeautifulSoup as bs
import sys
url="https://neetcode.io/practice/practice/neetcode150"
url=sys.argv[1]
response=requests.get(url)

def get_body_tittel_link(response):
    sowp = bs(response.text,"html.parser")
    body = sowp.body.get_text()
    cleanbody=""
    for char in body:
        if char.isalnum():
            cleanbody+=char
        else:
            cleanbody += " "
    title = ""
    if(sowp.title):
        title = sowp.title.string
    links = []
    for tag in sowp.find_all('a'):
        href = tag.get('href')
        if href:
            links.append(href)
    return cleanbody,title,links

body,title,links=get_body_tittel_link(response)


def word_count(str):
    word_list=str.split()
    word_frequency={}
    for word in word_list:
        if word in word_frequency:
            word_frequency[word]+=1
        else:
            word_frequency[word]=1
    return word_frequency