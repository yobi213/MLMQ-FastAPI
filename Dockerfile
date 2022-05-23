From python:3.8
RUN \
    apt-get update && \
    apt-get install -y vim

COPY src src
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "src/mlmq.py"]