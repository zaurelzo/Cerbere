# Cerbere

syntaxic and semantic web indexer and their search engine

## Install
  ```bash
    chmod +x install.sh;  sudo install.sh
  ```


## How to use the project ? 
  First of all, you need to index all html documents.You need to have mySQL database called cerbere_db
  To run it:
```bash
  python indexation number
```
  number must be 0 (to delete cerbere_db tables) or  1 (to create cerbere_db tables) or 2 (to run the indexation)


## Run the syntaxic search engine
  The syntaxic search engine is implemented in the file search.py
  To run it : 
  ```bash
   python search.py <TF|TF_IDF> <1|2|3|4> <perQuery|total>
  ```
  *the first parameter is term ponderation : TF or TF*IDF
  *the second paramter is the similarity method used  : 1: inner product, 2:Coef. de Dice, 3:Cosinus measure, 4: Jaccard measure
  *the fird paramater enable to run the query for just the parametered method (perQuery) or run the query for all methods(total)  
  


## Run the semantic search engine
  The syntaxic search engine is implemented in the file searchSemantic.py
  Youn need to install the fuseki server if you want to use this method. You will also need to rename the ontology used. It's can be done 
  by renamed it in the file sparqlRequest.py
  To run it : 
  ```bash
    python searchSemantic.py <TF|TF_IDF> <1|2|3|4> <perQuery|total> 
    <ref1(list syn)|ref2(combinaisons)|ref3(list syn avec poids) | ref4 | ref4+ > <ref1(list syn)|ref2(combinaisons)|ref3> <sum|max>
  ```