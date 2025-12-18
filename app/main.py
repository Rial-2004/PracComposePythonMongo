from flask import Flask, render_template_string, request, redirect, url_for
import pandas as pd
import db_manager
import graph_manager
import github_manager

app = Flask(__name__)
db_manager.init_db()

REPO_URL = "git@github.com:Rial-2004/DatosColegio.git"

BASE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Colegio Rial-2004</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f0f2f5; text-align: center; }
        .container { width: 80%; margin: 40px auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        .btn { display: inline-block; padding: 12px 24px; margin: 10px; background: #2c3e50; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; border: none; cursor: pointer; }
        .btn-success { background: #27ae60; }
        .btn-github { background: #24292e; }
        input { padding: 12px; margin: 10px; width: 300px; border: 1px solid #ddd; border-radius: 6px; }
        .status-msg { padding: 15px; margin: 20px; border-radius: 8px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        {{ body|safe }}
        <br><hr><br>
        <a href="/" class="btn">🏠 Volver al Panel Principal</a>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    contenido = """
        <h1>🏫 Gestión Escolar: Rial-2004</h1>
        <div style="margin-top:40px;">
            <a href="/grafos" class="btn">📊 B1: Ver Estadísticas</a>
            <a href="/nuevo-alumno" class="btn">📝 B2: Registrar Alumno</a>
            <a href="/github" class="btn btn-github">🐙 B3: Sincronizar GitHub</a>
        </div>
    """
    return render_template_string(BASE_HTML, body=contenido)

@app.route('/grafos')
def grafos():
    df = pd.DataFrame(db_manager.get_all_students())
    
    if df.empty:
        return render_template_string(BASE_HTML, body="<h1>No hay datos disponibles</h1>")

    # Generamos los 4 gráficos
    pie_chart = graph_manager.generate_pie_chart(df)
    bar_loc = graph_manager.generate_bar_chart(df)
    ranking_chart = graph_manager.generate_sorted_notes_chart(df) # Nuevo
    avg_chart = graph_manager.generate_average_locality_chart(df) # Nuevo
    
    contenido = f"""
        <h1>Estadísticas Académicas Completa</h1>
        <div style="display: flex; flex-wrap: wrap; justify-content: space-around;">
            <div style="width: 45%;">{pie_chart}</div>
            <div style="width: 45%;">{bar_loc}</div>
            <div style="width: 45%;">{ranking_chart}</div>
            <div style="width: 45%;">{avg_chart}</div>
        </div>
    """
    return render_template_string(BASE_HTML, body=contenido)

@app.route('/nuevo-alumno', methods=['GET', 'POST'])
def nuevo_alumno():
    if request.method == 'POST':
        db_manager.add_student(request.form['nombre'], request.form['localidad'], request.form['nota'])
        return redirect(url_for('index'))
    
    formulario = """
        <h1>Nuevo Alumno</h1>
        <form method="POST">
            <input type="text" name="nombre" placeholder="Nombre" required><br>
            <input type="text" name="localidad" placeholder="Localidad" required><br>
            <input type="number" name="nota" placeholder="Nota" min="0" max="10" required><br>
            <button type="submit" class="btn btn-success">Guardar</button>
        </form>
    """
    return render_template_string(BASE_HTML, body=formulario)

@app.route('/github', methods=['GET', 'POST'])
def github():
    mensaje = ""
    # Definimos el token de la práctica para mostrarlo en la interfaz
    TOKEN_PRACTICA = "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"
    
    if request.method == 'POST':
        token = request.form.get('token')
        path = "data/alumnos.json"
        accion = request.form.get('accion')

        if accion == "export":
            # Eliminados los comentarios que causaban error de sintaxis
            datos = db_manager.get_all_students()
            if github_manager.export_to_github(token, REPO_URL, path, datos):
                mensaje = '<div class="status-msg" style="background:#d4edda; color:#155724;">✅ Exportado correctamente a GitHub</div>'
            else:
                mensaje = '<div class="status-msg" style="background:#f8d7da; color:#721c24;">❌ Error de Token o Permisos</div>'
        
        elif accion == "import":
            nuevos_datos = github_manager.import_from_github(token, REPO_URL, path)
            if nuevos_datos:
                db_manager.get_db_collection().drop()
                db_manager.get_db_collection().insert_many(nuevos_datos)
                mensaje = f'<div class="status-msg" style="background:#d1ecf1; color:#0c5460;">✅ {len(nuevos_datos)} alumnos importados.</div>'
            else:
                mensaje = '<div class="status-msg" style="background:#fff3cd; color:#856404;">⚠️ No se encontró el archivo en el repositorio.</div>'

    view = f"""
        <h1>Sincronización GitHub</h1>
        <p>Repo: <code>{REPO_URL}</code></p>
        
        {mensaje}
        
        <form method="POST">
            <input type="password" name="token" placeholder="Pega aquí el GitHub Token" required><br>
            <div style="margin-top: 10px;">
                <button name="accion" value="export" class="btn btn-github">⬆️ Subir a GitHub</button>
                <button name="accion" value="import" class="btn btn-success">⬇️ Descargar de GitHub</button>
            </div>
        </form>

        <div style="margin-top: 30px; padding: 15px; border: 1px dashed #ccc; background: #fafafa; border-radius: 8px;">
            <p style="margin: 0; color: #666; font-size: 0.9em;">🔑 <strong>Token para la práctica:</strong></p>
            <code style="background: #eee; padding: 5px; display: block; margin-top: 10px; word-break: break-all;">{TOKEN_PRACTICA}</code>
            <small style="color: #999;">(Cópialo y pégalo en el campo de arriba)</small>
        </div>
    """
    return render_template_string(BASE_HTML, body=view)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)