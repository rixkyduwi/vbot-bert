
import requests
import html5lib
from bs4 import BeautifulSoup as bs
import pandas as pd
from flask import jsonify
from __init__ import mysql


def tips():
    link = 'https://www.alodokter.com/delapan-langkah-menuju-pola-hidup-sehat'
    req = requests.get(link)
    soup = bs(req.content, 'html5lib')
    
    titles = soup.findAll('h4')
    paragraphs = soup.findAll('p')

    text = []
    for title in titles:
        for p in paragraphs:
            text.append(title.text)
            text.append(p.text)
        
    text_ready = ' '.join(text[5:7])
    print(text_ready)
    respon_model = []
    dictlogs = {}
    status= False
    dictlogs.update({"status": status,"deskripsi":text_ready})
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tips_sehat(tips) VALUES(%s)" , (text_ready))
    mysql.connection.commit()
    respon_model.append(dictlogs)
    return jsonify(respon_model)