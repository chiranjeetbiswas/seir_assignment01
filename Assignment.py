import requests
from bs4 import BeautifulSoup as bs
import sys

def get_body_title_link(response):
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



def word_count(str):
    word_list=str.split()
    word_frequency={}
    stopwords=["the", "is", "am", "are" ,"not" ,"a" ,"very"]
    for word in word_list:
        if word in stopwords:
            continue
        if word in word_frequency:
            word_frequency[word]+=1
        else:
            word_frequency[word]=1
    return word_frequency


def Hash(word,p=53,m=2**64):
    hash=0
    for i in range(len(word)):
        hash+=ord(word[i])*(p**i)
    hash=hash%m
    return hash

def compute_simhash(word_frequency):
    vector=[0 for k in range(64)]
    for key in word_frequency:
        hashValue=Hash(key)
        for i in range(64):
            bit=(hashValue>>i)&1
            if bit==1:
                vector[i]+=word_frequency[key]
            else:
                vector[i]-=word_frequency[key]
        
    simhash_Code=0
    for i in range(len(vector)):
        if vector[i] > 0:
            simhash_Code+=1*(2**i)
        else:
            simhash_Code+=0*(2**i)
    return simhash_Code

def compair_Two_page(url_1,url_2):
    url_1,url_2=sys.argv[1],sys.argv[2]
    response1,response2=requests.get(url_1),requests.get(url_2)
    body1,title1,links1=get_body_title_link(response1)
    body2,title2,links2=get_body_title_link(response2)


