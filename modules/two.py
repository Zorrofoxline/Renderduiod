def procesar_lectura_roblox(metodo, argumentos, formulario, cabeceras, sid_guardado, estado_pines_actual):
    """
    Procesador Universal compatible con application/x-www-form-urlencoded
    """
    if not sid_guardado or sid_guardado == "por_defecto":
        return {"error": "Servidor vacio. Configura el panel web primero."}, 400

    # 1. Buscar el SID en el formulario urlencoded, cabeceras o URL
    sid_roblox = None
    if formulario:
        sid_roblox = formulario.get('sid') # Lee si viene como campo de formulario
    
    if not sid_roblox:
        sid_roblox = cabeceras.get('sid') # Lee si viene como Header
        
    if not sid_roblox and metodo == 'GET':
        sid_roblox = argumentos.get('sid') # Lee si viene en la URL (?sid=...)

    # 2. Validar credenciales de seguridad (Asegurando manejo de strings planos)
    if not sid_roblox or str(sid_roblox).strip() != str(sid_guardado).strip():
        print(f"[ACCESO RECHAZADO 401] Recibido: '{sid_roblox}' | Esperado: '{sid_guardado}'")
        return {"error": "SID no coincide o acceso no autorizado"}, 401

    # 3. Retornar la estructura limpia requerida para el juego
    print(f"[CONEXION EXITOSA] Enviando los 8 bits: {estado_pines_actual}")
    return {
        "success": True,
        "sid": str(sid_guardado),
        "data": estado_pines_actual
    }, 200
