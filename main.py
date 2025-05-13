from task_manager import TaskManager

# Crear una instancia del administrador de tareas
tm = TaskManager()

# Limpiar tareas anteriores (opcional durante pruebas)
tm.tasks = []
tm.save_tasks()

# Agregar tareas
tm.add_task(name="Estudiar lógica", priority=2)
tm.add_task(name="Terminar simulador N-body", priority=1)
tm.add_task(name="Revisar álgebra", priority=3)

# Agregar una tarea con dependencia
tm.add_task(name="Entregar informe final", priority=5, dependencies=["Terminar simulador N-body"])

# Mostrar tareas pendientes
print("📋 Tareas pendientes:")
for priority, task in tm.show_pending_tasks():
    print(f"- {task['name']} (Prioridad: {priority})")

# Obtener la siguiente tarea sugerida
next_task = tm.get_next_task()
if next_task:
    print("\n Próxima tarea sugerida:", next_task['name'])

# Completar una tarea
tm.complete_task("Terminar simulador N-body")

# Intentar completar una tarea con dependencia no satisfecha
try:
    tm.complete_task("Entregar informe final")
except ValueError as e:
    print(" Error al completar tarea:", e)

# Completar la dependencia y volver a intentar
tm.complete_task("Entregar informe final")

# Estado final
print(" Estado final de tareas pendientes:")
for priority, task in tm.show_pending_tasks():
    print(f"- {task['name']} (Prioridad: {priority})")
