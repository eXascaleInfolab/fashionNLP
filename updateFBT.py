#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 12:36:08 2018

@author: inesarous
"""

import json
import csv
import Levenshtein

def ner(input_file):
    nlp = StanfordCoreNLP(r'./stanford-corenlp-full-2018-02-27')
    influencer_text=open(input_file,'r')
    with influencer_text as f:
        lines = f.readlines()
    

    for i in range(0,len(lines)): 
        sentence=lines[i]
        tokenized_sentence=nlp.word_tokenize(sentence)
        taged_sentence=nlp.pos_tag(sentence)
        ner=nlp.ner(sentence)
        print 'Tokenize:', nlp.word_tokenize(sentence)
        print 'Part of Speech:', nlp.pos_tag(sentence)
        print 'Named Entities:', nlp.ner(sentence)
        tags=[item[1] for item in taged_sentence]
        entity=[item[1] for item in ner]
        rows = zip(tokenized_sentence,tags,entity)
        with open("./input/ner_posts_standford.csv", "w") as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row)
        f.close()

def findchild(n,listofdescriptiveitems):
    for x in n['children']:
        listofdescriptiveitems.append(x['name'])
        if findchild(x,listofdescriptiveitems):
            findchild(x,listofdescriptiveitems)

def findchildren(x,text,listofdescriptiveitems):
    for n in x['children']:
        #print (n['name'].lower(),text)
        if (n['name']).lower()==text:
            listofdescriptiveitems.append(n['name'])
            findchild(n,listofdescriptiveitems)
            return n
        else:
            findchildren(n,text,listofdescriptiveitems)
            #print (n,text)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def findItemsInFile(taxonomy,text):
    listoffounditems=[]
    listofdescriptiveitems=[]
    children=findchildren(taxonomy,text,listofdescriptiveitems)
    #f.close()
    #print (listofdescriptiveitems)
    itemlist = csv.reader(open('./input/ner_posts.csv', "r"))
    for row in itemlist:
        if (len(row))>=3:
            #print (row[0].lower().strip())
            for item in listofdescriptiveitems:
                if (str(item).lower() in (row[0].lower().strip())) or Levenshtein.ratio(str(item).lower(),(row[0].lower().strip()))>0.8:
                    #print (row[0].lower().strip())
                    listoffounditems.append(row[0].lower().strip())
                #if str(item).lower() in (row[0].lower().strip()):
                    #print (row[0].lower().strip())
    return (listofdescriptiveitems,listoffounditems)

def findHierarchy(taxonomy,text):
    listofdescriptiveitems=[]
    children=findchildren(taxonomy,text,listofdescriptiveitems)
    return (children)

def find(key, dictionary):
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result

                    

def updateFBtaxonomy(descItems):
    with open('./input/wikipediaKB.json','r') as f1:
        Wikitaxonomy=json.load(f1)
        for n in descItems:
            #print (n)
            children=findHierarchy(Wikitaxonomy,itemToSearch)
            ##find the longest child
            ##update later
            #print (children['name'])
            lookup=(children['children'][0]['name'])
            print (lookup)
            
            with open('./input/FBtaxonomy.json','r') as f2:
                FBtaxonomy=json.loads(f2.read())
                result=find('name',FBtaxonomy)
                for n in result:
                    if (n.lower()==lookup.lower()):
                        print ("Found in FB taxonomy; update csv")
                        
    with open('./input/FBtaxonomy.csv','r') as f2:
        with open('./output/updated_FBtaxonomy.csv','w') as f3:
            FBTaxonomycsv_modified=csv.writer(f3)
            FBTaxonomycsv=csv.reader(f2)
            print (lookup)
            flagitem=False
            i=0
            j=0
            for i,row in enumerate(FBTaxonomycsv):
                FBTaxonomycsv_modified.writerow(row)
                for j,field in enumerate(row):
                    if field.lower().strip()==lookup.lower().strip():
                        print ('item found at row '+str(i)+', column '+str(j))
                        flagitem=True
                        break
                if flagitem==True:
                    break
            row[j]=itemToSearch
            FBTaxonomycsv_modified.writerow(row)

            for Loopn,row in enumerate(FBTaxonomycsv):
                    FBTaxonomycsv_modified.writerow(row)
                    #print (Loopn,row)

def main():
    
    f=open('./input/wikipediaKB.json','r')
    taxonomy=json.load(f)
    f.close()
    itemToSearch='shawls'
    #listofdescriptiveitems=[]
    listofdescriptiveitems,listoffounditems=findItemsInFile(taxonomy,itemToSearch)
    print (listofdescriptiveitems,listoffounditems)
    #With Wikipedia taxonomy, try eyewear, jackets etc. 
    s=set(listoffounditems)
    if s:
        descItems=[]
        foundItems=[]
        for n in s:
            f1=open('./input/FBtaxonomy.json','r')
            FBtaxonomy=json.load(f1)
            f1.close()
            descItems,foundItems=findItemsInFile(FBtaxonomy,n)
            #print (descItems,foundItems)
        if (not(descItems)):
            print ('Item: ' + itemToSearch+' not found in FB taxonomy')
            updateFBtaxonomy(listofdescriptiveitems)
itemToSearch='shawls'
if __name__=="__main__":
    main()