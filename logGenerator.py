import datetime
import random
import time
import numpy as np
import uuid

# Configuration remains similar but organized for logic mapping
LVLS = ["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL", "CRITICAL"]
SRVS = ["auth-api", "payment-processor", "inventory-db", "order-worker", "frontend-gateway"]

# Grouping messages by state for the Markov Chain
STATE_MSGS = {
    0: { # HEALTHY STATE (Mostly INFO/DEBUG)
        "levels": [0, 1, 2],
        "msgs": ["User session initialized", "Cache hit for key: user_profile", "Health check heartbeat sent"]
    },
    1: { # DEGRADED STATE (Mostly WARN)
        "levels": [3],
        "msgs": ["API rate limit approaching (85%)", "Slow query detected: execution > 500ms", "Retrying connection to upstream"]
    },
    2: { # FAILURE STATE (ERROR/FATAL/CRITICAL)
        "levels": [4, 5, 6],
        "msgs": ["Database migration failed: lock timeout", "Primary data center unreachable", "Connection pool exhausted"]
    }
}

def solve(n):
    # prevState: [Healthy, Degraded, Failure]
    state_vector = np.array([1, 0, 0])
    transition = np.array([
        [0.9, 0.07, 0.03], # Healthy: usually stays healthy
        [0.40, 0.50, 0.10], # Degraded: can recover or fail
        [0.015, 0.005, 0.98]  # Failure: tends to "stick" (the flood effect)
    ])

    current_correlation_id = None
    
    with open("markov_flow.log", 'w') as f:
        for _ in range(n):
            prob = random.uniform(0, 1)
            probs = np.matmul(state_vector, transition)
            
            if prob < probs[0]:
                state_idx = 0
                current_correlation_id = None
            elif prob < (probs[0] + probs[1]):
                state_idx = 1
            else:
                state_idx = 2 # Failure
                if not current_correlation_id:
                    current_correlation_id = str(uuid.uuid4())[:8]

            state_vector = np.zeros(3)
            state_vector[state_idx] = 1

            level_idx = random.choice(STATE_MSGS[state_idx]["levels"])
            level = LVLS[level_idx]
            message = random.choice(STATE_MSGS[state_idx]["msgs"])
            service = random.choice(SRVS)
            
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            tid_str = f" [{current_correlation_id}]" if current_correlation_id else ""
            
            f.write(f"[{date}] {level.ljust(8)} {service.ljust(18)}{tid_str} {message}\n")

            if state_idx == 2 and random.random() < 0.3:
                f.write(f"    at com.app.{service}.Core.execute(SourceFile.java:{random.randint(10, 500)})\n")

            time.sleep(random.uniform(0.0001, 0.005))

if __name__ == "__main__":
    lines = int(input("# of lines: "))
    solve(lines)