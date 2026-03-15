
# worker.py

from collections import deque
from datetime import datetime
from slack import send_slack_alert_manual
import queue
import redis
import time
import uuid
import json
import logging

WINDOW_SIZE = 100
ERROR_MSG_FLAG = 50
BOT_TOKEN = "X123456"
CHANNEL = "C123456"

logger = logging.getLogger(__name__)

def worker_start(redis_conf, log_queue):
    r = redis.Redis(**redis_conf)
    
    while True:
        try:
            _, raw_data = r.brpop(log_queue)
            decoded_data = raw_data.decode('utf-8')
            
            if decoded_data == "SHUTDOWN_SIGNAL":
                # terminate worker
                print("Worker has received a shutdown signal. Exiting...")
                break
            
            start_time = time.time()
            
            element = json.loads(decoded_data)
                
            lvl = element.get("level", "")
            msg = element.get("message", "")
            timestamp_str = element.get("timestamp", "")

            title = f"{lvl}: {msg}"
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            timestamp = dt.timestamp()
            
            uniqueTime = timestamp_str + " " + (str(uuid.uuid4()))[:6]
            
            r.zadd(title, {uniqueTime: timestamp})
            
            curTime = time.time()
            cutoff = curTime - WINDOW_SIZE
            r.zremrangebyscore(title, 0, cutoff)
            
            curSize = r.zcard(title)
            
            processing_time = time.time()
            
            logger.info(f"Processed | title='{title}' | queue_depth={curSize} | duration={processing_time:.4f}s")
            
            if curSize > ERROR_MSG_FLAG: # the type of lvl is 'failure':
                send_slack_alert_manual(title, curSize, curTime, BOT_TOKEN, CHANNEL)
        
        except Exception as e:
            logger.error(f"Failed to process message | error={e} | raw='{decoded_data}'")
           
