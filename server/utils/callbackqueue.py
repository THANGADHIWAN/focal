import asyncio
import logging
import traceback
from typing import Callable, Any

class CallbackQueue:
    def __init__(self, name: str, queue_size: int, pool_size: int):
        self.name = name
        self.queue = asyncio.Queue(maxsize=queue_size)
        self.pool_size = pool_size
        self.workers = []
        self.shutdown_event = asyncio.Event()
        self.logger = logging.getLogger(__name__)

        # Start the worker threads
        for i in range(pool_size):
            worker = asyncio.create_task(self.worker(i))
            self.workers.append(worker)

    async def worker(self, worker_id: int):
        self.logger.info(f"CallbackQueue worker {worker_id} started.")
        while not self.shutdown_event.is_set():
            try:
                callback = await self.queue.get()
                await self.exec(callback)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in worker {worker_id}: {e}")
                traceback.print_exc()

    async def exec(self, callback: Callable[[], Any]):
        try:
            await callback()
        except Exception as e:
            self.logger.error(f"Callback error: {e}")
            traceback.print_exc()

    def enqueue(self, callback: Callable[[], Any]):
        if self.shutdown_event.is_set():
            self.logger.debug("CallbackQueue skipping enqueue, notifier is shutdown")
            return

        try:
            self.queue.put_nowait(callback)
        except asyncio.QueueFull:
            self.logger.warning("CallbackQueue queue backlog, skipping callback")

    async def shutdown(self):
        self.shutdown_event.set()
        await self.queue.join()  # Wait for all queued callbacks to finish
        for worker in self.workers:
            worker.cancel()
        await asyncio.gather(*self.workers, return_exceptions=True)  # Wait for all workers to finish
        self.logger.info("CallbackQueue shutdown complete.")

# Example usage in FastAPI

app = FastAPI()
callback_queue = CallbackQueue(name="ExampleQueue", queue_size=10, pool_size=4)

@app.post("/enqueue")
async def enqueue_callback():
    # Define a callback function
    async def example_callback():
        await asyncio.sleep(1)  # Simulate some work
        print("Callback executed")

    callback_queue.enqueue(example_callback)
    return {"message": "Callback enqueued"}

@app.on_event("shutdown")
async def shutdown_event():
    await callback_queue.shutdown()
