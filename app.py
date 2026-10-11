from flask import Flask, render_template, request, jsonify
from modules import two
import json
import os

app = Flask(__name__)
DATABASE_FILE = "datos.json"

def guardar_en_disco(sid, pines):
    with open(DATABASE_FILE, "w") as f:
        json.dump({"sid": sid, "data": pines}, f)

def leer_de_disco():
    if not os.path.exists(DATABASE_FILE):
        pines_defecto = [0,0,0,0,0,0,0,0]
        guardar_en_disco("por_defecto", pines_defecto)
        return "por_defecto", pines_defecto
    try:
        with open(DATABASE_FILE, "r") as f:
            contenido = json.load(f)
            return contenido.get("sid", "por_defecto"), contenido.get("data",)
    except:
        return "por_defecto",

# --- PÁGINA 1: INTERFAZ WEB ---
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/actualizar-pines', methods=['POST'])
def actualizar_pines():
    payload = request.get_json(force=True, silent=True)
    if not payload or "sid" not in payload or "data" not in payload:
        return jsonify({"success": False, "error": "Datos invalidos"}), 400
    
    guardar_en_disco(payload.get("sid"), payload.get("data"))
    return jsonify({
        "success": True, 
        "message": "¡Alerta! Configuracion transmitida al servidor con exito"
    }), 200

# --- PÁGINA 2: RECEPCIÓN COMPATIBLE CON URLENCODED ---
@app.route('/leer-transmisor', methods=['GET', 'POST'])
def leer_transmisor():
    metodo = request.method
    argumentos = request.args
    cabeceras = request.headers
    
    # Capturar datos de formulario si el juego usa x-www-form-urlencoded
    formulario = request.form if request.form else None
    
    sid_web, pines_actuales = leer_de_disco()
    
    # Delegar procesamiento seguro pasando los datos del formulario
    respuesta, codigo_estado = two.procesar_lectura_roblox(
        metodo, argumentos, formulario, cabeceras, sid_web, pines_actuales
    )
    
    return jsonify(respuesta), codigo_estado

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
