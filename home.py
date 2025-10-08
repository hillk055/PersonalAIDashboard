import streamlit as st
import time
from Helper_files.styling import get_css
from Helper_files.getresponse import TextResponder
from actionhandle import ToDoListHandler

st.set_page_config(page_title="Keegan's Dashboard", page_icon="📊", layout="wide")

# Load CSS from styling.py
st.markdown(get_css(), unsafe_allow_html=True)

st.title("📊 Keegan's Command Center")
st.markdown("Personal dashboard for **food tracking**, **budgeting**, and **daily insights.**")

# --- Session State ---
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "response_shown" not in st.session_state:
    st.session_state.response_shown = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

chat_container = st.container()

# --- Input ---
user_input = st.text_input("AI chat", placeholder="Type here to chat with AI")

if user_input:
    st.session_state.chat_history.append({"sender": "User", "text": f"You: {user_input}"})
    st.session_state.chat_history.append({"sender": "AI", "text": "AI: Sure, got it!"})

    with chat_container:
        for msg in st.session_state.chat_history:
            print(msg)
            if msg["sender"] == "User":
                st.markdown(
                    f"""
                    <div style="display:flex; justify-content:flex-end; margin-bottom:10px;">
                        <div style="
                            background-color:#0078FF;
                            color:white;
                            padding:10px 14px;
                            border-radius:10px;
                            max-width:70%;
                            word-wrap:break-word;">
                            {msg['text']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:  # AI messages with fade-in
                st.markdown(
                    f"""
                    <style>
                    @keyframes fadeIn {{
                        from {{opacity: 0; transform: translateY(10px);}}
                        to {{opacity: 1; transform: translateY(0);}}
                    }}
                    .fade-in {{
                        animation: fadeIn 0.5s ease forwards;
                    }}
                    </style>
                    <div style="display:flex; justify-content:flex-start; margin-bottom:10px;">
                        <div class="fade-in" style="
                            background-color:#2b2b2b;
                            color:white;
                            padding:10px 14px;
                            border-radius:10px;
                            max-width:70%;
                            word-wrap:break-word;">
                            {msg['text']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

if st.session_state.response_shown:

    handler = ToDoListHandler()
    agent = TextResponder()

    function, args, message = agent.get_response(user_input)
    print(*args)
    method = getattr(handler, function)
    method(*args)
    handler.save_input()

    st.markdown(f'<p class="fade-in">{message})</p>', unsafe_allow_html=True)
    time.sleep(1.5)
    st.session_state.response_shown = False

# ---------------------------
# Dashboard Cards
# ---------------------------
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Budget Tracker")
    st.write("View spending trends and update your weekly grocery budget.")
    if st.button("Open Budget"):
        st.session_state.page = "budget"
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🧾 Receipt Uploader")
    st.write("Upload receipts and automatically extract item prices.")
    if st.button("Open Receipt Uploader"):
        st.session_state.page = "receipt"
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🥑 Inventory & Expiry")
    st.write("Track what’s in your fridge and when it goes off.")
    if st.button("Open Inventory"):
        st.session_state.page = "inventory"
    st.markdown("</div>", unsafe_allow_html=True)

# Second row
col4, col5, col6 = st.columns(3, gap="large")

with col4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💳 Subscriptions")
    st.write("Monitor monthly subscriptions and renewal dates.")
    if st.button("Open Subscriptions"):
        st.session_state.page = "subscriptions"
    st.markdown("</div>", unsafe_allow_html=True)

with col5:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📬 Important Emails")
    st.write("Automatically sort and display key messages or offers.")
    if st.button("Open Emails"):
        st.session_state.page = "emails"
    st.markdown("</div>", unsafe_allow_html=True)

with col6:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🗒️ Daily Notes / Tasks")
    st.write("Write quick reminders or log today’s goals.")
    if st.button("Open Notes"):
        st.session_state.page = "notes"
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# PAGE ROUTING LOGIC
# ---------------------------
if "page" in st.session_state:
    page = st.session_state.page
    if page == "budget":
        st.switch_page("pages/budget.py")
    elif page == "receipt":
        st.switch_page("pages/Upload.py")
    elif page == "inventory":
        st.switch_page("pages/Inventory.py")
    elif page == "subscriptions":
        st.switch_page("pages/Subscriptions.py")
    elif page == "emails":
        st.switch_page("pages/Emails.py")
    elif page == "notes":
        st.switch_page("pages/Notes.py")
    if st.button("🏠 Back to Home"):
        st.switch_page("Home.py")
