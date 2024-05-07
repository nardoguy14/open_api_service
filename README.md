# About

This project aims to utilize OpenAI apis to answer questions on current topics. To meet this goal we create ebeddings created
by OpenAI for source data that we then store into a Mivilus vector database. With this stored set of source data and created
ebeddings we are then able to ask the service a question, find common embeddings we have stored, and provide the related 
source data to those alike ebeddings to OpenAI with their chatgpt model to ask a question. The last part or more so the first
part of aggregated the data is done by data scrapping a website endpoint. We define the data scrapper to dive N levels deep 
and store the related text into the database. When answers can't be question regarding source content, it is generally adviseable
to define a deeper level for the data scrapper to dig down through. We are sure not to reconstruct embeddings for urls we
have already seen hence not incurring any unnecessary costs.

# Dependencies

You will need to set the following environment variables:

One thing you will need to get is an api key to hit OpenAI endpoints. Calls to this endpoint aren't free. You
will need to sign up to attain your own key here: https://platform.openai.com/docs/quickstart

```shell
      export MIVILUS_HOST=http://standalone
      export MIVILUS_PORT=19530
      export OPENAI_API_KEY=< place your own api key here >
```

# Running the Service
This will stand up all the needed containers that constitute the service including the RESTful service, a selenium container,
and a Mivilus vector database along with its dependencies.

```shell
docker-compose up
```

# Calling the Service

The available endpoints can be seen at `http://localhost:8009`. You will be able to call the ingestion api and question
endpoint.

# Design

## Ingestion of Website Content to Embeddings
![Blank diagram - Page 2.png](images%2FBlank%20diagram%20-%20Page%202.png)

## Using Stored Embeddings to Ask ChatGPT Questions
![Blank diagram - Page 3.png](images%2FBlank%20diagram%20-%20Page%203.png)
