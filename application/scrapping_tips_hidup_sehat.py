
import requests
import html5lib
from bs4 import BeautifulSoup as bs
import pandas as pd
from flask import jsonify
from . import mysql


def tips():
    link = 'https://upk.kemkes.go.id/new/5-tips-sehat-selama-bulan-ramadhan'
    req = requests.get(link)
    soup = bs(req.content, 'html5lib')
    
    h4 = soup.findAll('h4',{'class':'blog-title'or'post-title'or'pmb-posts'or'entry-title'or'title'})
    h3 = soup.findAll('h3',{'class':'blog-title'or'post-title'or'pmb-posts'or'entry-title'or'title'})
    h2 = soup.findAll('h2',{'class':'blog-title'or'post-title'or'pmb-posts'or'entry-title'or'title'})
    h1 = soup.findAll('h1',{'class':'blog-title'or'post-title'or'pmb-posts'or'entry-title'or'title'})
    print(h4,h3,h2)
    if h4 == []:
        if h3 == []:
            if h2 == []:
                if h1 == []:
                    title = ''
                else:
                    title = h1[0].text
            else:
                title = h2[0].text
        else:
            title = h3[0].text
    else:
        title = h4[0].text
    print(title)
    paragraphs = soup.findAll('p')

    text = []
    for p in paragraphs:
        print(p.text)
        if p.text == '':
            pass
        elif p.text == ' ':
            pass
        elif "Selamat Datang" in p.text:
            pass
        else:
            text.append(p.text)

    text.pop(2)
    print(text)
    text_ready =' '.join(text[0:-1])
    print(text_ready)
    respon = []
    dictlogs = {}
    status= False
    dictlogs.update({"title": title,"isi":text_ready,"sumber":link})
    cur = mysql.connection.cursor()
    mysql.connection.commit()
    respon.append(dictlogs)
    return respon