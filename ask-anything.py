import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Ask with Gemini", page_icon="💬")

st.title("💬 Ask Anything (Gemini)")

# -------------------------------
# 🔑 Sidebar: API Key Input
# -------------------------------
with st.sidebar:
    st.header("🔐 Gemini API Key")
    API_KEY = st.text_input("Enter your Gemini API key", type="password")
    st.caption("Get one from https://aistudio.google.com/app/apikey")

if not API_KEY:
    st.info("Please input your Gemini API key to proceed.")
    st.stop()

# -------------------------------
# ⚙️ Configure Gemini client
# -------------------------------
try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Error configuring Gemini client: {e}")
    st.stop()

# -------------------------------
# 🔍 List available models
# -------------------------------
try:
    models = genai.list_models()
    gen_models = [
        m for m in models
        if hasattr(m, "supported_generation_methods")
        and "generateContent" in m.supported_generation_methods
    ]
except Exception as e:
    st.error(f"Failed to fetch models: {e}")
    st.stop()

if not gen_models:
    st.error("No models found that support text generation. Check your API key or permissions.")
    st.stop()

# -------------------------------
# 🎛️ Model Selector
# -------------------------------
model_names = [m.name for m in gen_models]
display_names = [m.name.split("/")[-1] for m in gen_models]
selected_model = st.selectbox(
    "Choose a Gemini model",
    options=model_names,
    format_func=lambda x: x.split("/")[-1]
)

st.write(f"Using model: **{selected_model.split('/')[-1]}**")

# -------------------------------
# 💬 Question Input
# -------------------------------
question = st.text_area("Enter your question:")

# -------------------------------
# 🚀 Generate Response
# -------------------------------
if st.button("Ask"):
    if not question.strip():
        st.warning("Please type a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                model = genai.GenerativeModel(selected_model)
                response = model.generate_content(question)
                st.success("✅ Gemini Response:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error generating content: {e}")
