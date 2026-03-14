
# watcher.py

import redis
import json
import time
import re

def watcher_start(redis_conf, log_queue, log_file_path="markov_flow.log"):
    r = redis.Redis(**redis_conf)
    
    try:
        with open(log_file_path, 'r') as file:
            file.seek(0, 2)
            
            while True:
                reader = file.readline()
                pattern = r'\[(.+?)\]\s+(\w+)\s+(\S+)\s+(.+)'
                
                if not reader:
                    time.sleep(0.2)
                    continue

                match = re.match(pattern, reader.strip())
                
                try:
                    log_entry = {
                        "timestamp" : match.group(1),
                        "level" : match.group(2),
                        "event" : match.group(3),
                        "message" : match.group(4)
                    }
                    
                    r.lpush(log_queue, json.dumps(log_entry))
                    
                except json.JSONDecodeError:
                    print(f"Skipping malformed line: {reader.strip()}")
                    
    except FileNotFoundError:
        print(f"Error: The file {log_file_path} was not found.")
    
    except:
        print("Your file path does not exist")

