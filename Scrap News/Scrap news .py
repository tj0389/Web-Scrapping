import bs4
import requests
from selenium import webdriver
import json
import numpy as np
import urllib
import cv2
from PIL import Image
import requests
import matplotlib.pyplot as plt

def get_headers():
    return {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-IN,en-US;q=0.9,en;q=0.8",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "__cfduid=dc953a47fbc0ce87571d964d494d236e61598518238; _ga=GA1.2.180493284.1598518241; _gid=GA1.2.167481700.1598518241; _fbp=fb.1.1598518241000.778698853; __gads=ID=5e96bf13f4e28b9a:T=1598518243:S=ALNI_MbxZesVMCAC7zcNZlODtALn95Rygw; _gat=1",
        "origin": "https://inshorts.com",
        "referer": "https://inshorts.com/en/read/",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

def news(data):
    soup=bs4.BeautifulSoup(data)
    for dataAll in soup.find_all('div',{'class':'news-card z-depth-1'}):     
        pic=dataAll.find('div',{'class':'news-card-image'}).attrs['style']
        path=pic[23:-3]
        response = requests.get(path, stream=True)
        img = Image.open(response.raw)
        plt.imshow(img)
        plt.axis('off')
        plt.show()
        data=dataAll.find('div',{'class':'news-card-title news-right-box'}).span
        print("Headline -",data.text)
        data=dataAll.find('div',{'itemprop':'articleBody'})
        with open("head.txt","a",encoding="utf8") as f:
            f.write(data.text)
        print("Description -",data.text)
        data=dataAll.find('a',{'class':'source'})
        if (data!=None):
            print("Read More -",data.get('href'))
        print("\n \n")

url="https://inshorts.com/en/read"
data=requests.get(url)
try:
    news(data.content)

    url = 'https://inshorts.com/en/ajax/more_news'
    news_offset = "o9wyecy6-1"

    while True:
        response = requests.post(url, data={"category": "", "news_offset": news_offset}, headers=get_headers())
        if response.status_code != 200:
            print(response.status_code)
            break

        response_json = json.loads(response.text)
        news(response_json["html"])
        news_offset = response_json["min_news_id"]
except:
    print("CONGRATS ....  YOU READ ALL THE LATEST NEWS")



