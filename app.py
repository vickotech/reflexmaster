import streamlit as st
import random
import time

st.set_page_config(page_title="ReflexMaster - Target Click", layout="centered")
st.title("🎯 ReflexMaster - Klik Target Sebanyak Mungkin!")

# Inisialisasi
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'target_position' not in st.session_state:
    st.session_state.target_position = (random.randint(0, 4), random.randint(0, 4))

# Fungsi reset game
def reset_game():
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.game_over = False
    st.session_state.target_position = (random.randint(0, 4), random.randint(0, 4))

# Mulai game
if st.button("Mulai Game" if st.session_state.start_time is None else "Mulai Lagi"):
    reset_game()

# Jalankan game selama 20 detik
if st.session_state.start_time:
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 20 - elapsed)

    if remaining == 0:
        st.session_state.game_over = True

    if not st.session_state.game_over:
        st.success(f"Waktu tersisa: {int(remaining)} detik | Skor: {st.session_state.score}")

        # Tampilkan grid tombol 5x5, hanya satu yang aktif
        for i in range(5):
            cols = st.columns(5)
            for j in range(5):
                if (i, j) == st.session_state.target_position:
                    if cols[j].button("🎯", key=f"{i}-{j}"):
                        st.session_state.score += 1
                        st.session_state.target_position = (random.randint(0, 4), random.randint(0, 4))
                else:
                    cols[j].empty()
    else:
        st.subheader(f"⏱️ Waktu Habis! Skor Akhir: {st.session_state.score}")