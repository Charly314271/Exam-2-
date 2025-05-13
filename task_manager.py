import heapq
import json
from datetime import datetime

class TaskManager:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self):
        try:
            with open(self.filename, 'r') as f:
                tasks_data = json.load(f)
                # Convertir listas en tuplas
                self.tasks = [(int(priority), task) for priority, task in tasks_data]
                heapq.heapify(self.tasks)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []
    
    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump([[priority, task] for priority, task in self.tasks], f)
    
    def add_task(self, name, priority, dependencies=[], due_date=None):
        if not name:
            raise ValueError("El nombre de la tarea no puede estar vacío")
        try:
            priority = int(priority)
        except ValueError:
            raise ValueError("La prioridad debe ser un número entero")

        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("El formato de fecha debe ser YYYY-MM-DD")
        
        for dep in dependencies:
            if not any(t['name'] == dep for _, t in self.tasks):
                raise ValueError(f"Dependencia no encontrada: {dep}")
        
        new_task = {
            'name': name,
            'priority': priority,
            'dependencies': dependencies,
            'completed': False,
            'due_date': due_date
        }
        
        heapq.heappush(self.tasks, (priority, new_task))
        self.save_tasks()
    
    def complete_task(self, task_name):
        for i, (priority, task) in enumerate(self.tasks):
            if task['name'] == task_name:
                for dep in task['dependencies']:
                    if not self.is_task_completed(dep):
                        raise ValueError(f"La tarea {dep} no está completada")
                task['completed'] = True
                heapq.heapify(self.tasks)
                self.save_tasks()
                return
        raise ValueError("Tarea no encontrada")
    
    def is_task_completed(self, task_name):
        for _, task in self.tasks:
            if task['name'] == task_name:
                return task['completed']
        return False
    
    def get_next_task(self):
        if not self.tasks:
            return None
        for priority, task in sorted(self.tasks, key=lambda x: x[0]):
            if not task['completed']:
                return task
        return None
    
    def show_pending_tasks(self):
        pending = [(priority, task) for priority, task in self.tasks if not task['completed']]
        return sorted(pending, key=lambda x: x[0])
