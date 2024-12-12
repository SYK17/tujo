from flask import Flask, jsonify
from storage import Storage

app = Flask(__name__)

storage = Storage()

def calculate_stats(data):
    """
    Calculate task statistics from the provided data.
    """
    total_count = 0
    completed_count = 0
    pending_count = 0
    
    for date in data:
        tasks = data[date]
        total_count += len(tasks)
        for task in tasks:
            if task.startswith('x '):
                completed_count += 1
            else:
                pending_count += 1
                
    return {
        "total": total_count,
        "completed": completed_count,
        "pending": pending_count
    }

@app.route('/stats', methods=['GET'])
def get_stats():
    task_data = storage.load()
    print(f"{task_data}")
    return jsonify(calculate_stats(task_data))

if __name__ == "__main__":
    app.run(port=2002)
