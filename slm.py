import streamlit as st
import ollama
import time
import random

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(page_title="Shinchan Fun SLM AI", layout="wide")

# ============================================
# SESSION INIT
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "xp" not in st.session_state:
    st.session_state.xp = 0

# ============================================
# COLORFUL CSS (DARK + NEON STYLE)
# ============================================
st.markdown("""
<style>

body {
    background: linear-gradient(135deg,#1f1c2c,#928dab);
    color:white;
}

/* TITLE */
.title {
    text-align:center;
    font-size:48px;
    font-weight:bold;
    color:#00ffe0;
    text-shadow:2px 2px #ff00ff;
}

/* FLOATING EMOJIS */
@keyframes floatUp {
    0% { transform: translateY(0px); opacity:1; }
    50% { transform: translateY(-40px); opacity:0.6; }
    100% { transform: translateY(0px); opacity:1; }
}

.floating {
    position: fixed;
    font-size: 28px;
    animation: floatUp 4s infinite;
    pointer-events:none;
}

/* FEATURE CARDS */
.card {
    background: linear-gradient(135deg,#ff00cc,#3333ff);
    color:white;
    padding:18px;
    border-radius:18px;
    text-align:center;
    font-weight:bold;
    font-size:18px;
    box-shadow:0 6px 15px rgba(0,0,0,0.4);
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#141e30,#243b55);
    color:white;
}

/* CHAT USER */
div[data-testid="stChatMessage"][data-user="true"] > div {
    background-color:#00c6ff !important;
    color:black !important;
    border-radius:18px !important;
    font-weight:bold;
}

/* CHAT ASSISTANT */
div[data-testid="stChatMessage"][data-user="false"] > div {
    background-color:#ff0080 !important;
    color:white !important;
    border-radius:18px !important;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ============================================
# FLOATING EMOJIS
# ============================================
emoji_list = ["😂","🤪","🍭","🎉","🍕","🌈","⭐","😎","💥","🧸"]

for i in range(8):
    left = random.randint(5, 90)
    emoji = random.choice(emoji_list)
    st.markdown(
        f'<div class="floating" style="left:{left}vw;">{emoji}</div>',
        unsafe_allow_html=True
    )

# ============================================
# TITLE
# ============================================
st.markdown('<div class="title">🎭 Shinchan Ultimate Fun AI 🤪</div>', unsafe_allow_html=True)
st.write("💬 Offline Small Language Model using Ollama + Gemma")

# ============================================
# SIDEBAR
# ============================================
st.sidebar.title("⚙️ Fun Settings")

temperature = st.sidebar.slider(
    "🔥 Mischief Level",
    0.0, 1.2, 0.5, 0.1
)

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.session_state.xp = 0
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.progress(st.session_state.xp % 100)
st.sidebar.write(f"⭐ XP: {st.session_state.xp}")
st.sidebar.write(f"🎖 Level: {st.session_state.xp // 100}")

# ============================================
# SYSTEM PROMPT
# ============================================
SYSTEM_PROMPT = """
You are Shinchan.
Be funny, dramatic, playful.
Never say you are AI.
Reply in user's language.
Keep responses short and entertaining.
Use expressions like hehe~, hmmm~, ehehe~, ohhh~
"""

def build_messages():
    return [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages

# ============================================
# FEATURE PANELS (NOW COLORFUL)
# ============================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">😂 Funny Mode</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">💬 Smart Chat</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">🎉 XP Rewards</div>', unsafe_allow_html=True)

st.markdown("---")

# ============================================
# CHAT HISTORY
# ============================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ============================================
# USER INPUT
# ============================================
user_input = st.chat_input("Talk to Shinchan... hehe~ 🤪")

if user_input:

    st.session_state.xp += 10
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("💭 Shinchan thinking... hehe~")
        time.sleep(0.8)

        try:
            response = ollama.chat(
                model="gemma3:latest",
                messages=build_messages(),
                options={"temperature": temperature}
            )
            reply = response["message"]["content"]
        except Exception as e:
            reply = f"⚠️ Model error: {e}"

        placeholder.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

    if any(word in reply.lower() for word in ["haha", "hehe", "lol"]):
        st.balloons()

    if any(word in reply.lower() for word in ["wow", "cool", "amazing"]):
        st.snow()