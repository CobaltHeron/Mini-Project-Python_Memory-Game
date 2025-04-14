
#===================================================================================
                              #MEMORY GAME #
#===================================================================================
# # Descripción: Juego de memoria donde el objetivo es encontrar pares de cartas idénticas.
# Tablero: Mostrar un tablero con cartas ocultas que el jugador debe descubrir de dos en
# dos.
# ● Pares: Si las cartas coinciden, se quedan reveladas; si no, se ocultan nuevamente.
# ● Puntuación: Añadir un contador de intentos y mostrar el puntaje al final

#=================================================================================

# Importar las librerías necesarias
import streamlit as st
import random
import time
import os
from datetime import datetime

# Configuración del juego
BOARD_SIZE = 4
TOTAL_CARDS = BOARD_SIZE * BOARD_SIZE
PAIRS = TOTAL_CARDS // 2
INITIAL_SCORE = 0
POINTS_PER_PAIR = 100
TIME_BONUS_MULTIPLIER = 2  # Multiplicador del bonus por tiempo
ATTEMPT_PENALTY = 5        # Puntos perdidos por intento fallido

# Añade esto al inicio con las demás constantes
RANKING_FILE = "ranking.txt"

# Lista de emojis 
EMOJIS = ['🐶', '🐱', '🐸', '🐙', '🐥', '🦄', '🐢', '🐬']  

#Estilo de Página#
st.markdown(
 """
    <style>
        /* Fondo blanco */
        .stApp {

            background-color:    #1b4f72       ;  /* Color de fondo */; 
             
        }

        /* Título y subtítulos */
        h1, h2, h3 {
            color: #000000 ;  /* Texto blanco */
            font-size: 36px;  /* Tamaño de fuente grande */
            font-weight: bold;
            text-align: center;
        }


        p {
            color:      #b03a2e  ;  /* Texto rojo granate */
            font-size: 40px;  /* Tamaño de fuente grande */
            font-weight: bold;
            text-align: center;
            
        }

        /* Cartas y botón reinicio */
        .stButton>button {
            display: block;
            margin: 0 auto;           /* Centra el botón horizontalmente */
            background-color:  #FFFFFF; /* Color de fondo inicial */
            border-radius: 14px;      /* Bordes redondeados */
            color: white;             /* Color del texto */
            padding: 10px 20px;       /* Espaciado interno */
            font-size: 20px;          /* Tamaño de la fuente */
            border: solid line;             /* Sin borde */
            cursor: transition;         /* Aparece como cursor de puntero */
            
        
        }

        /* Estilo cuando el mouse pasa por encima (hover) */
        .stButton>button[title="🔄 Reiniciar juego"]:hover {
            background-color: #34495E; /* Color de fondo cuando el ratón pasa por encima */
            transform: scale(1.1);      /* Aumenta ligeramente el tamaño del botón *
        }

        .victory-message {
            font-size: 24px;
            color: #27AE60;
            text-align: center;
            font-weight: bold;
            margin: 20px 0;
            line-height: 1.6;
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            border: 2px solid #27AE60;
        }

        .score-display {
            font-size: 20px;
            color: #F1C40F;
            text-align: center;
            font-weight: bold;
            margin: 10px 0;
            display: inline-block;
            padding: 8px 15px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
        }

    </style>
    """,
    unsafe_allow_html=True
)

# Título y subtítulos con markdown
st.markdown("<h1 style='text-align: center; color: #FFFFFF;'>Memory Game</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #ea641d ;'>¡Encuentra las parejas!</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #FFFFFF; font-size: 38px; margin-bottom: 40px;'>🐶 🐱 🐸 🐙 🐥 🦄 🐢 🐬</h3>", unsafe_allow_html=True)

# Función para guardar los resultados (añade esto después de las importaciones)
def save_game_result(player_name, score, attempts, game_time):
    # Crear el archivo si no existe
    if not os.path.exists(RANKING_FILE):
        with open(RANKING_FILE, "w") as f:
            f.write("Fecha|Nombre|Puntuación|Intentos|Tiempo(s)\n")
    
    # Guardar los datos
    with open(RANKING_FILE, "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}|{player_name}|{score}|{attempts}|{game_time}\n")

# Función para mostrar el ranking (opcional)
def show_ranking():
    if os.path.exists(RANKING_FILE):
        with open(RANKING_FILE, "r") as f:
            lines = f.readlines()[1:]  # Saltar la cabecera
            if lines:
                st.subheader("🏆 Ranking de Jugadores")
                st.markdown("""
                <style>
                .ranking-table {
                    width: 100%;
                    border-collapse: collapse;
                }
                .ranking-table th {
                   /* background-color: #2C3E50; */
                    color: white;
                    padding: 10px;
                    text-align: center;
                }
                .ranking-table td {
                    padding: 8px;
                    text-align: center;
                    border-bottom: 1px solid #ddd;
                }
                .ranking-table tr:nth-child(even) {
                    background-color: #f2f2f2;
                }
                            
                # .ranking-table tr:hover {
                #     background-color: #D5F5E3;
                }
                </style>
                """, unsafe_allow_html=True)
                
                # Mostrar top 10
                lines.sort(key=lambda x: -int(x.split("|")[2]))  # Ordenar por puntuación
                st.markdown("<table class='ranking-table'><tr><th>Posición</th><th>Nombre</th><th>Puntos</th><th>Intentos</th><th>Tiempo</th><th>Fecha</th></tr>", unsafe_allow_html=True)
                
                for i, line in enumerate(lines[:10], 1):
                    parts = line.strip().split("|")
                    st.markdown(f"""
                    <tr>
                        <td>{i}</td>
                        <td>{parts[1]}</td>
                        <td>{parts[2]}</td>
                        <td>{parts[3]}</td>
                        <td>{parts[4]}s</td>
                        <td>{parts[0]}</td>
                    </tr>
                    """, unsafe_allow_html=True)
                
                st.markdown("</table>", unsafe_allow_html=True)
            else:
                st.info("Aún no hay partidas registradas en el ranking")

# En la sección de inicialización del juego (donde está st.session_state)
if "board" not in st.session_state:
    chosen_emojis = random.sample(EMOJIS, PAIRS)
    emoji_pairs = chosen_emojis * 2
    random.shuffle(emoji_pairs)
    st.session_state.board = emoji_pairs
    st.session_state.revealed = [False] * TOTAL_CARDS
    st.session_state.matched = [False] * TOTAL_CARDS
    st.session_state.selected = []
    st.session_state.attempts = 0
    st.session_state.score = INITIAL_SCORE
    st.session_state.game_over = False
    st.session_state.start_time = time.time()  # Registrar tiempo de inicio
    st.session_state.last_pair_time = None     # Tiempo del último par encontrado

else:   
    # st.markdown("<p class='instructions' style= 'color: white; font-size: 24px'>Selecciona dos cartas y encuentra las parejas</p>", unsafe_allow_html=True)
    
    # Añade este marcador en la interfaz (junto al contador de intentos)
    st.markdown(f"""
    <div style="display: flex; justify-content: center; gap: 50px; margin-bottom: 20px;">
        <div class='attempts-counter'>⏱️ Tiempo: {int(time.time() - st.session_state.get('start_time', time.time()))}s</div>
        <div class='attempts-counter'>💯 Puntos: {st.session_state.score}</div>
        <div class='attempts-counter'>🔢 Intentos: {st.session_state.attempts}</div>
    </div>
    """, unsafe_allow_html=True)

# Mostrar tablero
cols = st.columns(BOARD_SIZE)
# Verificar si debemos bloquear nuevas selecciones (cuando hay 2 cartas reveladas)
lock_selection = len(st.session_state.selected) == 2

for i in range(TOTAL_CARDS):
    col = cols[i % BOARD_SIZE]
    with col:
        if st.session_state.matched[i]:
            st.button(st.session_state.board[i], key=f"btn_{i}", disabled=True)
        elif st.session_state.revealed[i] or i in st.session_state.selected:
            st.button(st.session_state.board[i], key=f"btn_{i}", disabled=True)
        else:
            # Deshabilitar el botón si ya hay 2 cartas seleccionadas
            if st.button("❓", key=f"btn_{i}", disabled=lock_selection):
                st.session_state.selected.append(i)
                st.session_state.revealed[i] = True
                st.rerun()

# Modifica la lógica cuando se encuentra un par (en la sección de comprobación de pares)
if len(st.session_state.selected) == 2:
    i1, i2 = st.session_state.selected
    if st.session_state.board[i1] == st.session_state.board[i2]:
        # Calcular puntos por tiempo (más rápido = más puntos)
        current_time = time.time()
        time_bonus = 0
        
        if st.session_state.last_pair_time:
            time_since_last = current_time - st.session_state.last_pair_time
            time_bonus = max(50 - int(time_since_last), 10) * TIME_BONUS_MULTIPLIER
        
        # Sumar puntos
        st.session_state.score += POINTS_PER_PAIR + time_bonus
        st.session_state.last_pair_time = current_time
        
        st.session_state.matched[i1] = True
        st.session_state.matched[i2] = True
    else:
        # Penalización por intento fallido
        st.session_state.score = max(0, st.session_state.score - ATTEMPT_PENALTY)
        time.sleep(1)
        st.session_state.revealed[i1] = False
        st.session_state.revealed[i2] = False
    
    st.session_state.attempts += 1
    st.session_state.selected = []
    st.rerun()

# Modifica el mensaje de victoria para pedir el nombre y guardar los datos
if all(st.session_state.matched):
    total_time = int(time.time() - st.session_state.start_time)
    time_bonus = max(300 - total_time, 0)
    st.session_state.score += time_bonus
    st.session_state.game_over = True
    
    with st.form("game_results"):
        st.markdown(f"""
        <div class='victory-message'>
            🎉 ¡Ganaste en {st.session_state.attempts} intentos!<br>
            ⏱️ Tiempo total: {total_time}s<br>
            💯 Puntuación final: {st.session_state.score}<br>
            ⭐ Bonus por tiempo: +{time_bonus}
        </div>
        """, unsafe_allow_html=True)
        
        player_name = st.text_input("Ingresa tu nombre para el ranking:", max_chars=20)
        
        if st.form_submit_button("Guardar mi resultado"):
            if player_name.strip():
                save_game_result(player_name, st.session_state.score, st.session_state.attempts, total_time)
                st.success("¡Resultado guardado en el ranking!")
                st.balloons()
                time.sleep(2)
                st.rerun()
            else:
                st.warning("Por favor ingresa un nombre válido")
    
    # Mostrar el ranking después del formulario
    show_ranking()

# Botón para reiniciar
if st.button("🔄 Reiniciar juego"):
    # Eliminar cada clave de session_state
    st.session_state.clear()

    # Reiniciar el estado y componentes del juego
    chosen_emojis = random.sample(EMOJIS, PAIRS)
    emoji_pairs = chosen_emojis * 2
    random.shuffle(emoji_pairs)
    st.session_state.board = emoji_pairs
    st.session_state.revealed = [False] * TOTAL_CARDS
    st.session_state.matched = [False] * TOTAL_CARDS
    st.session_state.selected = []
    st.session_state.attempts = 0
    st.session_state.score = INITIAL_SCORE
    st.session_state.game_over = False
    st.session_state.start_time = time.time()  # Registrar tiempo de inicio
    st.session_state.last_pair_time = None     # Tiempo del último par encontrado
    st.rerun()