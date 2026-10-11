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
        pines_defecto = [0, 0, 0, 0, 0, 0, 0, 0]
        guardar_en_disco("por_defecto", pines_defecto)
        return "por_defecto", pines_defecto
    try:
        with open(DATABASE_FILE, "r") as f:
            contenido = json.load(f)
            return contenido.get("sid", "por_defecto"), contenido.get("data", [0,0,0,0,0,0,0,0])
    except:
        return "por_defecto", [0, 0, 0, 0, 0, 0, 0, 0]

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/actualizar-pines', methods=['POST'])
def actualizar_pines():
    # SOLUCIÓN 500: 'force=True' fuerza la conversión a JSON de manera segura
    payload = request.get_json(force=True, silent=True)
    if not payload or "sid" not in payload or "data" not in payload:
        return jsonify({"success": False, "error": "Datos inválidos o vacíos"}), 400
    
    guardar_en_disco(payload.get("sid"), payload.get("data"))
    print(f"[WEB POST] Transmisión exitosa asignada en base de datos.")
    
    return jsonify({
        "success": True, 
        "message": "¡Alerta! Configuración transmitida al servidor con éxito"
    }), 200

@app.route('/leer-transmisor', methods=['GET', 'POST'])
def leer_transmisor():
    metodo = request.method
    argumentos = request.args
    
    # SOLUCIÓN 500: Extracción forzada ultra-segura para Roblox
    json_body = None
    if metodo == 'POST':
        json_body = request.get_json(force=True, silent=True)
    
    sid_web, pines_actuales = leer_de_disco()
    
    respuesta, codigo_estado = two.procesar_lectura_roblox(
        metodo, argumentos, json_body, sid_web, pines_actuales
    )
    
    return jsonify(respuesta), codigo_estado

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
