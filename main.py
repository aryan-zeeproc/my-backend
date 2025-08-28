# fastapi-app-a/main.py
from fastapi import FastAPI
from google.cloud import pubsub_v1
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(os.environ["GCP_PROJECT"], os.environ["PUBSUB_TOPIC"])

@app.post()
def root():
    return {"message": "Hello from AI Server!"}

@app.get("/publish")
def publish_message():
    message = "Hello from App A!"
    publisher.publish(topic_path, message.encode("utf-8"))
    return {"status": "published"}
