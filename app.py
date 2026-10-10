from flask import Flask, render_template, request, jsonify
from modules import two

app = Flask(__name__)

# Memoria global del servidor para almacenar los estados actuales
sid_activo = None
pines_activos = [0, 0, 0, 0, 0, 0, 0, 0]  # Inicia con los 8 bits en 0

# --- PÁGINA 1: PANEL WEB DE CONTROL (HTML) ---
@app.route('/')
def home():
    return render_template('index.html')

# Acción interna de la Página 1 para inyectar y cambiar los pines en el servidor
@app.route('/actualizar-pines', methods=['POST'])
def actualizar_pines():
    global sid_activo, pines_activos
    payload = request.get_json()
    
    if not payload or "sid" not in payload or "data" not in payload:
        return jsonify({"success": False, "error": "Datos inválidos"}), 400
    
    sid_activo = payload.get("sid")
    pines_activos = payload.get("data")
    
    print(f"[WEB API] Pines actualizados desde la web con SID: {sid_activo}")
    return jsonify({"success": True}), 200


# --- PÁGINA 2: ENDPOINT DE LECTURA PARA EL HTTP TRANSMITTER ---
@app.route('/leer-transmisor', methods=['POST'])
def leer_transmisor():
    payload = request.get_json()
    
    # Delegamos la validación y respuesta al módulo 'two'
    respuesta, codigo_estado = two.procesar_lectura_roblox(payload, sid_activo, pines_activos)
    
    return jsonify(respuesta), codigo_estado

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
