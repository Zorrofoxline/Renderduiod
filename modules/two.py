# Guardar en: modules/two.py

def procesar_lectura_roblox(metodo, argumentos, json_body, sid_guardado, estado_pines_actual):
    """
    Procesador Universal GET y POST para leer los pines desde el juego.
    """
    # 1. Verificar si ya hay configuración en el servidor
    if not sid_guardado:
        return {"error": "Servidor vacio. Configura el panel web primero."}, 400

    # 2. Extraer el SID dependiendo del método HTTP utilizado
    sid_roblox = None
    if metodo == 'GET':
        sid_roblox = argumentos.get('sid') # Lee de la URL (?sid=...)
    elif metodo == 'POST':
        if json_body:
            sid_roblox = json_body.get('sid') # Lee del JSON interno

    # 3. Validar coincidencia del SID de seguridad
    if not sid_roblox or sid_roblox != sid_guardado:
        print(f"[ALERTA DE SEGURIDAD] Acceso denegado via {metodo}. SID incorrecto.")
        return {"error": "SID no coincide o no autorizado"}, 401

    # 4. Enviar respuesta exitosa compatible con el HTTP Transmitter
    print(f"[ROBLOX {metodo}] Pines entregados con éxito: {estado_pines_actual}")
    return {
        "success": True,
        "data": estado_pines_actual
    }, 200
