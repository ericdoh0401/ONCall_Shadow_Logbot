import json
import time

PADDING = 404040
HR_PADDING = 24000000

def watcher_start(log_queue, log_file_path = "filepath.log"):
    try:
        with open(log_file_path, 'r') as file:
            file.seek(0, 2)
            
            while True:
                reader = file.readline()
                
                if not reader:
                    time.sleep(0.2)
                    continue
                
                log_entry = json.loads(reader.strip())
                log_queue.put(log_entry)
    
    except:
        print("Your file path does not exist")