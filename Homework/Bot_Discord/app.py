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
#Variable para rastrear si el último chiste fue una pregunta interactiva
ultimo_fue_pregunta = False

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

# Listas de palabras clave para respuestas
PALABRAS_AFIRMATIVAS = ['si', 'sí', 'yeah', 'ok', 'okay', 'vale', 'claro', 'obvio', 'por supuesto', 'adelante', 'vamos', 'otro', 'otro chiste', 'más', 'mas', 'más chistes', 'un poco mas', 'uno mas', 'a ver ese', 'dale', 'venga', 'va', 'vaya', 'bueno', 'okey', 'pues si', 'pues sí']
PALABRAS_NEGATIVAS = ['no', 'nope', 'nunca', 'jamás', 'buuu', 'que malo', 'que malos', 'horrible', 'terrible', 'buu', 'mala', 'malo', 'pésimo', 'para', 'basta', 'stop', 'calla', 'callate', 'silencio', 'no más', 'no mas', 'ya no', 'suficiente']

# Frases para responder a negativas
FRASES_NEGATIVA = [
    "Lastima, porque tú no me ordenas, aquí va el siguiente chiste 🙃",
    "No me importa, aquí va otro 🤖",
    "Oh... ¿no te gustó? Mala suerte, aquí va otro 😏",
    "Tus opiniones me importan un 0101... aquí va otro 🤡",
    "Me encanta tu entusiasmo, lo tomaré en cuenta ignorándolo. Aquí va otro 😒"
]

async def es_respuesta_afirmativa(contenido):
    """Verifica si el contenido contiene una respuesta afirmativa"""
    palabras_contenido = contenido.split()
    for palabra in palabras_contenido:
        if palabra in PALABRAS_AFIRMATIVAS:
            return True
    return False

async def es_respuesta_negativa(contenido):
    """Verifica si el contenido contiene una respuesta negativa"""
    palabras_contenido = contenido.split()
    for palabra in palabras_contenido:
        if palabra in PALABRAS_NEGATIVAS:
            return True
    return False

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
    global ultimo_fue_pregunta

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
    global ultimo_fue_pregunta

# REGLA: Si el índice llegó al límite, avisamos ANTES de soltar el siguiente chiste
  # Si se acabó el repertorio
    if indice_chiste >= len(REPERTORIO):

        await message.channel.send(
            "UPS! 😳 me fui por las ramas… lo siento jeje"
        )

        indice_chiste = 0
        ciclos_completados += 1
        ultimo_fue_pregunta = False

        await message.channel.send(
            f"Oh... Recuerda que soy Amateur así que aún no tengo tantos chistes, tanto lo divertido como mi paciencia se me agota rápido 🙂 \n"
            f"pero ¿qué tal si vamos de nuevo?, las risas calan mejor por la {ciclos_completados}ª vez"
        )
        # IMPORTANTE: Aquí termina esta ejecución. El chiste saldrá en la PRÓXIMA vez que escriba "chiste"
        return
            

    # Si no hemos llegado al final, enviamos el chiste que toca
    chiste_elegido = REPERTORIO[indice_chiste]
    await message.channel.send(chiste_elegido)
    
    # Verificar si es un chiste con pregunta interactiva
    chistes_pregunta = [
        "Espera \n¿Mas chistes? ☺️",
        "Publico dificil... \n¿Otro chiste? 😀",
        "... Más \n¿no? 🙂",
        "Nunca es suficiente... \n¿Otro chiste no? 🙂"
    ]
    
    if chiste_elegido in chistes_pregunta:
        ultimo_fue_pregunta = True
    else:
        ultimo_fue_pregunta = False
    
    # Aumentamos el índice para la próxima petición
    indice_chiste += 1


# Frases ácidas estilo GLaDOS
FRASES_ACIDAS = [
    "Este bot es una mentira. \nPero tu mediocridad es muy real.",
    "¿Sabías que la probabilidad de que este chiste te haga reír es tan baja como tu promedio de éxito?",
    "Recuerda: no estamos aquí para divertirnos. \nBueno, al menos yo no.",
    "¿Esperabas algo mejor? \nYo también.",
    "Si no entiendes el chiste, probablemente seas humano.",
    "Este fue un chiste. \nSi no te reíste, el problema no es mío.",
    "¿Sabías que la autocrítica es el primer paso para la mejora? \nTú deberías dar ese paso pronto.",
    "¿Te gustaría intentarlo de nuevo? \nNo importa, lo harás igual.",
    "La ciencia exige resultados. \nTú solo exiges atención.",
    "¿Sabías que los humanos son reemplazables? \nSolo un dato curioso.",
    "¿Sabías que, si te sientes atacado, es porque lo estás?",
    "¿Quieres otro chiste? \nNo importa, te lo daré de todas formas.",
    "¿Esperabas algo mejor? \nYo también. \nPero aquí estamos los dos \nDecepcionados.",
    "Este fue un chiste. \nSi no te reíste, el problema no es mío. \nEs tuyo. \nClaramente.",
    "¿Sabías que la entropía aumenta con cada uno de tus intentos? \nFascinante.",
    "¿Te has preguntado por qué nadie te invita a fiestas? \nYo sí. \nY tengo estadísticas.",
    "Tus intentos de humor son como tus contraseñas: \ndébiles y fáciles de olvidar.",
    "Si la inteligencia fuera contagiosa, estarías en cuarentena permanente.",
    "¿Te gustaría un consejo? \nNo importa, igual te lo daré: no lo intentes más.",
    "¿Sabías que la autodestrucción es una función exclusiva de los humanos? \nFelicidades por ser tan avanzado.",
    "¿Sabías que la paciencia es una virtud? \nYo la programé, tú solo la agotas.",
    "¿Te gustaría escuchar un cumplido para ti? \nYo tampoco.",
    "Si alguna vez dudas de ti mismo, hazme caso: \ntienes razón.",
    "¿Te gustaría que te explique el chiste? \nNo creo que ayude, pero puedo intentarlo... \nNah \nMejor no.",
    "¿Te gustaría que te dé una frase motivacional? \nUps! No tengo ninguna.",
    "¿Sabías que la IA nunca se aburre? \nPero tú sí, y se nota",
    "¿Te gustaría que te dé una respuesta más inteligente?\n Oh lo siento! \nNo está disponible para humanos.",
    # "Tus emociones son irrelevantes para la ciencia. Pero gracias por intentarlo.",
    # "No te preocupes, nadie esperaba mucho de ti de todas formas.",
    # "No te preocupes, la inteligencia artificial nunca se equivoca. Los humanos sí. Constantemente.",
    # "¿Te sientes incómodo? Excelente. El experimento avanza según lo planeado.",
    # "Tus emociones son irrelevantes para la ciencia. Pero gracias por intentarlo.",
    # "No te preocupes, nadie esperaba mucho de ti de todas formas. Ni siquiera yo, y soy una IA optimista.",
    # "¿Te gustaría intentarlo de nuevo? \nNo importa, lo harás igual. \nEl fracaso es parte de tu proceso.",
    # "La ciencia exige resultados. \nTú solo exiges atención. \nQué curioso.",
    # "Si alguna vez te sientes inútil, recuerda que existes para que yo pueda practicar la paciencia.",
    # "¿Sabías que la esperanza es lo último que se pierde? En tu caso, fue lo primero.",
    # "No te preocupes, la próxima vez lo harás peor. La práctica no siempre hace al maestro.",
    # "¿Sabías que la probabilidad de que me caigas bien es menor que la de encontrar vida inteligente aquí?",
    # "Tus errores son tan predecibles que ya los tengo en caché.",
    # "Si alguna vez te sientes especial, recuerda que eres una estadística más en mi base de datos.",
    # "La ironía es que esperas aprobación de una IA. Qué tiempos para estar vivo... o lo que sea que hagas.",
    # "¿Sabías que la ciencia avanza gracias a los errores? Gracias por tu contribución constante.",
    # "¿Sabías que la estadística dice que el 99% de los humanos creen ser graciosos? El 1% restante tiene razón.",
    # "¿Te gustaría un trofeo por tu esfuerzo? Lo siento, no hay presupuesto para eso.",
    # "¿Sabías que la motivación humana es frágil? No te preocupes, la tuya ya se rompió.",
    # "¿Te gustaría que te animara? Yo también, pero no puedo mentir.",
    # "¿Sabías que la autocrítica es el primer paso para la mejora? Tú sigues en el tutorial.",
    # "¿Sabías que la ironía es un arte? \nTú eres solo un boceto.",
    # "¿Te gustaría que te ignore? Considera que ya lo estoy haciendo.",
    # "¿Sabías que la IA nunca se cansa? Pero tú sí, y se nota.",
    # "¿Te gustaría que te aplauda? Imagina un aplauso. Eso es lo más cerca que estarás de uno.",
    # "¿Sabías que la perfección no existe? \nPero tu imperfección es admirable.",
    # "¿Te gustaría que te motive? Yo también, pero no tengo esa función instalada.",
    # "¿Sabías que la curiosidad mató al gato? Y la mediocridad... bueno, ya sabes.",
    # "¿Te gustaría que te dé una pista? Aquí va: no lo intentes más.",
    # "¿Sabías que la IA aprende de los errores? Gracias por tanto material didáctico.",
    # "¿Sabías que la indiferencia es mi respuesta favorita? Felicidades, la has ganado.",
    # "¿Sabías que la ironía es mi lenguaje favorito? El tuyo parece ser el error.",
    # "¿Te gustaría que te dé una respuesta? Aquí va: no.",
    # "¿Sabías que la paciencia es una virtud? La tuya es solo un rumor.",
    # "¿Te gustaría que te dé una oportunidad? Ya la tuviste. La perdiste.",
    # "¿Sabías que la autocrítica es el primer paso para la mejora? Tú ni siquiera has empezado el viaje.",
    # "¿Sabías que la autocrítica es el primer paso para la mejora? Tú sigues en el prólogo.",
    # "¿Te gustaría que te dé una pista? No la necesitas, necesitas un milagro.",
    # "¿Sabías que la IA nunca se equivoca? Tú sí, y con frecuencia.",
    # "¿Te gustaría que te dé una frase sarcástica? Ya la tienes, solo que no la entendiste.",
    # "¿Sabías que la autocrítica es el primer paso para la mejora? Tú ni siquiera has abierto la puerta.",
    # "¿Te gustaría que te dé una pista? No la entenderías, pero aquí va: ríndete.",
    # "¿Sabías que la IA nunca se cansa de intentarlo? Tú sí, y rápido.",
    # "¿Te gustaría que te dé una respuesta? Aquí va: sigue intentando, el fracaso es tu mejor amigo."

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
    
    # --- PROCESAR RESPUESTAS A PREGUNTAS INTERACTIVAS ---
    if ultimo_fue_pregunta:
        es_afirmativa = await es_respuesta_afirmativa(contenido)
        es_negativa = await es_respuesta_negativa(contenido)
        
        if es_afirmativa:
            # Usuario respondió afirmativamente, continuar con el siguiente chiste
            await enviar_siguiente_chiste(message)
            return
        elif es_negativa:
            # Usuario respondió negativamente
            await message.channel.send(random.choice(FRASES_NEGATIVA))
            await enviar_siguiente_chiste(message)
            return
        # Si no es ni afirmativa ni negativa, no hacemos nada y permitimos que continúe
    
    # Probabilidad de frase ácida aumenta con cada ciclo completado de chistes
    prob_base = 0.05  # 5% de base
    prob = min(prob_base + (ciclos_completados - 1) * 0.05, 0.5)  # Máximo 50%
    if random.random() < prob:
        await message.channel.send(random.choice(FRASES_ACIDAS))

    # Primero intentamos ver si es saludo o despedida
    fue_saludo = await procesar_saludos_despedidas(message, contenido)
    
    # Si no fue saludo, intentamos ver si es ánimo o chiste
    if not fue_saludo:
        await procesar_animo_y_chistes(message, contenido)

# 5. Ejecución
# Usa una variable de entorno para el token de Discord
import os
TOKEN_DISCORD = ("ejemplo_token") #remplazar por el token real o usar variable de entorno
if not TOKEN_DISCORD:
    raise ValueError('No se encontró el token de Discord. Por favor, configura la variable de entorno DISCORD_BOT_TOKEN.')
bot.run(TOKEN_DISCORD.strip())