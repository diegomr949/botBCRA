import tweepy
import schedule
import time
from datetime import datetime, timedelta
import requests

# Claves API de Twitter
api_key = '3yyJcDSnhUWS5RSFX0S3ACVss'
api_secret = 'WzaecI0DwzIwAiB83VCbVPsCDcL1whFxllpiNYJHD0IOwcNGs3'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAOFgtwEAAAAAk88AuVdooZJHnjY5v6oBaInL6w4%3DAnGWUbHhxD4khWWd1BOYCsI0YD39YzN6kgoZizb7DE3E1rysIq'
access_token = '1791474455996182528-w3O9U1tGIFcTvRYV8tSQvUlbDJDhTd'
access_token_secret = 'zJxHgJeFAZVzyPdKa2U03b9aUuUrXhrW8Vrt7EGMFXOzd'

# Función para formatear la fecha
def formatear_fecha(fecha):
    """
    Formatea una fecha en formato YYYY-MM-DD.

    Args:
        fecha (datetime): Objeto datetime de la fecha.

    Devuelve:
        - Fecha formateada como string (YYYY-MM-DD).
    """
    return fecha.strftime("%Y-%m-%d")

# Función para publicar un tweet con los datos de la variable
def publicar_tweet_variable(id_variable, descripcion, datos):
    """
    Publica un tweet con la información de una variable y sus datos.

    Args:
        id_variable (int): Identificador de la variable.
        descripcion (str): Descripción de la variable.
        datos (list): Lista de diccionarios con datos de la variable.
    """
    # Crea el tweet con la información formateada
    hashtag = "#BCRAData"  # Puedes modificar el hashtag por defecto
    tweet = f"{descripcion} ({id_variable})\n\n"
    for dato in datos:
        fecha = dato["fecha"]
        valor = dato["valor"]
        tweet += f"{fecha}: {valor}\n"
    tweet += f"#BCRA #EconomiaArgentina {hashtag}"

    # Autentifica en Twitter
    client = tweepy.Client(bearer_token=bearer_token, api_key=api_key, api_secret=api_secret, access_token=access_token, access_token_secret=access_token_secret)

    # Publica el tweet
    try:
        client.create_tweet(text=tweet)
        print(f"Tweet publicado: {tweet}")
    except tweepy.TweepyException as e:
        # Handle specific Tweepy exceptions
        error_code = e.api_code
        error_message = e.reason
        print(f"Error al publicar tweet: {error_code} - {error_message}")
    except Exception as e:
        # Catch any other unexpected exceptions
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

def obtener_datos_variable(id_variable, fecha_desde, fecha_hasta):
    """
    Obtiene datos de una variable específica en un rango de fechas.

    Args:
        id_variable (int): Identificador de la variable.
        fecha_desde (str): Fecha de inicio en formato YYYY-MM-DD.
        fecha_hasta (str): Fecha de fin en formato YYYY-MM-DD.

    Devuelve:
        - Lista de diccionarios con datos de la variable o None en caso de error.
    """
    url = f"https://api.bcra.gob.ar/{id_variable}/{fecha_desde}/{fecha_hasta}"  # Aquí deberías completar la URL base de la API
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            contenido = respuesta.json().get("results", [])
            return contenido
        else:
            print(f"Error al obtener datos de variable: {id_variable}, {respuesta.status_code}")
            return None
    except requests.exceptions.RequestException as error:
        print(f"Error de conexión: {error}")
        return None

# Función para twittear cada variable
def twittear_variables():
    hoy = datetime.now()
    fecha_desde = formatear_fecha(hoy - timedelta(days=1))
    fecha_hasta = formatear_fecha(hoy)
    
    for variable in variables:
        id_variable = variable["id"]
        descripcion = variable["descripcion"]
        datos = obtener_datos_variable(id_variable, fecha_desde, fecha_hasta)
        if datos:
            publicar_tweet_variable(id_variable, descripcion, datos)

# Llamada directa para twittear las variables cuando se ejecute el script
twittear_variables()

# Programar la tarea diaria
schedule.every().day.at("11:40").do(twittear_variables)

# Ejecutar el scheduler en un bucle con manejo de excepciones
while True:
    try:
        schedule.run_pending()
        time.sleep(60)
    except Exception as e:
        print(f"Error durante la ejecución del scheduler: {e}")
        # Podrías querer registrar el error o realizar otras acciones según sea necesario
        time.sleep(60)  # Espera antes de volver a intentar ejecutar el scheduler
