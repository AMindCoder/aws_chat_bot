import streamlit as st
import requests
import re

# Page config
st.set_page_config(
    page_title="Corporate Data Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with Glassmorphism styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main container with animated gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main content area */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 80px;
        max-width: 900px;
        margin: 0 auto;
    }

    /* Chat message styling */
    .chat-message {
        padding: 1rem 1.25rem;
        border-radius: 18px;
        margin-bottom: 1rem;
        display: flex;
        gap: 0.875rem;
        animation: slideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        max-width: 85%;
        word-wrap: break-word;
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    .chat-message.user {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.5) 0%, rgba(139, 92, 246, 0.5) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.3);
        flex-direction: row-reverse;
        margin-left: auto;
        box-shadow: 0 4px 24px rgba(139, 92, 246, 0.2);
    }

    .chat-message.bot {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-right: auto;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
    }

    .chat-message .avatar {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        flex-shrink: 0;
    }

    .chat-message.user .avatar {
        background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.1) 100%);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .chat-message.bot .avatar {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .chat-message .content {
        color: #f1f5f9;
        line-height: 1.6;
        flex: 1;
        font-size: 0.95rem;
    }

    /* Header styling */
    .header-container {
        text-align: center;
        padding: 1.5rem 1rem;
        margin-bottom: 0.5rem;
    }

    .header-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        filter: drop-shadow(0 0 20px rgba(99, 102, 241, 0.5));
    }

    .header-title {
        color: #ffffff;
        font-size: 1.75rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
        background: linear-gradient(135deg, #f1f5f9 0%, #c4b5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .header-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        font-weight: 400;
    }

    /* Chat input styling - Fixed at bottom */
    .stChatInput {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1rem 1.5rem 1.5rem;
        background: linear-gradient(to top, rgba(15, 12, 41, 0.98) 0%, rgba(15, 12, 41, 0.9) 70%, transparent 100%);
        z-index: 1000;
    }

    .stChatInput > div {
        max-width: 900px;
        margin: 0 auto;
    }

    [data-testid="stChatInput"] {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
        padding: 0.5rem !important;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: rgba(139, 92, 246, 0.5) !important;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.15) !important;
    }

    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInputTextArea"],
    .stChatInput textarea,
    [data-testid="stChatInput"] [data-testid="stChatInputTextArea"] {
        background: transparent !important;
        color: #1e1e2e !important;
        font-size: 0.95rem !important;
        caret-color: #1e1e2e !important;
        -webkit-text-fill-color: #1e1e2e !important;
    }

    [data-testid="stChatInput"] textarea::placeholder,
    [data-testid="stChatInputTextArea"]::placeholder {
        color: #6b7280 !important;
        -webkit-text-fill-color: #6b7280 !important;
    }

    [data-testid="stChatInput"] button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        border: none !important;
        border-radius: 10px !important;
    }

    [data-testid="stChatInput"] button:hover {
        transform: scale(1.05) !important;
    }

    [data-testid="stChatInput"] button svg {
        fill: white !important;
    }

    /* Regular button styling */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
        white-space: nowrap !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(99, 102, 241, 0.5) !important;
    }

    /* Secondary button */
    .stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: none !important;
    }

    /* Welcome message */
    .welcome-container {
        text-align: center;
        padding: 2rem;
        color: #94a3b8;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        margin-bottom: 1.5rem;
    }

    .welcome-container h3 {
        color: #f1f5f9;
        margin-bottom: 0.5rem;
        font-weight: 600;
        font-size: 1.25rem;
    }

    .welcome-container p {
        margin: 0;
        font-size: 0.95rem;
    }

    /* URL badge */
    .url-badge {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(34, 197, 94, 0.1) 100%);
        border: 1px solid rgba(34, 197, 94, 0.3);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        color: #86efac;
        font-size: 0.85rem;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.98) !important;
        backdrop-filter: blur(20px) !important;
    }

    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }

    /* Input in sidebar */
    section[data-testid="stSidebar"] .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
    }

    /* Separator */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        margin: 1rem 0;
    }

    /* Clear chat button container */
    .clear-btn-container {
        display: flex;
        justify-content: center;
        margin-top: 1rem;
        margin-bottom: 100px;
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #8b5cf6 !important;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .chat-message {
            max-width: 95%;
            padding: 0.875rem 1rem;
        }

        .header-title {
            font-size: 1.5rem;
        }

        .header-icon {
            font-size: 2.5rem;
        }

        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .stChatInput {
            padding: 0.75rem 1rem 1rem;
        }
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 3px;
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(139, 92, 246, 0.4);
        border-radius: 3px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(139, 92, 246, 0.6);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_url" not in st.session_state:
    st.session_state.api_url = ""
if "connected" not in st.session_state:
    st.session_state.connected = False


def escape_dollars(text: str) -> str:
    """Escape dollar signs to prevent LaTeX rendering."""
    text = re.sub(r'\$(\d)', r'&#36;\1', text)
    text = text.replace('$', '&#36;')
    return text


def query_api(user_query: str) -> str:
    """Send query to the API and return response."""
    try:
        url = f"{st.session_state.api_url}?user_query={requests.utils.quote(user_query)}"
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()
        if isinstance(data, dict):
            result = data.get("body") or data.get("response") or data.get("message") or str(data)
        else:
            result = str(data)

        return escape_dollars(result)
    except requests.exceptions.RequestException as e:
        return f"Error connecting to API: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


def render_message(role: str, content: str):
    """Render a chat message with glassmorphism styling."""
    avatar = "👤" if role == "user" else "🤖"
    msg_class = "user" if role == "user" else "bot"

    safe_content = content.replace("<", "&lt;").replace(">", "&gt;")
    safe_content = safe_content.replace("\n", "<br>")

    st.markdown(f"""
    <div class="chat-message {msg_class}">
        <div class="avatar">{avatar}</div>
        <div class="content">{safe_content}</div>
    </div>
    """, unsafe_allow_html=True)


# Sidebar for API configuration
with st.sidebar:
    st.markdown("### ⚙️ API Configuration")

    api_url = st.text_input(
        "API Endpoint URL",
        value=st.session_state.api_url,
        placeholder="https://your-api.execute-api.region.amazonaws.com/stage",
        help="Enter your AWS API Gateway endpoint URL"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Connect", use_container_width=True):
            if api_url:
                st.session_state.api_url = api_url
                st.session_state.connected = True
                st.success("✅ Connected!")
                st.rerun()
            else:
                st.error("Please enter a URL")

    with col2:
        if st.button("Disconnect", use_container_width=True):
            st.session_state.api_url = ""
            st.session_state.connected = False
            st.session_state.messages = []
            st.rerun()

    if st.session_state.connected:
        st.markdown("""
        <div class="url-badge">
            🟢 Connected
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    **💡 Tip:** Your API should accept a `user_query` parameter.
    """)


# Main content
if not st.session_state.connected:
    # Setup screen
    st.markdown("""
    <div class="header-container">
        <div class="header-icon">🔗</div>
        <div class="header-title">Connect to Your Backend</div>
        <div class="header-subtitle">Enter your AWS API endpoint URL to get started</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        setup_url = st.text_input(
            "API Endpoint URL",
            placeholder="https://your-api.execute-api.region.amazonaws.com/stage",
            label_visibility="collapsed",
            key="setup_url"
        )

        if st.button("🚀 Connect & Start Chatting", use_container_width=True):
            if setup_url:
                st.session_state.api_url = setup_url
                st.session_state.connected = True
                st.rerun()
            else:
                st.error("Please enter a valid URL")

else:
    # Chat interface
    st.markdown("""
    <div class="header-container">
        <div class="header-icon">🤖</div>
        <div class="header-title">Corporate Data Assistant</div>
        <div class="header-subtitle">Ask me anything about corporate data & reports</div>
    </div>
    """, unsafe_allow_html=True)

    # Chat messages
    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome-container">
            <h3>👋 Hello! I'm your Corporate Data Assistant</h3>
            <p>I can help you explore corporate financial data, annual reports, and growth metrics.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**✨ Try asking:**")
        col1, col2, col3 = st.columns(3)

        suggestions = [
            ("📈 Amazon 2023 Growth", "What is the growth reported in 2023 for Amazon?"),
            ("🍎 Apple Revenue 2023", "What was Apple revenue in 2023?"),
            ("📊 MS vs Google", "Compare Microsoft and Google profits")
        ]

        for i, (label, query) in enumerate(suggestions):
            col = [col1, col2, col3][i]
            with col:
                if st.button(label, key=f"sug_{i}", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": query})
                    with st.spinner("Thinking..."):
                        response = query_api(query)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
    else:
        # Display chat history
        for message in st.session_state.messages:
            render_message(message["role"], message["content"])

        # Clear chat button
        st.markdown('<div class="clear-btn-container">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🗑️ Clear Chat", type="secondary", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Chat input - Fixed at bottom (Streamlit's native chat_input)
    if prompt := st.chat_input("Ask about corporate data..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("Thinking..."):
            response = query_api(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
