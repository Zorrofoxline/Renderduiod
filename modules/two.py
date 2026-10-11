# Guardar en: modules/two.py

def procesar_lectura_roblox(metodo, argumentos, json_body, sid_guardado, estado_pines_actual):
    """
    Procesador Universal GET y POST para leer los pines desde el juego.
    """
    # 1. Verificar si el servidor ya tiene datos guardados
    if not sid_guardado:
        return {"error": "Servidor vacio. Configura el panel web primero."}, 400

    # 2. Extraer el SID dinámicamente según el método usado por el HTTP Transmitter
    sid_roblox = None
    if metodo == 'GET':
        sid_roblox = argumentos.get('sid') # Consigue de la URL (?sid=...)
    elif metodo == 'POST':
        if json_body:
            sid_roblox = json_body.get('sid') # Consigue del JSON interno

    # 3. Validar contraseña (SID)
    if not sid_roblox or sid_roblox != sid_guardado:
        print(f"[ALERTA] Acceso denegado via {metodo}. El SID no coincide.")
        return {"error": "SID no coincide o no autorizado"}, 401

    # 4. Enviar los pines limpios al juego
    print(f"[ROBLOX {metodo}] Solicitud exitosa. Enviando pines: {estado_pines_actual}")
    return {
        "success": True,
        "data": estado_pines_actual
    }, 200
