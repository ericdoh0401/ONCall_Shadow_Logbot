
 
# main.py
import multiprocessing
from worker import worker_start
from watcher import watcher_start

if __name__ == "__main__":
#     The Queue: By default, multiprocessing.Queue is already built to be shared across processes. It has "Locks" built into its code. When Worker 1 tries to get() an item, the Queue automatically "locks" itself so Worker 2 can't touch it. It is self-managing.

# The List/Dict: Standard Python lists and dicts are not thread-safe or process-safe. If two workers tried to update a standard dictionary at the exact same nanosecond, the data would get corrupted (this is a "Race Condition"). The Manager()'s job is to wrap that dictionary in a "security guard" so it can be shared safely.
    
    
    log_queue = multiprocessing.Queue()
    manager = multiprocessing.Manager()
    manager_dict = manager.dict()
    
    watcher1 = multiprocessing.Process(watcher_start, args = (log_queue, ))
    watcher1.start()
    workers = []
    
    for _ in range(2):
        workerI = multiprocessing.Process(worker_start, args = (log_queue, manager_dict, ))
        workerI.start()
        workers.append(workerI)
    
    try:
        watcher1.join()
    
    except KeyboardInterrupt:
        print("Stopping the system...")
        
        watcher1.terminate()
        
        for _ in range(len(workers)):
            log_queue.put(None)
        
        for workerI in workers:
            workerI.join()
            
    print("System Offline...")


