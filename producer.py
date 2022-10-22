import aio_pika
from fastapi import FastAPI
from pydantic import BaseModel


class Task(BaseModel):
    task_id: str
    description: str
    params: dict


app = FastAPI()


@app.post("/add_task/")
async def add_task(task: Task):
    routing_key = "test_queue"
    channel = await app.rq_connection.channel()

    msg = task.json().encode()
    queue = await channel.declare_queue(routing_key)
    result = await channel.default_exchange.publish(
        aio_pika.Message(body=msg),
        routing_key=routing_key,
    )

    return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@rabbitmq/?name=publisher_fastapi",
    )
    app.__setattr__('rq_connection', connection)


@app.on_event("shutdown")
async def shutdown_event():
    await app.rq_connection.close()
