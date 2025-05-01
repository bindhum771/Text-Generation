import streamlit as st
from transformers import pipeline, set_seed
from deep_translator import GoogleTranslator
import streamlit.components.v1 as components

# Load GPT-Neo model
generator = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")
set_seed(42)

# App UI
st.set_page_config(page_title="GPT-Neo Text Generator", layout="centered")
st.title("📝 GPT-Neo Based Text Generator")

prompt = st.text_input("Enter your topic or question:")
length_type = st.radio("Response Length:", ["Short", "Detailed"])
generate_button = st.button("Generate")

if generate_button and prompt:
    n_paragraphs = 1 if length_type == "Short" else 5
    st.info(f"Generating {n_paragraphs} paragraph(s)...")
    
    outputs = generator(prompt, max_length=300, num_return_sequences=n_paragraphs, 
                        temperature=0.7, top_p=0.95, top_k=50)
    all_text = "\n\n".join([out["generated_text"] for out in outputs])

    st.subheader("📄 Generated Text")
    st.text_area("Output", all_text, height=300)

    # Copy to clipboard
    safe_output = all_text.replace("`", "\`").replace("\", "\\").replace("\n", "\\n")
    components.html(f'''
        <textarea id="copyText" style="height:0;opacity:0">{safe_output}</textarea>
        <button onclick="copyToClipboard()" style="
            background-color:#4CAF50;
            border:none;
            color:white;
            padding:10px 20px;
            text-align:center;
            font-size:16px;
            margin-top:10px;
            border-radius:5px;
            cursor:pointer;
        ">📋 Copy to Clipboard</button>
        <script>
        function copyToClipboard() {{
            var copyText = document.getElementById("copyText");
            copyText.select();
            document.execCommand("copy");
        }}
        </script>
    ''', height=100)

    # Translation
    with st.expander("🌍 Translate Output"):
        target_lang = st.selectbox("Choose language:", [
            "french", "spanish", "german", "tamil", "hindi", "chinese (simplified)",
            "japanese", "arabic", "russian", "bengali"
        ])
        if st.button("Translate"):
            lang_code_map = {
                "french": "fr", "spanish": "es", "german": "de", "tamil": "ta", "hindi": "hi",
                "chinese (simplified)": "zh-CN", "japanese": "ja", "arabic": "ar",
                "russian": "ru", "bengali": "bn"
            }
            translated = GoogleTranslator(target=lang_code_map[target_lang]).translate(all_text)
            st.success(f"Translated to {target_lang.title()}:")
            st.text_area("📜 Translated Text", translated, height=200)