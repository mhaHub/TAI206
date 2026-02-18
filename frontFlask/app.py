from flask import Flask, render_template, redirect, request
import requests

app = Flask(__name__)

API_URL = "http://localhost:5000/v1/usuarios"

@app.route('/')
def inicio():
    response = requests.get(API_URL)
    if response.status_code == 200:
        datos = response.json()
        usuarios = datos['data']
    else:
        usuarios = []

    return render_template("index.html", usuarios=usuarios)

@app.route('/agregar', methods=["POST"])
def agregarUsuario():
    nuevo_usuario = {
        "id": int(request.form["id"]),
        "nombre": request.form["nombre"],
        "edad": int(request.form["edad"])
        
    }
    
    requests.post(API_URL, json=nuevo_usuario)
    return redirect('/')

@app.route('/eliminar/<int:id>')
def eliminarUsuario(id):
    requests.delete(f"{API_URL}/{id}")
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=5001)

