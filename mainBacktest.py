
# main.py

import multiprocessing
from worker import worker_start
from watcher import watcher_start
import signal
import redis

FILE_PATH = "markov.log"

# --REDIS CONFIGURATION--
REDIS_CONF = {
    'host' : 'localhost',
    'port' : 6379,
    'db' : 0
}
LOG_QUEUE = "log_pipeline_queue"

if __name__ == "__main__":
    n = int(input("Enter number of worker processes: "))

    with open(FILE_PATH, 'a') as f:
        for _ in range(n):
            f.write("SHUTDOWN_SIGNAL" + "\n")
    
    # place the redis_conf as a parameters so that the watcher knows where to push the data
    watcher = multiprocessing.Process(
        watcher_start, 
        args = (REDIS_CONF, LOG_QUEUE,)
    )
    watcher.start()
    
    workers = []
    for _ in range(n):
        # each worker will get the same address, so that they all connect to the same Redis
        # instance to pull data
        workerI = multiprocessing.Process(
            worker_start, 
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
        
        r = redis.Redis(host=REDIS_CONF['host'], port=REDIS_CONF['port'], db=REDIS_CONF['db'])
        
        # Sending shutdown signals to all workers
        
        for _ in range(n):
            r.lpush(REDIS_CONF[LOG_QUEUE], "SHUTDOWN_SIGNAL")
        
        for workerI in workers:
            workerI.join()
            
    print("System Offline...")
