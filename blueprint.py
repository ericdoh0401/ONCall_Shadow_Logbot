

# a simple prefixSum problem utilizing a binary search approach
# to find the city in O(log n) time for each query
from collections import deque
import bisect

def solve():
    N = int(input())

    mapping = [[] for _ in range(N + 1)]

    for _ in range(N - 1):
        x, y = [int(element) for element in input().split(" ")]
        mapping[x].append(y)
        mapping[y].append(x)

    guards = [int(element) for element in input().split(" ")]

    Q = int(input())
    printQ = [0 for _ in range(Q)]
    queries = [[] for _ in range(N + 1)]

    for i in range(Q):
        U, X = [int(element) for element in input().split(" ")]
        queries[U].append([X, i])

    for i in range(N+1):
        v = queries[i]
        v.sort(key = lambda x : -x[0])
        
    # maximum depth of recursion.

    def dfs(curNode, parent, prefixSum, path):
        for q, index in queries[curNode]:
            anchor = bisect.bisect_right(prefixSum, prefixSum[-1] - q)
            
            printQ[index] = path[anchor]
        
        for neigh in mapping[curNode]:
            if neigh != parent:
                prefixSum.append(prefixSum[-1] + guards[neigh - 1])
                path.append(neigh)
                
                dfs(neigh, curNode, prefixSum, path)
                
                prefixSum.pop()
                path.pop()

    # queue = deque([[1, -1, [guards[0]], [1]]])

    dfs(1, -1, [guards[0]], [1])
    
    for pQ in printQ:
        print(pQ)

if __name__ == "__main__":
    T = int(input())

    for _ in range(T):
        solve()



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
            
