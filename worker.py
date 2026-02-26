  
def worker_start(log_queue, manager_dict):
    
    while True:
        try:
            element = log_queue.get(block = True, timeout = 1)
            
            if element is None:
                break
            
            # {"level": "WARN", "msg": "Auth failure: invalid credentials for 'admin'", "time": "14:00:01:56", "user": "admin", "ip": "192.168.5.12"}
            # {"level": "WARN", "msg": "Auth failure: account locked for 'root'", "time": "14:00:02:42", "user": "root", "ip": "104.28.1.5"}
            # {"level": "ERROR", "msg": "Connection error: peer reset connection during handshake", "time": "14:00:03:71", "user": "unknown", "ip": "192.168.5.12"}
            # {"level": "WARN", "msg": "Auth failure: invalid credentials for 'admin'", "time": "14:00:04:33", "user": "admin", "ip": "192.168.5.12"}
            lvl, msg, time = element.get("level", ""), element.get("msg", ""), element.get("time", "")
            
            name = lvl + msg[:10]
            
            if name not in manager_dict:
                manager_dict[name] = SortedList()
                
            digits = time.split(":")
            
            for i in range(len(digits)):
                digits[i] = str(40 + int(digits[i]))
                
            digits = int("".join(digits))
            removals = []
            
            for t in manager_dict[name]:
                if (digits + (HR_PADDING if str(t[:2]) > time[:2] else 0)) - (t + (PADDING if str(t[:2]) != time[:2] else 0)) < 100:
                    break
                else:
                    removals.append(t)
            
            for r in removals:
                manager_dict[name].remove(r)
            
            manager_dict[name].add(digits)
            
            
        except queue.Empty:
            # No data in the last second? Just loop back and try again.
            continue
        except Exception as e:
            print(f"Worker encountered an error: {e}")
           