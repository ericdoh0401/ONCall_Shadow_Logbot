from fastapi import FastAPI
import uvicorn
import redis
import time

app = FastAPI()

_wokers = []
_start_time = None
_redis_conf = None
_log_queue = None

def init(workers, start_time, redis_conf, log_queue):
  global _workers, _start_time, _redis_conf, _log_queue
  
  _workers = workers
  _start_time = start_time
  _redis_conf = redis_conf
  _log_queue = log_queue

@app.get("/health")
def health():
  r = redis.Redis(**_redis_conf)

  alive_workers = [w for w in _workers if w.is_alive()]
  queue_depth = r.llen(_log_queue)
  uptime = time.time() - _start_time

  return {
    "status" : "online",
    "worker_count" : len(alive_workers),
    "queue_depth" : int(queue_depth),
    "uptime" : f"{uptime:.2f}s"
  }

def start_health_server(workers, start_time, redis_conf, log_queue):
  init(workers, start_time, redis_conf, log_queue)
  uvicorn.run(app, host = "0.0.0.0", port = 8000)

