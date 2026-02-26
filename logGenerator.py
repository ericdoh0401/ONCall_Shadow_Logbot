# [2026-02-26 17:55:01.234] INFO  [auth-service] User login successful
# [2026-02-26 17:56:12.887] WARN  [inventory-manager] Low stock threshold reached for SKU-505
# [2026-02-26 17:57:45.001] ERROR [payment-gateway] Credit card processing failed
# [2026-02-26 17:58:20.552] DEBUG [email-worker] SMTP handshake completed
# [2026-02-26 18:00:05.110] FATAL [database-proxy] Connection pool exhausted

# timestamp, level, service name, message

import datetime
import random
import time

# Expanded Levels (Adding standard trace levels)
LVLS = ["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL", "CRITICAL"]

# Service Names (Common microservice architecture components)
SRVS = [
    "auth-api",          # Identity & Permissions
    "payment-processor", # Stripe/Bank integrations
    "inventory-db",      # Database layer
    "order-worker",      # Background task processor
    "frontend-gateway",  # Nginx/Load Balancer
    "email-notifier",    # Notification service
    "search-engine",     # Elasticsearch/Indexing
    "shipping-api"       # Third-party logistics tracking
]

# Messages (Categorized by severity for logic mapping)
MSGS = {
    "TRACE": ["Variable 'retry_count' incremented to 3",
        "Entering function: validate_checksum_v2()",
        "Memory address pointer set to 0x7ffee392",
        "Raw packet payload: 48 65 6c 6c 6f 20 57 6f 72 6c 64",
        "Iterating sequence: item 402 of 1000",
        "Hook registered: post_process_data"
    ],
    
    "INFO": ["User session initialized",
    "Cache hit for key: user_profile",
    "Health check heartbeat sent",
    "Outbound request to provider successful"],

    "DEBUG": ["User session initialized",
    "Cache hit for key: user_profile",
    "Health check heartbeat sent",
    "Outbound request to provider successful"],

    "WARN": ["API rate limit approaching (85%)",
    "Slow query detected: execution > 500ms",
    "Deprecated API version used by client",
    "Memory usage exceeding threshold (90%)"],

    "ERROR": ["Failed to validate JWT signature",
    "Connection reset by peer (upstream)",
    "Database migration failed: lock timeout",
    "Disk space critical: 0 bytes remaining",
    "Dependency 'payment-provider' is unreachable",
    "Illegal state exception: unexpected null value"],

    "FATAL": ["Failed to validate JWT signature",
    "Connection reset by peer (upstream)",
    "Database migration failed: lock timeout",
    "Disk space critical: 0 bytes remaining",
    "Dependency 'payment-provider' is unreachable",
    "Illegal state exception: unexpected null value"],

    "CRITICAL": ["Kernel panic: Unable to mount root filesystem",
        "Primary data center region (us-east-1) unreachable",
        "Global emergency shutdown initiated by watchdog",
        "Data integrity check failed: possible storage corruption",
        "Hardware failure: Disk array /dev/md0 degraded",
        "Total resource exhaustion: system unable to fork new processes"
    ]
}

def solve(n):
    with open("tmp.log", 'w') as f:

        for _ in range(n):
            date = datetime.datetime.now()
            level = LVLS[random.randint(0, 6)]
            service = SRVS[random.randint(0, 7)]
            message = random.randint(0, len(MSGS[level]) - 1)

            f.write("[{}] {} {} {}\n".format(date, level, service, MSGS[level][message]))

            r = random.uniform(0.0001, 0.001)

            time.sleep(r)


if __name__ == "__main__":
    lines = int(input("# of lines: "))

    solve(lines)