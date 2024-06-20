import aiohttp
import asyncio
import os

counter = 0

backend_url = os.getenv('BACKEND_URL', 'http://backend-service:5001')

async def wait_for_backend(session):
    while True:
        try:
            async with session.get(f'{backend_url}/hello') as response:
                if response.status == 200:
                    print("Backend service is available.", flush=True)
                    return
        except aiohttp.ClientConnectionError:
            pass
        print("Waiting for backend service...", flush=True)
        await asyncio.sleep(1)

async def main():
    global counter
    async with aiohttp.ClientSession() as session:
        await wait_for_backend(session)
        while True:
            counter += 1
            try:
                async with session.get(f'{backend_url}/hello') as response:
                    backend_message = await response.json()
                    print(f"Hello from client, iteration {counter}", flush=True)
                    print(f"Backend says: {backend_message['message']}, iteration {backend_message['iteration']}", flush=True)
            except Exception as e:
                print(f"Error: {e}", flush=True)
            await asyncio.sleep(1)  # Reduced the sleep interval

if __name__ == '__main__':
    asyncio.run(main())
