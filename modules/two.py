def procesar_lectura_roblox(payload, sid_guardado, estado_pines_actual):
    """
    Valida el SID enviado desde el juego de Roblox y retorna los pines correspondientes.
    """
    # 1. Verificar si ya se configuró un SID en la interfaz web
    if not sid_guardado:
        return {"error": "Servidor no configurado. Entra a la web primero y define un SID."}, 400

    # 2. Validar que el HTTP Transmitter esté enviando el SID correcto
    if not payload or payload.get("sid") != sid_guardado:
        print(f"[ALERTA SEGURIDAD] Intento de lectura bloqueado. El SID no coincide.")
        return {"error": "No autorizado / El SID no coincide"}, 401

    # 3. Mostrar log de éxito en la consola de Render
    print(f"[ROBLOX API] Petición exitosa con SID '{sid_guardado}'. Enviando: {estado_pines_actual}")
    
    # 4. Responder con la estructura JSON que lee de forma nativa Build Logic!
    return {
        "success": True,
        "data": estado_pines_actual
    }, 200
  
