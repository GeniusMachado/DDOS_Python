

import asyncio

async def main():
	users = 20000
	link = "https://abc.xyz"
	workers = [worker for _ in range(users)]
	asyncio.gather(*workers)

async def workers(session):
	asyncsession




if __name__ = "__main__":
	asyncio.run(main)
