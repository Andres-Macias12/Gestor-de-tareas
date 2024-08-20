from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

class Tarea:
    def __init__(self, titulo, descripcion, estado='Pendiente'):
        self.titulo = titulo
        self.descripcion = descripcion
        self.estado = estado

    def __str__(self):
        return f"{self.titulo} - {self.estado}: {self.descripcion}"

tareas = [
    Tarea("Comprar víveres", "Comprar frutas y verduras", "Pendiente"),
    Tarea("Lavar el coche", "Lavar el coche en el garage", "Completada"),
]

@app.route('/')
def index():
    return render_template('index.html', tareas=tareas)

@app.route('/agregar', methods=['POST'])
def agregar_tarea():
    try:
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        nueva_tarea = Tarea(titulo, descripcion)
        tareas.append(nueva_tarea)
        return redirect(url_for('index'))
    except ValueError:
        return "Error: Título y descripción son requeridos."

@app.route('/buscar', methods=['POST'])
def buscar_tarea():
    titulo = request.form['titulo']
    resultado = [tarea for tarea in tareas if tarea.titulo.lower() == titulo.lower()]
    return render_template('index.html', tareas=resultado)

@app.route('/actualizar', methods=['POST'])
def actualizar_tarea():
    try:
        titulo = request.form['titulo']
        nuevo_estado = request.form['estado']
        for tarea in tareas:
            if tarea.titulo.lower() == titulo.lower():
                tarea.estado = nuevo_estado
                return redirect(url_for('index'))
        return "Tarea no encontrada."
    except ValueError:
        return "Error: Estado debe ser 'Pendiente' o 'Completada'."

@app.route('/eliminar', methods=['POST'])
def eliminar_tarea():
    titulo = request.form['titulo']
    global tareas
    tareas = [tarea for tarea in tareas if tarea.titulo.lower() != titulo.lower()]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
