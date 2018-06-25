#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 12:38:48 2018

@author: inesarous
"""

#import urllib.request
from urllib2 import urlopen
import csv
import json

pages =urlopen('https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:Clothing_by_type&format=json&cmlimit=500&cmtype=subcat')
data = json.load(pages)
query = data['query']
category = query['categorymembers']
#print (category)
data={}
data['name']=('Category:Clothing_by_type')
recursiondepth=0
f=open('wikitaxonomy.csv','w')
with f:
    writer=csv.writer(f)
    def addchildren(category,recursiondepth):
        for x in category:
            #print (recursiondepth)
            title= (x['title'])
            if recursiondepth==1:
                writer.writerow('\t'+title+'\n')
            if recursiondepth==2:
                writer.writerow('\t\t'+title+'\n')
            if recursiondepth==3:
                writer.writerow('\t\t\t'+title+'\n')
            if (x['title'])=='Category:Hosiery':
                continue
            test='https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle='+x['title']+'&format=json&cmlimit=500&cmtype=subcat'
            #print (test)
            try:
                pages1 = urlopen(test)
                data1 = json.load(pages1)
                query1 = data1['query']
                category1 = query1['categorymembers']
                #print (category1)
                if addchildren(category1,recursiondepth+1):
                    #print (category1)
                    addchildren(category1)
            except:
                continue


    addchildren(category,1)