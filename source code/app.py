from flask import Flask, render_template, request, jsonify
import heapq
from datetime import datetime

app = Flask(__name__)

# In-memory priority queue for tasks
tasks = []
task_history = []

# Task counter for unique IDs
task_counter = 1

# Task class to store task details and its priority
class Task:
    def __init__(self, task_id, name, date, start_time, end_time, priority):
        self.id = task_id
        self.name = name
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.priority = priority  # Lower number means higher priority (earlier start time)
    
    def __lt__(self, other):
        return self.priority < other.priority

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET', 'POST'])
def tasks_route():
    global task_counter
    if request.method == 'GET':
        return jsonify([task.__dict__ for task in tasks])
    
    if request.method == 'POST':
        data = request.json
        task = Task(
            task_counter, data['taskName'], data['taskDate'], data['startTime'], data['endTime'], task_counter
        )
        heapq.heappush(tasks, task)
        task_counter += 1
        return jsonify(task.__dict__)

@app.route('/tasks/<int:task_id>', methods=['GET', 'DELETE'])
def task_details(task_id):
    global tasks, task_history
    task = None
    for t in tasks:
        if t.id == task_id:
            task = t
            break

    if not task:
        return jsonify({'message': 'Task not found'}), 404
    
    if request.method == 'GET':
        task_history.append(task)
        tasks.remove(task)
        return jsonify({'message': 'Task completed', 'task': task.__dict__})

    if request.method == 'DELETE':
        tasks = [t for t in tasks if t.id != task_id]
        task_history = [t for t in task_history if t.id != task_id]  
        return jsonify({'message': 'Task deleted'})

if __name__ == '__main__':
    app.run(debug=True)

