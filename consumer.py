import asyncio
import logging

import aio_pika


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@rabbitmq/?name=consumer_asyncio",
    )

    queue_name = "test_queue"

    async with connection:
        channel = await connection.channel()

        await channel.set_qos(prefetch_count=10)

        queue = await channel.declare_queue(queue_name)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print(message.body)


if __name__ == "__main__":
    asyncio.run(main())
