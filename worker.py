from collections import deque
from datetime import datetime
import queue

def worker_start(log_queue, manager_dict):
    while True:
        try:
            element = log_queue.get(block = True, timeout = 1)
            
            if element is None:
                break

            # {
            #     "timestamp": "2026-02-26T16:22:51.482Z",
            #     "level": "ERROR",
            #     "service": "payment-gateway",
            #     "event": "timeout_detected",
            #     "duration_ms": 502,
            #     "on_call_engineer": "jdoe"
            # }
            
            lvl = element.get("level", "")
            msg = element.get("event", "")
            time = element.get("timestamp", "")

            title = lvl + msg
            curTime = datetime.fromisoformat(time.replace('Z', '+00:00'))

            tmp_deque = deque(manager_dict.get(title, []))

            while tmp_deque:
                diff = curTime - tmp_deque[0]

                if diff.total_seconds() > 100.0:
                    tmp_deque.popleft()
            
            tmp_deque.append(curTime)

            # serialization safety.
            manager_dict[title] = list(tmp_deque)

        except queue.Empty:
            continue
        except Exception as e:
            print(f"Worker encountered an error: {e}")
           