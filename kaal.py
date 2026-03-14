

import asyncio
from curl_cffi.requests import AsyncSession

link="https://csulb.edu"

async def main():
	async with AsyncSession() as session:
		users = 20000
		link = "https://abc.xyz"
		workers = [worker(session) for _ in range(users)]
		await asyncio.gather(*workers)

async def worker(session):
	while True:
		try:
			response = await session.get(link, impersonate="chrome110")
			print(response.status_code)
		except Exception as e:
			print("could not get a a response")
		await asyncio.sleep(0.01)




import asyncio
from curl_cffi.requests import AsyncSession
async def main():
        async with AsyncSession() as session:
                users = 20000
                workers = [worker(session) for _ in range(users)]
                await asyncio.gather(*workers)

async def worker(session):
        while True:
                try:
                        response = await session.get(link, impersonate="chrome110")
                        print(response.status_code)
                except Exception as e:
                        print("could not get a a response")
                await asyncio.sleep(0.01)





if __name__ == "__main__":
        asyncio.run(main())
               
