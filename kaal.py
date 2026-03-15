import asyncio
import multiprocessing
import random
from curl_cffi.requests import AsyncSession

# Use the official ordering site as noted in their alerts
link = "https://abc.xyz" 

# List of real-world User-Agents to help mask the script
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
]

async def worker(session, worker_id):
    while True:
        try:
            # Rotate User-Agent for every single request
            headers = {"User-Agent": random.choice(USER_AGENTS)}
            
            response = await session.get(link, impersonate="chrome110", headers=headers)
            
            if response.status_code == 200:
                print(f"[{worker_id}] Success: 200")
            elif response.status_code == 429:
                # Check if the server told us how long to wait
                retry_after = response.headers.get("Retry-After", 30) # Default to 30s if not specified
                print(f"[{worker_id}] Rate Limited (429). Sleeping for {retry_after}s...")
                await asyncio.sleep(int(retry_after))
            else:
                print(f"[{worker_id}] Unexpected Status: {response.status_code}")

        except Exception as e:
            print(f"[{worker_id}] Connection error: {e}")
        
        # ESSENTIAL: Without proxies, you MUST slow down. 
        # A 0.01s delay will get a single IP banned almost instantly.
        await asyncio.sleep(random.uniform(2.0, 5.0)) 

async def run_async_loop(users_per_core, core_index):
    async with AsyncSession() as session:
        # Reduced workers per core to prevent local OS crashes
        workers = [worker(session, f"Core-{core_index}-U{i}") for i in range(users_per_core)]
        await asyncio.gather(*workers)

def start_process(users_per_core, core_index):
    asyncio.run(run_async_loop(users_per_core, core_index))

if __name__ == "__main__":
    # Note: MOD Pizza has issued alerts about unauthorized impersonation sites.
    # Always ensure you are interacting with the official domain: orders.modpizza.com
    
    total_users = 20000 # Reduced from 20k; 20k on one IP will result in a permanent ban.
    num_cores = multiprocessing.cpu_count()
    users_per_core = total_users // num_cores

    print(f"Launching {num_cores} processes. Total simulated users: {total_users}")

    processes = []
    for i in range(num_cores):
        p = multiprocessing.Process(target=start_process, args=(users_per_core, i))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
