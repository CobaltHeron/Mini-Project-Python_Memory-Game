
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

# Configuración del juego
BOARD_SIZE = 4
TOTAL_CARDS = BOARD_SIZE * BOARD_SIZE
PAIRS = TOTAL_CARDS // 2

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
    </style>
    """,
    unsafe_allow_html=True
)

st.title(" Memory Game" )
st.subheader("¡Encuentra las parejas!")
st.subheader("🐶 🐱 🐸 🐙 🐥 🦄 🐢 🐬")

# Inicializa el estado del juego

if "board" not in st.session_state:
    chosen_emojis = random.sample(EMOJIS, PAIRS)
    emoji_pairs = chosen_emojis * 2
    random.shuffle(emoji_pairs)
    st.session_state.board = emoji_pairs
    st.session_state.revealed = [False] * TOTAL_CARDS
    st.session_state.matched = [False] * TOTAL_CARDS
    st.session_state.selected = []
    st.session_state.attempts = 0
    st.session_state.game_over = False

if st.session_state.game_over:
    st.warning("El juego ha terminado. ¡Reinicia para jugar de nuevo!")

else:   
    st.write(f"Intentos: {st.session_state.attempts}")
    st.write("Selecciona dos cartas para ver si son un par.")


# Mostrar tablero
cols = st.columns(BOARD_SIZE)
for i in range(TOTAL_CARDS):
    col = cols[i % BOARD_SIZE]
    with col:
        if st.session_state.revealed[i] or st.session_state.matched[i]:
            st.button(st.session_state.board[i], key=f"btn_{i}", disabled=True) # !!!
        else:
            if st.button("❓", key=f"btn_{i}"):
                st.session_state.revealed[i] = True # !!!
                st.session_state.selected.append(i)

# Lógica del juego
if len(st.session_state.selected) == 2:
    i1, i2 = st.session_state.selected
    if st.session_state.board[i1] == st.session_state.board[i2]:
        st.session_state.matched[i1] = True
        st.session_state.matched[i2] = True
    else:
        time.sleep(1)  # breve pausa visual
        st.session_state.revealed[i1] = False
        st.session_state.revealed[i2] = False
    st.session_state.attempts += 1
    st.session_state.selected = []

# Mensaje de victoria
if all(st.session_state.matched):
    st.session_state.game_over = True
    st.success(f"🎉 ¡Ganaste en {st.session_state.attempts} intentos!")

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
    st.session_state.game_over = False
    


