
# watcher.py
import json
import time
from sortedcontainers import SortedList

PADDING = 404040
HR_PADDING = 24000000

def watcher_start(log_queue, log_file_path = "your_file.log"):
    
    try:
        with open(log_file_path, 'r') as file:
            
            # the primary reason we are calling this function in the first place is to collect recently
            # occurring errors
            file.seek(0, 2)
            
            while True:
                reader = file.readline()
                
                if not reader:
                    # without a pause, the while loop will run millions of lines of code per second
                    # asking the Hard Drive whether there is a new line yet: will max out one of the CPUs.
                    time.sleep(0.2)
                    continue
                
                log_entry = json.loads(reader.strip())
                log_queue.put(log_entry)
    
    except:
        print("Your file path does not exist")