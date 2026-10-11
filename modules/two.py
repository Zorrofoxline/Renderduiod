# Guardar en: modules/two.py

def procesar_lectura_roblox(metodo, argumentos, json_body, sid_guardado, estado_pines_actual):
    """
    Valida las credenciales universales de Build Logic de forma segura.
    """
    # Si por alguna razón el disco está vacío, prevenir la caída
    if not sid_guardado or sid_guardado == "por_defecto":
        return {"error": "Servidor vacío. Configura tu SID en el panel web primero."}, 400

    # Extraer el SID según el canal de transmisión elegido
    sid_roblox = None
    if metodo == 'GET':
        sid_roblox = argumentos.get('sid')
    elif metodo == 'POST':
        if json_body:
            sid_roblox = json_body.get('sid')

    # Validar contraseña
    if not sid_roblox or sid_roblox != sid_guardado:
        print(f"[ACCESO RECHAZADO] Canal {metodo}. SID incorrecto.")
        return {"error": "SID no coincide o no autorizado"}, 401

    # Respuesta exitosa para los pines Data Out
    print(f"[CONEXIÓN EXITOSA {metodo}] Transmitiendo pines: {estado_pines_actual}")
    return {
        "success": True,
        "data": estado_pines_actual
    }, 200
