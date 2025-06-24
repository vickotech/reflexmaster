import streamlit as st
import random
import time

st.set_page_config(page_title="ReflexMaster v2.1", layout="centered")
st.title("🎯 ReflexMaster v2.1 - Klik Target & Catat Skormu!")

# Inisialisasi leaderboard
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

# Input nama pemain
if "player_name" not in st.session_state:
    st.session_state.player_name = ""

if st.session_state.player_name == "":
    name_input = st.text_input("Masukkan Nama untuk Mulai Bermain:")
    if name_input.strip():
        st.session_state.player_name = name_input.strip()
        st.experimental_rerun()

# Inisialisasi game
def init_game():
    st.session_state.score = 0
    st.session_state.start_time = None
    st.session_state.game_over = False
    st.session_state.target_key = str(random.randint(0, 10000))

if "score" not in st.session_state:
    init_game()

# Fungsi mulai ulang
def start_game():
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.game_over = False
    st.session_state.target_key = str(random.randint(0, 10000))

# Tombol mulai
if st.button("Mulai Game" if not st.session_state.start_time else "Mulai Lagi"):
    start_game()

# Permainan berjalan
if st.session_state.start_time:
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 20 - elapsed)

    if remaining == 0 and not st.session_state.game_over:
        st.session_state.game_over = True
        st.session_state.leaderboard.append((st.session_state.player_name, st.session_state.score))
        st.session_state.leaderboard = sorted(st.session_state.leaderboard, key=lambda x: x[1], reverse=True)[:5]

    if not st.session_state.game_over:
        st.success(f"{st.session_state.player_name} | Waktu tersisa: {int(remaining)} detik | Skor: {st.session_state.score}")

        # Tampilkan tombol target acak
        rows, cols = 5, 5
        target_pos = divmod(random.randint(0, rows * cols - 1), cols)
        grid = [[None for _ in range(cols)] for _ in range(rows)]
        grid[target_pos[0]][target_pos[1]] = "🎯"

        for i in range(rows):
            col_objs = st.columns(cols)
            for j in range(cols):
                if grid[i][j]:
                    if col_objs[j].button(grid[i][j], key=f"target-{st.session_state.score}-{time.time()}"):
                        st.session_state.score += 1
                        st.experimental_rerun()
                else:
                    col_objs[j].write(" ")
    else:
        st.subheader(f"⏱️ Waktu Habis! Skor Akhir {st.session_state.player_name}: {st.session_state.score}")
        st.markdown("## 🏆 Papan Peringkat Top 5")
        for idx, (name, score) in enumerate(st.session_state.leaderboard, start=1):
            st.write(f"**{idx}. {name}** - {score} poin")
        if st.button("Main Lagi"):
            st.session_state.player_name = ""
            init_game()
            st.experimental_rerun()