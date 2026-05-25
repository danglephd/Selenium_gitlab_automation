from datetime import datetime

def write_log(message):
    """Helper function to write logs to file with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}\n"
    try:
        with open("collect-issue.log", "a", encoding="utf-8") as f:
            f.write(log_message)
    except Exception as e:
        print(f"Error writing to log file: {e}")