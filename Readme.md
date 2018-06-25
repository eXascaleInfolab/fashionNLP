# FashionNLP: natural language processing tool for fahion textual dataset.

EU project 732328: "Fashion Brain".

D2.1: "Named entity recognition and linking methods".

## Getting started

### Installation:
``` bash 
git clone https://github.com/eXascaleInfolab/fashionNLP.git
cd fashionNLP/
```

### Description of the "fashionNLP" package
The ”fashionnlp” package contains the following files:
- updateFBT.py: This code performs the following tasks:
	1) Take a concept present in WikiKB as input. 
	2) Find the mentions of this concept and its similar concepts (using String matching and tree search) in instagram posts.
	3) Find if the WikiKB concept is present in FBtaxonomy. If not, update the FB taxonomy.
- wikitaxonomy.py: This file is used to generate the wikipedia taxonomy from the wikipedia categorisation https://en.wikipedia.org/wiki/Category:Clothing_by_type
- input folder: This folder contains the following input files:
	1) FBTaxonomy.csv: The initial FashionBrain taxonomy in a csv format.
	2) Find the mentions of this concept and its similar concepts (using String matching and tree search) in instagram posts.
	3) FBTaxonomy.csv: The initial FashionBrain taxonomy in a json format.
	4) ner_posts.csv: This file contains the output result of applying SENNA on the instagram posts.
	5) wikipediaKB.json: This file contains the wikipedia knowledge base of fashion items in a json format.
- result folder:This folder contains the updated taxonomy

 

### Running the code 
In order to run an experiment, the updateFBT.py file is used. 

The corresponding command line to run the code is :
``` bash 
python updateFBT.py
```
