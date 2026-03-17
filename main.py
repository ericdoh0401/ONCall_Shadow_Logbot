
# main.py
import time
import multiprocessing
from worker import worker_start
from watcher import watcher_start
import signal
import redis
import logging

# --REDIS CONFIGURATION--
REDIS_CONF = {
    'host' : 'localhost',
    'port' : 6379,
    'db' : 0
}
LOG_QUEUE = "log_pipeline_queue"

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s | %(processName)s | %(levelname)s | %(message)s'
)

if __name__ == "__main__":
    n = int(input("Enter number of worker processes: "))
    
    start_time = time.time()
    
    # place the redis_conf as a parameters so that the watcher knows where to push the data
    watcher = multiprocessing.Process(
        target = watcher_start, 
        args = (REDIS_CONF, LOG_QUEUE,)
    )
    watcher.start()
    
    workers = []
    for _ in range(n):
        # each worker will get the same address, so that they all connect to the same Redis
        # instance to pull data
        workerI = multiprocessing.Process(
            target = worker_start, 
            args = (REDIS_CONF, LOG_QUEUE,)
        )
        workerI.start()
        workers.append(workerI)
        
    print("System Online.")
    
    try:
        watcher.join()
    
    except KeyboardInterrupt:
        print("Stopping the system...")
        
        watcher.terminate()
        
        r = redis.Redis(**REDIS_CONF)
        
        # Sending shutdown signals to all workers
        
        for _ in range(n):
            r.lpush(LOG_QUEUE, "SHUTDOWN_SIGNAL")
        
        for workerI in workers:
            workerI.join()
            
    total_time = time.time() - start_time
    
    print(f"Whole session took duration={total_time:.4f}s")
    print("System Offline...")
