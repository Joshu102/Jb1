import streamlit as st
import plotly.graph_objects as go
import numpy as np
import collections

st.set_page_config(page_title="Hex Pro AI", layout="centered")

# --- GAME LOGIC ---
SIZE = 7

if 'board' not in st.session_state:
    st.session_state.board = np.zeros((SIZE, SIZE))
    st.session_state.turn = 1 # 1: Player, 2: AI
    st.session_state.msg = "YOUR TURN - CONNECT TOP TO BOTTOM (RED)"

def get_hex_coords(r, c):
    x = c * 1.75 + r * 0.875
    y = -r * 1.5
    return x, y

def check_win(board, p):
    q = collections.deque()
    vis = set()
    for i in range(SIZE):
        r, c = (0, i) if p == 1 else (i, 0)
        if board[r][c] == p:
            q.append((r, c)); vis.add((r, c))
    while q:
        r, c = q.popleft()
        if (p == 1 and r == SIZE-1) or (p == 2 and c == SIZE-1): return True
        for nr, nc in [(-1,0),(1,0),(0,-1),(0,1),(-1,1),(1,-1)]:
            if 0 <= nr < SIZE and 0 <= nc < SIZE and board[nr][nc] == p and (nr, nc) not in vis:
                vis.add((nr, nc)); q.append((nr, nc))
    return False

# --- UI & GRAPHICS ---
st.title("🏆 Hex Pro AI - Neon Edition")
st.write(f"### {st.session_state.msg}")

fig = go.Figure()

for r in range(SIZE):
    for c in range(SIZE):
        x, y = get_hex_coords(r, c)
        color = "#1f2937" # Gray
        if st.session_state.board[r][c] == 1: color = "#ff4b4b" # Neon Red
        if st.session_state.board[r][c] == 2: color = "#00d4ff" # Neon Blue
        
        # Hexagon Shape
        angles = np.linspace(0, 2*np.pi, 7)
        fig.add_trace(go.Scatter(
            x=x + np.cos(angles), y=y + np.sin(angles),
            fill="toself", mode='lines',
            fillcolor=color, line=dict(color="white", width=1),
            hoverinfo='text', text=f"Pos: {r},{c}",
            name=f"{r},{c}"
        ))

fig.update_layout(
    width=700, height=600, showlegend=False,
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
)

# Click handling (Streamlit special)
selected = st.selectbox("Select Hexagon to move (Row, Col):", 
                       [f"{r},{c}" for r in range(SIZE) for c in range(SIZE) if st.session_state.board[r,c] == 0])

if st.button("Confirm Move"):
    r, c = map(int, selected.split(","))
    st.session_state.board[r, c] = 1
    if check_win(st.session_state.board, 1):
        st.session_state.msg = "🏆 CHAMPION! YOU WON DUDE ! 🏆"
        st.balloons()
    else:
        # Simple AI Move
        empty = np.argwhere(st.session_state.board == 0)
        if len(empty) > 0:
            idx = np.random.choice(len(empty))
            st.session_state.board[empty[idx][0], empty[idx][1]] = 2
            if check_win(st.session_state.board, 2):
                st.session_state.msg = "🤖 AI WON! BETTER LUCK NEXT TIME!"
    st.rerun()

st.plotly_chart(fig, use_container_width=True)