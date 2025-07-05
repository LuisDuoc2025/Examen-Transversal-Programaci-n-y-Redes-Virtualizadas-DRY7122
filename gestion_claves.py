from flask import Flask, request, render_template_string
import sqlite3
import hashlib
import os

# Configurar aplicación Flask
app = Flask(__name__)
PORT = 5800

# Crear base de datos si no existe
if not os.path.exists("usuarios.db"):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE usuarios (
            nombre TEXT,
            password_hash TEXT
        )
    """)
    conn.commit()
    conn.close()

# HTML muy simple embebido
template = """
<!doctype html>
<title>Login Examen DRY7122</title>
<h2>Ingreso de Usuario</h2>
<form method=post>
  Nombre: <input type=text name=nombre required><br><br>
  Contraseña: <input type=password name=clave required><br><br>
  <input type=submit value=Ingresar>
</form>
<p>{{ mensaje }}</p>
"""

# Usuarios válidos (integrantes)
usuarios_validos = ["Luis Contreras", "Miguel Gutierrez"]

# Página principal (login)
@app.route("/", methods=["GET", "POST"])
def login():
    mensaje = ""
    if request.method == "POST":
        nombre = request.form["nombre"]
        clave = request.form["clave"]
        hash_clave = hashlib.sha256(clave.encode()).hexdigest()

        if nombre in usuarios_validos:
            # Guardar en base de datos
            conn = sqlite3.connect("usuarios.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)", (nombre, hash_clave))
            conn.commit()
            conn.close()
            mensaje = "Usuario validado y contraseña almacenada (hash)"
        else:
            mensaje = "Usuario no autorizado"

    return render_template_string(template, mensaje=mensaje)

if __name__ == "__main__":
    app.run(port=PORT)
