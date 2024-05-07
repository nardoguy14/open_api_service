# About

This project aims to utilize OpenAI apis to answer questions on current topics. To meet this goal we create ebeddings created
by OpenAI for source data that we then store into a Mivilus vector database. With this stored set of source data and created
ebeddings we are then able to ask the service a question, find common embeddings we have stored, and provide the related 
source data to those alike ebeddings to OpenAI with their chatgpt model to ask a question. The last part or more so the first
part of aggregated the data is done by data scrapping a website endpoint. We define the data scrapper to dive N levels deep 
and store the related text into the database. When answers can't be question regarding source content, it is generally adviseable
to define a deeper level for the data scrapper to dig down through. We are sure not to reconstruct embeddings for urls we
have already seen hence not incurring any unnecessary costs.

# Design

## Ingestion of Website Content to Embeddings
![Blank diagram - Page 2.png](images%2FBlank%20diagram%20-%20Page%202.png)

## Using Stored Embeddings to Ask ChatGPT Questions
![Blank diagram - Page 3.png](images%2FBlank%20diagram%20-%20Page%203.png)
