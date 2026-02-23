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