from fastapi import FastAPI
from pororo import Pororo
from pydantic import BaseModel



sentiment_model = None


app = FastAPI()

sentiment_model = Pororo(task='sentiment', model='brainbert.base.ko.shopping', lang='ko')


@app.get('/text_classification')
def model_health_check():

    if sentiment_model is None:
        return {'status': 400}


    return {'status': 200}


@app.get('/text_classification/sentiment/{query}')
def predict_sentiment(query: str):
    pred = sentiment_model(query)
    if pred == "Positive":
        pred = 1
    else:
        pred = 0

    return pred


