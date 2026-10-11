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
        return None, [0, 0, 0, 0, 0, 0, 0, 0]
    try:
        with open(DATABASE_FILE, "r") as f:
            contenido = json.load(f)
            return contenido.get("sid"), contenido.get("data")
    except:
        return None, [0, 0, 0, 0, 0, 0, 0, 0]

# --- PÁGINA 1: PANEL WEB (VISTA) ---
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# --- TRANSMITIR DESDE LA WEB (POST con Alerta) ---
@app.route('/actualizar-pines', methods=['POST'])
def actualizar_pines():
    payload = request.get_json()
    if not payload or "sid" not in payload or "data" not in payload:
        return jsonify({"success": False, "error": "Datos inválidos"}), 400
    
    guardar_en_disco(payload.get("sid"), payload.get("data"))
    print(f"[WEB POST] Transmisión exitosa guardada en disco.")
    
    return jsonify({
        "success": True, 
        "message": "¡Alerta! Configuración transmitida al servidor con éxito"
    }), 200

# --- PÁGINA 2: LECTURA UNIVERSAL DESDE ROBLOX (GET y POST) ---
@app.route('/leer-transmisor', methods=['GET', 'POST'])
def leer_transmisor():
    # Extraer el método actual, argumentos de la URL y cuerpo JSON
    metodo = request.method
    argumentos = request.args
    json_body = request.get_json(silent=True)
    
    # Recuperar datos guardados
    sid_web, pines_actuales = leer_de_disco()
    
    # Procesar con el módulo 'two' universal
    respuesta, codigo_estado = two.procesar_lectura_roblox(
        metodo, argumentos, json_body, sid_web, pines_actuales
    )
    
    return jsonify(respuesta), codigo_estado

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
