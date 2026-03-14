
# worker.py

from collections import deque
from datetime import datetime
from slack import send_slack_alert_manual
import queue
import redis
import time
import uuid

WINDOW_SIZE = 100
ERROR_MSG_FLAG = 50

def worker_start(redis_conf, log_queue):
    r = redis.Redis(**redis_conf)
    
    while True:
        try:
            _, raw_data = r.brpop(redis_conf[log_queue])
            decoded_data = raw_data.decode('utf-8')
            
            if decoded_data == "SHUTDOWN_SIGNAL":
                # terminate worker
                print("Worker has received a shutdown signal. Exiting...")
                break
            
            element = json.get(decoded_data)
                
            lvl = element.get("level", "")
            msg = element.get("message", "")
            time = element.get("timestamp", "")

            title = f"{lvl}: {msg}"
            dt = datetime.fromisoformat(time.replace('Z', '+00:00'))
            timestamp = dt.timestamp()
            
            uniqueTime = time + uuid.uuid4()[:6]
            
            r.zadd(title, {uniqueTime: timestamp})
            
            # if folder 'title' contains a timestamp that is 'outdated', we should remove it.
            # (implement this one)
            curTime = time.time()
            cutoff = curTime - WINDOW_SIZE
            r.zremrangebyscore(title, 0, cutoff)
            
            curSize = r.zcard(title)
            
            if curSize > ERROR_MSG_FLAG: # the type of lvl is 'failure':
                slack.send_slack_alert_manual(title, curSize, curTime)
                # if the size of the 'title' folder is greater than some metric x, we should instantiate
                # the Slack-message-sending function. (do not implement this one yet)
                # pass
        
        except Exception as e:
            print(f"Worker encountered an error: {e}")
           
