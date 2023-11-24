# TwitterSentimentAnalysisGraphDB

This project aims at importing a previous MongoDB NoSQL document-based database for the sentiment analysis of the Tweets in Neo4j. The main objective is to compare performances between the two different systems on the selected queries of interest.

# Database

The database module contains:

* the `CRUD` folder, containing the CRUD operations,
* the `data` folder, containing the JSON files with the data to be loaded into the database,
* the `model.py` file.

## `model.py`

In order to deal with the graph database in Neo4j in a simpler way, I decided to use `neomodel` as `OGM` ([Object Graph Mapper](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjIv8Lq092CAxUwcvEDHcxcCBQQFnoECBcQAQ&url=https%3A%2F%2Fneo4j.com%2Fdocs%2Fogm-manual%2Fcurrent%2Fintroduction%2F&usg=AOvVaw3V8X64u8nYqBvVITygMH__&opi=89978449)), which is based on the `neo4j` python driver. This file contains the classes mapping the *nodes* and the *reationships* of the database.
