import tweepy
import schedule
import time
from datetime import datetime, timedelta
import requests
import time

# Claves API de Twitter
api_key = 'API_KEY'
api_secret = 'API_SECRET'
bearer_token = 'BEARER_TOKEN'
access_token = 'ACCESS_TOKEN'
access_token_secret = 'ACCESS_TOKEN_SECRET'

# Autentificación en Twitter
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)

# Función para formatear la fecha
def formatear_fecha(fecha):
    """
    Formatea una fecha en formato DD-MM-AAAA.

    Args:
        fecha (datetime): Objeto datetime de la fecha.

    Devuelve:
        str: Fecha formateada como string (DD-MM-AAAA).
    """
    return fecha.strftime("%Y-%m-%d")

# Función para obtener datos de una variable específica en un rango de fechas
def obtener_datos_variable(id_variable, fecha_desde, fecha_hasta):
    """
    Obtiene datos de una variable específica en un rango de fechas.

    Args:
        id_variable (int): Identificador de la variable.
        fecha_desde (str): Fecha de inicio en formato YYYY-MM-DD.
        fecha_hasta (str): Fecha de fin en formato YYYY-MM-DD.

    Devuelve:
        list: Lista de diccionarios con datos de la variable o None en caso de error.
    """
    url = f"https://api.bcra.gob.ar/estadisticas/v2.0/DatosVariable/{id_variable}/{fecha_desde}/{fecha_hasta}"
    try:
        respuesta = requests.get(url, verify=False)

        if respuesta.status_code == 200:
            contenido = respuesta.json().get("results", [])
            return contenido
        else:
            print(f"Error al obtener datos de variable: {id_variable}, {respuesta.status_code}")
            return None
    except requests.exceptions.RequestException as error:
        print(f"Error de conexión: {error}")
        return None
    
# Función para publicar un tweet con los datos de la variable
def publicar_tweet_variable(client, id_variable, descripcion, datos):
    """
    Publica un tweet con la información de una variable y sus datos.

    Args:
        client (tweepy.Client): Cliente de Tweepy.
        id_variable (int): Identificador de la variable.
        descripcion (str): Descripción de la variable.
        datos (list): Lista de diccionarios con datos de la variable.
    """
   # Crea el tweet con la información formateada
    hashtag = "#BCRAData"  # Puedes modificar el hashtag por defecto
    dato = datos[-1]  # Obtener solo el último dato de la lista
    fecha = datetime.strptime(dato["fecha"], "%Y-%m-%d").strftime("%d-%m-%Y")  # Modificado el formato de fecha
    valor = dato["valor"]
    tweet = f"{descripcion} al {fecha}\n{valor}\n\n"
    tweet += f"#BCRA #EconomiaArgentina {hashtag}"

    # Imprimir el tweet en la consola
    print(f"Tweet: {tweet}")

    # Publica el tweet
    try:
        client.create_tweet(text=tweet)
        print(f"Tweet publicado: {tweet}")
    except tweepy.errors.TooManyRequests as e:
        print("Demasiadas solicitudes. Esperando 15 minutos antes de intentar nuevamente...")
        time.sleep(15 * 60)  # Espera 15 minutos antes de intentar nuevamente
        publicar_tweet_variable(client, id_variable, descripcion, datos)  # Intenta publicar nuevamente
    except tweepy.TweepyException as e:
        # Manejar otras excepciones de Tweepy
        print(f"Error al publicar tweet: {e}")
    except Exception as e:
        # Capturar cualquier otra excepción inesperada
        print(f"Error general: {e}")


# Definir las variables con su ID y descripción
variables = [
    {"id": 1, "descripcion": "Reservas Internacionales del BCRA"},
    {"id": 4, "descripcion": "Tipo de Cambio Minorista ($ por USD) - Promedio vendedor"},
    {"id": 5, "descripcion": "Tipo de Cambio Mayorista ($ por USD) - Referencia"},
    {"id": 6, "descripcion": "Tasa de Política Monetaria (en % n.a.)"},
    {"id": 7, "descripcion": "BADLAR en pesos de bancos privados (en % n.a.)"},
    {"id": 8, "descripcion": "TM20 en pesos de bancos privados (en % n.a.)"},
    {"id": 9, "descripcion": "Tasas de interés de las operaciones de pase activas para el BCRA, a 1 día de plazo (en % n.a.)"},
    {"id": 10, "descripcion": "Tasas de interés de las operaciones de pase pasivas para el BCRA, a 1 día de plazo (en % n.a.)"},
    {"id": 11, "descripcion": "Tasas de interés por préstamos entre entidades financiera privadas (BAIBAR) (en % n.a.)"},
    {"id": 12, "descripcion": "Tasas de interés por depósitos a 30 días de plazo en entidades financieras (en % n.a.)"},
    {"id": 13, "descripcion": "Tasa de interés de préstamos por adelantos en cuenta corriente"},
    {"id": 14, "descripcion": "Tasa de interés de préstamos personales"},
    {"id": 15, "descripcion": "Base monetaria - Total (en millones de pesos)"},
    {"id": 16, "descripcion": "Circulación monetaria (en millones de pesos)"},
    {"id": 17, "descripcion": "Billetes y monedas en poder del público (en millones de pesos)"},
    {"id": 18, "descripcion": "Efectivo en entidades financieras (en millones de pesos)"},
    {"id": 19, "descripcion": "Depósitos de los bancos en cta. cte. en pesos en el BCRA (en millones de pesos)"},
    {"id": 21, "descripcion": "Depósitos en efectivo en las entidades financieras - Total (en millones de pesos)"},
    {"id": 22, "descripcion": "En cuentas corrientes (neto de utilización FUCO) (en millones de pesos)"},
    {"id": 23, "descripcion": "En Caja de ahorros (en millones de pesos)"},
    {"id": 24, "descripcion": "A plazo (incluye inversiones y excluye CEDROS) (en millones de pesos)"},
    {"id": 25, "descripcion": "M2 privado, promedio móvil de 30 días, variación interanual (en %)"},
    {"id": 26, "descripcion": "Préstamos de las entidades financieras al sector privado (en millones de pesos)"},
    {"id": 27, "descripcion": "Inflación mensual (variación en %)"},
    {"id": 28, "descripcion": "Inflación interanual (variación en % i.a.)"},
    {"id": 29, "descripcion": "Inflación esperada - REM próximos 12 meses - MEDIANA (variación en % i.a)"},
    {"id": 30, "descripcion": "CER (Base 2.2.2002=1)"},
    {"id": 31, "descripcion": "Unidad de Valor Adquisitivo (UVA) (en pesos -con dos decimales-, base 31.3.2016=14.05)"},
    {"id": 32, "descripcion": "Unidad de Vivienda (UVI) (en pesos -con dos decimales-, base 31.3.2016=14.05)"},
    {"id": 34, "descripcion": "Tasa de Política Monetaria (en % e.a.)"},
    {"id": 35, "descripcion": "BADLAR en pesos de bancos privados (en % e.a.)"},
    {"id": 40, "descripcion": "Índice para Contratos de Locación (ICL-Ley 27.551, con dos decimales, base 30.6.20=1)"},
    {"id": 41, "descripcion": "Tasas de interés de las operaciones de pase pasivas para el BCRA, a 1 día de plazo (en % e.a.)"},
    {"id": 42, "descripcion": "Pases pasivos para el BCRA - Saldos (en millones de pesos)"}
]

# Lista para realizar un seguimiento de las variables para las que ya se ha publicado un tweet
variables_publicadas = []

def twittear_variables():
    """
    Obtiene los datos de las variables y publica tweets para cada una.
    """
    hoy = datetime.now()
    fecha_desde = formatear_fecha(hoy - timedelta(days=7))  # Cambia la fecha de inicio según sea necesario
    fecha_hasta = formatear_fecha(hoy - timedelta(days=6))
    for variable in variables:
        id_variable = variable["id"]
        descripcion = variable["descripcion"]
        # Verificar si ya se ha publicado un tweet para esta variable
        if id_variable in variables_publicadas:
            continue  # Saltar esta variable y pasar a la siguiente
        datos = obtener_datos_variable(id_variable, fecha_desde, fecha_hasta)
        if datos:
            publicar_tweet_variable(client, id_variable, descripcion, datos)  # Pasar el cliente como primer argumento
            # Agregar esta variable a la lista de variables publicadas
            variables_publicadas.append(id_variable)

# Llamada directa para twittear las variables cuando se ejecute el script
twittear_variables()

# Programar la tarea diaria
#schedule.every().day.at("11:40").do(twittear_variables)

# Ejecutar el scheduler en un bucle con manejo de excepciones
while True:
    try:
        schedule.run_pending()
        time.sleep(60)
    except Exception as e:
        print(f"Error durante la ejecución del scheduler: {e}")
        # Podrías querer registrar el error o realizar otras acciones según sea necesario
        time.sleep(60)  # Espera antes de volver a intentar ejecutar el scheduler

