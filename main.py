import multiprocessing
from worker import worker_start
from watcher import watcher_start

if __name__ == "__main__":
    n = int(input())
    
    log_queue = multiprocessing.Queue()
    manager = multiprocessing.Manager()
    manager_dict = manager.dict()
    
    watcher1 = multiprocessing.Process(watcher_start, args = (log_queue, ))
    watcher1.start()
    workers = []
    
    for _ in range(n):
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