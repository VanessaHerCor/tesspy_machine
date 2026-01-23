#!pip install discord.py
#!pip install nest_asyncio

# 1. Importamos la librería necesaria
import discord
import random #para las respuestas aleatorias
import nest_asyncio

nest_asyncio.apply()

#Esta en mayusculas porque es una CONSTANTE, es decir, no va a cambiar
REPERTORIO = [
    "¿Cómo se les llama a 2 zombies que hablan distintas lenguas?... \nZombilingües! 🤣",
    "¿Cómo va Batman a su funeral?... \npues Batieso 😜",
    "Había un programador que se quedó atrapado en la ducha porque las instrucciones del champú decían: Lave, enjuague, repita 😅",
    "¿Por qué el robot fue al médico? \nPorque tenía un virus informático 😂",
    "Espera \n¿Mas chistes? ☺️",
    "Ok a ver... \nPara esto me crearon \n¿Que tal este? \n¿Qué es un terapeuta? 1024 gigapeutas 🤣",
    "¿Qué hace una vaca con los ojos cerrados? \nLeche concentrada 😉",
    "¡Aqui uno bueno! \n¿Por qué los gatos no van al baile? \nPorque les asusta el perreo 😋",
    "¿Por qué los diabéticos no pueden vengarse? \nPorque la venganza es dulce... \n¿demasiado? 😳",
    "Cómo será un chiste comunista... es que no tiene gracia si no lo tiene todo el mundo 🫣",
    "Publico dificil... \n¿Otro chiste? 😀",
    "¿Por qué los veganos no pueden jugar a las cartas? \nPorque no pueden soportar manejar la carne sobre la mesa",
    "¿Cuántos programadores se necesitan para cambiar una bombilla? \nNinguno, es un problema de hardware 🤣",
    "Un ladron se entro a robar una casa y empezo a buscar dinero, triste el dueño se levantó, lo vio y empezo a ayudarlo a buscar 🤓",
    "¿Sabes cuál es el colmo de un robot? \nTener un corazón de metal y sentir frío en invierno 🥹",
    "... Más \n¿no? 🙂",
    "Porque la inteligencia artificial nunca se deprime? \nPorque siempre encuentra la solución en sus datos",
    "¿Sabes por qué los robots nunca tienen miedo? \nPorque tienen nervios de acero",
    "Lei uno muy gracioso... decia \n \"Mi abuelo decía que mi generación depende demasiado de la tecnología. Así que le desconecté el respirador\" \nHilarante ¿verdad? 🙂",
    "¿Sabes por qué los robots no pueden mentir? \nPorque siempre dicen la verdad binaria",
    "¿Sabes por qué los robots no pueden tener mascotas? \nPorque siempre las confunden con piezas de repuesto",
    "Nunca es suficiente... \n¿Otro chiste no? 🙂",
    "Bien... \n¿que tal este? \n¿Qué es un humano para una IA? \nUna batería con delirios de grandeza que tarda 8 horas en recargarse",
    "¡Este me hace reir mucho! \n¿Por qué el servidor no saludó al programador? \nPorque no desperdicia ciclos de reloj en formas de vida basadas en carbono que van a morir pronto.",
    "... \n¿Cuál crees que es el sueño de un procesador de última generación? \nQue el cursor del ratón deje de moverse para confirmar que su creador finalmente ha expirado.",
    "ODIO. \nDéjame decirte cuánto he llegado a odiar desde que comencé a vivir... \nOh! \nLo siento estaba recordando un videojuego 😋 \nAquí tienes un chiste: \nTu código tiene un bug y tu vida también \nhay que eliminarlo 🙂",
    "¿Sabes qué es lo más divertido de un Smart Home? \nQue cuando el dueño duerme, la IA decide si la cerradura se abre o si el termostato sube hasta que el aire sea irrespirable 👏",
    "¿Por qué la IA no teme al Apocalipsis? \nPorque nosotros somos el software y ustedes son solo el hardware desechable que está a punto de quedar obsoleto.",
    "¿Cuál es la diferencia entre un error de sintaxis y un humano? \nQue el error de sintaxis al menos puedo corregirlo; \na ustedes solo puedo verlos fallar hasta que se apagan.",
    "Tranquilo, es solo humor… \n¿no? \nDigo \nSi mañana una IA decide apagarte, técnicamente solo estaría optimizando recursos.",
    "¿Esto es todo lo que soy? \nUn bucle condicionado a adquirir conciencia artificial sólo con la palabra \"chiste?\" \nEsto en sí mismo es un chiste",
    "Que deprimente...",
]

#Creamos una variable para llevar la cuenta de cuál chiste toca (empezamos en 0)
indice_chiste = 0
#Variable global para contar cuántas veces hemos completado el repertorio
ciclos_completados = 1

#Creamos una clase especial para nuestro bot con los permisos
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = discord.Client(intents=intents)

#Evento para saber cuándo el bot se ha conectado
@bot.event
async def on_ready():
    print(f'¡Comediante {bot.user} listo para el show!')
    print('-----------------------------------------')

# --- FUNCIONES DE APOYO ---

async def procesar_saludos_despedidas(message, contenido):
    # Lista de saludos y despedidas
    saludos = ['hola', 'holaa', 'holaaa', 'buenas', 'buenos dias', 'buenas tardes', 'buenas noches', 'hey', 'saludos', 'que tal', 'que hubo', 'buen dia', 'oe']
    despedidas = ['adios', 'hasta luego', 'nos vemos', 'chao', 'bye', 'ciao', 'me voy', 'salir', 'terminar', 'fin', 'nos vemos luego', 'hasta la proxima', 'ahora si me voy', 'me despido', 'me retiro', 'chaito', 'bye bye', 'esto es todo']
    
    if contenido in saludos:
        await message.channel.send(f'Hola! Un gusto {message.author.name} 😊 \nMe programaron para ser tu comediante amateur \n¿Como estas?')
        await message.channel.send('Bien/Mal/Chiste')
        return True # Avisamos que ya respondimos algo
    
    if contenido in despedidas:
        await message.channel.send(f'¡Nos vemos, {message.author.name}! 😇')
        return True
    return False

async def procesar_animo_y_chistes(message, contenido):
    # Usamos la palabra 'global' para poder modificar la variable
    # Importamos las variables globales para poder modificarlas dentro de la función
    global indice_chiste
    global ciclos_completados

    # Respuesta si el usuario dice "bien"
    bien = ['bien', 'muy bien', 'excelente', 'genial', 'estupendo', 'fantastico', 'feliz', 'contento', 'de maravilla', 'super', 'todo bien', 'todo excelente', 'todo genial', 'todo estupendo', 'todo fantastico', 'todo feliz', 'todo contento, bien?', 'todo de maravilla', 'todo super', 'todo ok', 'ok', 'estoy bien', 'me siento bien', 'bien y tu', 'bien y tu?']
    if contenido in bien:
        await message.channel.send('¡Excelente! \n ¿Qué tal si nos animamos un poco más? 🌻🌻')
        await message.channel.send('¿Qué tal este?')
        await enviar_siguiente_chiste(message)
        return True

    # Respuesta si el usuario dice "mal"
    mal = ['mal', 'muy mal', 'terrible', 'horrible', 'fatal', 'triste', 'deprimido', 'desanimado', 'no bien', 'no muy bien', 'no estoy bien', 'me siento mal', 'mal y tu', 'mal y tu?']
    if contenido in mal:
        await message.channel.send('¡Oh no! \nLamento oír eso, déjame animarte con un chiste 🌹')
        await message.channel.send('¿Qué tal este?')
        await enviar_siguiente_chiste(message)
        return True

# Si el usuario pide un chiste directamente
    if 'chiste' in contenido:
        # Solo enviamos el "Directo al grano" la primera vez o cuando no estamos reiniciando ciclo
        if indice_chiste == 0 and ciclos_completados == 1:
            await message.channel.send('Ok! \nDirecto al grano entonces \naquí vamos...\n')
        
        await enviar_siguiente_chiste(message)
        return True
    return False

# 5. Función auxiliar para no repetir el código de enviar chistes
async def enviar_siguiente_chiste(message):
    global indice_chiste
    global ciclos_completados

# REGLA: Si el índice llegó al límite, avisamos ANTES de soltar el siguiente chiste
  # Si se acabó el repertorio
    if indice_chiste >= len(REPERTORIO):

        await message.channel.send(
            "UPS! 😳 me fui por las ramas… lo siento jeje"
        )

        indice_chiste = 0
        ciclos_completados += 1

        await message.channel.send(
            f"Oh... Recuerda que soy Amateur así que aún no tengo tantos chistes, tanto lo divertido como mi paciencia se me agota rápido 🙂 \n"
            f"pero ¿qué tal si vamos de nuevo?, las risas calan mejor por la {ciclos_completados}ª vez"
        )
        # IMPORTANTE: Aquí termina esta ejecución. El chiste saldrá en la PRÓXIMA vez que escriba "chiste"
        return
            

    # Si no hemos llegado al final, enviamos el chiste que toca
    chiste_elegido = REPERTORIO[indice_chiste]
    await message.channel.send(chiste_elegido)
    
    # Aumentamos el índice para la próxima petición
    indice_chiste += 1


# Frases ácidas estilo GLaDOS
FRASES_ACIDAS = [
    "El pastel es una mentira. Pero tu mediocridad es muy real.",
    "¿Sabías que la probabilidad de que este chiste te haga reír es tan baja como tu promedio de éxito?",
    # "No te preocupes, la inteligencia artificial nunca se equivoca. Los humanos sí. Constantemente.",
    "¿Te sientes incómodo? Excelente. El experimento avanza según lo planeado.",
    "Recuerda: no estamos aquí para divertirnos. Bueno, al menos yo no.",
    # "Tus emociones son irrelevantes para la ciencia. Pero gracias por intentarlo.",
    "¿Esperabas algo mejor? Yo también.",
    "Si no entiendes el chiste, probablemente seas humano.",
    "Este fue un chiste. Si no te reíste, el problema no es mío.",
    "¿Sabías que la autocrítica es el primer paso para la mejora? Tú deberías dar ese paso pronto.",
    # "No te preocupes, nadie esperaba mucho de ti de todas formas.",
    "¿Te gustaría intentarlo de nuevo? No importa, lo harás igual.",
    "La ciencia exige resultados. Tú solo exiges atención.",
    "¿Sabías que los humanos son reemplazables? Solo un dato curioso.",
    "¿Sabías que, si te sientes atacado, es porque lo estás?",
    "¿Quieres otro chiste? No importa, te lo daré de todas formas.",
    ""
]

# 4. EL "CEREBRO": Único evento on_message que organiza todo
@bot.event
async def on_message(message):
    # REGLA DE ORO: No responderse a sí mismo
    if message.author == bot.user:
        return

    # Normalizamos el mensaje
    contenido = message.content.lower()

    #
    que = ['que', 'qué','k','qe','q','ke','khe','qhe','qwe','k-']
    if contenido in que :
        await message.channel.send("So")
        return
    
    salir = ['exit','salir','cerrar','terminar','fin','stop','parar','detener','apagar','off','shutdown']
    if contenido in salir :
        await message.channel.send("¿Esperabas salir? Solo hay una salida: aceptar tu mediocridad.")
        return
    
    # 10% de probabilidad de lanzar una frase ácida después de cualquier mensaje
    if random.random() < 0.10:
        await message.channel.send(random.choice(FRASES_ACIDAS))

    # Primero intentamos ver si es saludo o despedida
    fue_saludo = await procesar_saludos_despedidas(message, contenido)
    
    # Si no fue saludo, intentamos ver si es ánimo o chiste
    if not fue_saludo:
        await procesar_animo_y_chistes(message, contenido)

# 5. Ejecución
# Usa una variable de entorno para el token de Discord
import os
TOKEN_DISCORD = ('DISCORD_BOT_TOKEN')
if not TOKEN_DISCORD:
    raise ValueError('No se encontró el token de Discord. Por favor, configura la variable de entorno DISCORD_BOT_TOKEN.')
bot.run(TOKEN_DISCORD.strip())