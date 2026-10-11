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

# --- PÁGINA 1: PANEL WEB DE CONTROL ---
# Habilitamos explícitamente el método GET para abrir la interfaz visual
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Habilitamos explícitamente el método POST para guardar los botones
@app.route('/actualizar-pines', methods=['POST'])
def actualizar_pines():
    payload = request.get_json()
    if not payload or "sid" not in payload or "data" not in payload:
        return jsonify({"success": False, "error": "Datos inválidos"}), 400
    
    # Guardamos los datos de manera persistente en el archivo físico
    guardar_en_disco(payload.get("sid"), payload.get("data"))
    print(f"[WEB API] Pines actualizados desde la web correctamente via POST.")
    return jsonify({"success": True}), 200


# --- PÁGINA 2: ENDPOINT DE LECTURA DE ROBLOX ---
# El HTTP Transmitter siempre envía solicitudes de tipo POST
@app.route('/leer-transmisor', methods=['POST'])
def leer_transmisor():
    payload = request.get_json()
    
    # Recuperamos los datos del archivo en disco
    sid_guardado, pines_actuales = leer_de_disco()
    
    # Validamos usando la lógica del módulo 'two.py'
    respuesta, codigo_estado = two.procesar_lectura_roblox(payload, sid_guardado, pines_actuales)
    
    return jsonify(respuesta), codigo_estado

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
