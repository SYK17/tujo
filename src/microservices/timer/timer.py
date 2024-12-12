from flask import Flask, jsonify
from datetime import datetime, timedelta


app = Flask(__name__)

is_running = False
end_time = None

def calculate_remaining_time() -> tuple[int, int]:
    """
    Calculate the remaining time on the timer.
    """
    if not is_running or end_time is None:
        return 30, 0
        
    time_left = end_time - datetime.now()
    total_seconds = max(0, int(time_left.total_seconds()))
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    
    return minutes, seconds

def format_timer_response(minutes: int, seconds: int, status: str) -> dict:
    return {
        "status": status,
        "minutes": minutes,
        "seconds": seconds
    }

@app.route('/start', methods=['POST'])
def start_timer():
    """Start or resume the timer."""
    global is_running, end_time
    
    if not is_running:
        is_running = True
        end_time = datetime.now() + timedelta(minutes=30)
        return jsonify(format_timer_response(30, 0, "started"))
    
    # If already running, return current time
    minutes, seconds = calculate_remaining_time()
    return jsonify(format_timer_response(minutes, seconds, "running"))

@app.route('/stop', methods=['POST'])
def stop_timer():
    """Stop the timer and reset to initial state."""
    global is_running, end_time
    
    is_running = False
    end_time = None
    return jsonify(format_timer_response(30, 0, "stopped"))

@app.route('/time', methods=['GET'])
def get_time():
    """Get current timer status and remaining time."""
    minutes, seconds = calculate_remaining_time()
    status = "running" if is_running else "stopped"
    print({minutes}, {seconds}, {status})
    return jsonify(format_timer_response(minutes, seconds, status))

if __name__ == '__main__':
    app.run(port=2003)
