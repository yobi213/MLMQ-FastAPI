from fastapi import FastAPI
import uvicorn
import json
from consumer import Consumer
from publisher import Publisher,Sample
from STT import STT_layout


app = FastAPI()


# RabbitMQ 연결

@app.route("/health")
async def health_check():
    return "OK"

#publish test
@app.get("/pub")
async def pub():
    data = {
        "rec_id": 1,
        "name": "My Name",
        "text": "배송이 느려요"
    }

    message = json.dumps(data)
    publisher = Publisher()
    publisher.main(message)

    return

# get 방식으로 샘플 데이터 생성
@app.get("/sample")
async def sample():
    data = {
        "rec_id": 1,
        "name": "My Name",
        "text": "배송이 빨라"
    }
    message = json.dumps(data)
    publisher = Sample()
    publisher.main(message)

    return


#post 방식으로 샘플 데이터 생성
@app.post("/create")
async def create(data: STT_layout):

    data = dict(data)
    message = json.dumps(data)
    publisher = Sample()
    publisher.main(message)
    return

#@app.on_event("startup")
@app.get("/con")
async def startup():
    consumer = Consumer()
    consumer.main()

    return

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)