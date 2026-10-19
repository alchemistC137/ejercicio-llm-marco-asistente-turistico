import logging

# Configurar el sistema de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_weather(fecha: str) -> str:
    """..."""
    logger.info(f"Herramienta invocada: get_weather | Argumento recibido: fecha='{fecha}'")
    
    try:
        if not fecha or len(fecha.strip()) == 0:
            raise ValueError("La fecha no puede estar vacía.")
        
        fecha_lower = fecha.lower()
        if "mañana" in fecha_lower:
            resultado = "Mañana hará sol, con una temperatura máxima de 24°C."
        elif "hoy" in fecha_lower:
            resultado = "Hoy está nublado, con 18°C y posibilidad de lluvia ligera."
        else:
            resultado = f"Para la fecha '{fecha}': Cielo despejado y 22°C."
            
        logger.info(f"Herramienta exitosa: {resultado}")
        return resultado
            
    except Exception as e:
        logger.error(f"Error en get_weather: {str(e)}")
        return f"Error al obtener el tiempo: {str(e)}"