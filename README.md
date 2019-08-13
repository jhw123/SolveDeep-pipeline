## Introduction

This is the manual for running the REST API server used for SolveDeep.

## How to Start

### Setting the Virtual Environment

```bash
$ virtualenv rest-env
$ source rest-env/bin/activate
```

Note that Python ver. 2.7 should be used. Use pip to download the packages required.

* flask
* pyrebase
* nltk
* gensim
* textdistance 

### Configure Database

Place db-config.json to the project root directory (the folder where the api.py is). Contact the project director to acquire the db-config.json file for accessing the Firebase DB.

### Run the API Server

```bash
$ python api.py
```

```
loading a word2vec model...
glove_vectors model is loaded successfully
```

Start the server takes time to load a word2vec model

## How to Use

Use [Insomnia](https://insomnia.rest/download/) or other REST client applications to test various queries.

Example queries are:

POST: [HOST\_URL]/w2v_similarity

```json
{
	"w1": "calculate",
	"w2": "variable"
}
```

You will get a response like:

```json
{
  "similarity": "0.5018222",
  "w1": "calculate",
  "w2": "variable"
}
```