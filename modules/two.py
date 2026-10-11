def procesar_lectura_roblox(metodo, argumentos, json_body, cabeceras, sid_guardado, estado_pines_actual):
    """
    Procesador Universal que extrae el SID de las cabeceras HTTP de Roblox.
    """
    if not sid_guardado or sid_guardado == "por_defecto":
        return {"error": "Servidor vacio. Configura el panel web primero."}, 400

    # 1. INTENTO PRINCIPAL: Buscar el SID en las cabeceras (Headers) enviados por Roblox
    sid_roblox = cabeceras.get('sid')

    # 2. INTENTOS DE RESPALDO: Si no viene en los headers, buscar en URL o JSON
    if not sid_roblox:
        if metodo == 'GET':
            sid_roblox = argumentos.get('sid')
        elif metodo == 'POST' and json_body:
            sid_roblox = json_body.get('sid')

    # 3. Validar contraseña (SID)
    if not sid_roblox or str(sid_roblox).strip() != str(sid_guardado).strip():
        print(f"[ACCESO DENEGADO 401] SID Recibido: '{sid_roblox}' | SID Esperado: '{sid_guardado}'")
        return {"error": "SID no coincide o no autorizado"}, 401

    # 4. Éxito total: Enviar los 8 bits al HTTP Transmitter
    print(f"[CONEXION EXITOSA] Entregando pines via cabeceras HTTP: {estado_pines_actual}")
    return {
        "success": True,
        "data": estado_pines_actual
    }, 200
