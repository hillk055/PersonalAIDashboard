import streamlit as st
import time
from Helper_files.styling import get_css, get_chat_box_styling
from Helper_files.getresponse import TextResponder, ChatResponder, command_or_chat
from actionhandle import ToDoListHandler

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# Load custom CSS
st.markdown(get_css(), unsafe_allow_html=True)

# --- Extra CSS for fade animation ---
st.markdown("""
<style>
.fade-container {
    transition: opacity 0.6s ease-in-out, max-height 0.6s ease-in-out;
    overflow: hidden;
}
.fade-hidden {
    opacity: 0;
    max-height: 0;
    pointer-events: none;
}
.fade-visible {
    opacity: 1;
    max-height: 500px; /* Adjust as needed */
}
.toggle-btn {
    background-color: #3b3b98;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.4em 1em;
    cursor: pointer;
    margin-bottom: 8px;
}
.toggle-btn:hover {
    background-color: #575fcf;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Dashboard Header
# ---------------------------
st.title("📊 Keegan's Command Center")
st.markdown("Personal dashboard for **food tracking**, **budgeting**, and **daily insights.**")

# ---------------------------
# Session State
# ---------------------------
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "response_shown" not in st.session_state:
    st.session_state.response_shown = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_expanded" not in st.session_state:
    st.session_state.chat_expanded = True  # default visible

# ---------------------------
# Chat Section with Toggle
# ---------------------------
toggle_label = "🔽 Hide Chat" if st.session_state.chat_expanded else "▶ Show Chat"
if st.button(toggle_label, key="toggle_chat", help="Show or hide the chat window"):
    st.session_state.chat_expanded = not st.session_state.chat_expanded

# Chat fade container
chat_state_class = "fade-visible" if st.session_state.chat_expanded else "fade-hidden"
st.markdown(f"<div class='fade-container {chat_state_class}'>", unsafe_allow_html=True)

if st.session_state.chat_expanded:
    user_input = st.text_input(label="AI chat", placeholder="Type here to chat with AI", label_visibility='collapsed')

    if user_input:

        pick = command_or_chat(user_input)
        if pick == 'general_chat':
            agent = ChatResponder()
            message = agent.get_response(user_input)
        elif pick == 'command':
            handler = ToDoListHandler()
            agent = TextResponder()
            function, *args, message = agent.get_response(user_input)
            method_call = getattr(handler, function)
            method_call()
        else:
            agent = None
            message = None

        st.session_state.chat_history.append({"sender": "User", "text": f"You: {user_input}"})
        st.session_state.chat_history.append({"sender": "AI", "text": message})

    # Display chat messages
    for msg in st.session_state.chat_history:
        get_chat_box_styling(msg)

st.markdown("</div>", unsafe_allow_html=True)

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
