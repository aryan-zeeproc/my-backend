from fastapi import FastAPI
from google.cloud import pubsub_v1
import logging

# --- Hardcoded values ---
GCP_PROJECT = "test-project-443004"
PUBSUB_TOPIC = "test"

# --- Setup ---
app = FastAPI()
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(GCP_PROJECT, PUBSUB_TOPIC)

logging.basicConfig(level=logging.INFO)

@app.post("/")
def root():
    return {"message": "Hello from AI Server!"}

@app.get("/publish")
def publish_message():
    message = "Hello from App A!"
    
    # Publish and wait for result
    future = publisher.publish(topic_path, message.encode("utf-8"))
    message_id = future.result()  # Blocks until the message is published

    logging.info(f"Published message with ID: {message_id}")
    return {"status": "published", "message_id": message_id}



from google.cloud import tasks_v2
import json

PROJECT = "test-project-443004"
QUEUE = "test-queue"
LOCATION = "us-central1"
AI_URL = "https://72307f4ed1a9.ngrok-free.app/do-work"

client = tasks_v2.CloudTasksClient()
parent = client.queue_path(PROJECT, LOCATION, QUEUE)

@app.get("/create-task")
def create_task():
    payload = {"message": "Hello from Backend!"}

    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": AI_URL,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(payload).encode()
        }
    }

    response = client.create_task(parent=parent, task=task, timeout=30)
    print("📤 Task created:", response.name)

    return {"status": "task created", "task": response.name}
