from collections import defaultdict
from datetime import datetime, timedelta

# Example logs data structure (IP, session_id, timestamp)
logs = [
    {"ip": "192.168.1.1", "session_id": "abc123", "timestamp": "2024-08-12T10:00:00Z"},
    {"ip": "192.168.1.2", "session_id": "abc123", "timestamp": "2024-08-12T10:05:00Z"},
    {"ip": "10.0.0.1", "session_id": "def456", "timestamp": "2024-08-12T10:10:00Z"},
    # Add more log entries here
]

def detect_session_sidejacking(logs):
    session_activity = defaultdict(list)
    
    # Parse logs and group by session_id
    for log in logs:
        session_id = log["session_id"]
        ip = log["ip"]
        timestamp = datetime.strptime(log["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        session_activity[session_id].append((ip, timestamp))
    
    suspicious_sessions = []
    
    for session_id, activities in session_activity.items():
        # Sort activities by timestamp
        activities.sort(key=lambda x: x[1])
        
        # Check for activity from multiple IP addresses
        ip_addresses = set()
        for ip, timestamp in activities:
            ip_addresses.add(ip)
            if len(ip_addresses) > 1:
                suspicious_sessions.append(session_id)
                break
        
        # Additional checks for unexpected token changes or behavior can be added here
    
    return suspicious_sessions

suspicious_sessions = detect_session_sidejacking(logs)
print("Suspicious sessions:", suspicious_sessions)
