import streamlit as st
import os
from google import genai

# Configure the Streamlit page
st.set_page_config(page_title="A4 Grid Sentence Generator", layout="centered")
st.title("🧩 A4 Grid Sentence Generator")
st.write("Generate custom sentences tailored to fit exactly into an 8x5 character block grid layout.")

# API Key input setup
api_key = st.text_input("Enter your Gemini API Key:", type="password", value=os.environ.get("GEMINI_API_KEY", ""))

if api_key:
    # Initialize the official Google GenAI Client
    client = genai.Client(api_key=api_key)
    
    # Layout options for the user
    language = st.selectbox("Select Language:", ["English", "Bahasa Indonesia"])
    topic = st.text_input("Enter a theme or topic (optional):", placeholder="e.g., coffee, coding, running, food")
    
    if st.button("Generate Grid Sentence", type="primary"):
        # The prompt strictly enforces your formatting rules
        prompt = (
            f"Generate one creative sentence in {language} about: {topic if topic else 'any random interesting topic'}.\n\n"
            f"STRICT MECHANICAL CONSTRAINTS:\n"
            f"1. The sentence must consist of EXACTLY 5 words.\n"
            f"2. Every single word must have a MAXIMUM length of 8 letters.\n"
            f"3. Do not include punctuation marks like periods, commas, or quotes.\n"
            f"4. Provide ONLY the final sentence string. No intro, no outro, no explanations."
        )
        
        with st.spinner("Gemini is brainstorming..."):
            try:
                # Call the standard, fast Gemini Flash model
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                
                # Sanitize response
                sentence = response.text.strip()
                words = sentence.split()
                
                st.subheader("✨ Generated Sentence:")
                st.info(f"**{sentence}**")
                
                # Layout checking mechanics
                st.write("### 📊 Grid Verification Analysis")
                grid_analysis = []
                is_valid = True
                
                for idx, word in enumerate(words):
                    clean_word = word.translate(str.maketrans('', '', '.,!?“”"\''))
                    length = len(clean_word)
                    status = "✅ Fits" if length <= 8 else "❌ Exceeds 8 Letters!"
                    if length > 8:
                        is_valid = False
                    
                    grid_analysis.append({
                        "Word Order": f"Word {idx+1}",
                        "Word Text": clean_word,
                        "Letter Count": f"{length} / 8",
                        "Status": status
                    })
                
                st.table(grid_analysis)
                
                # Safety checks for total word counts
                if len(words) != 5:
                    st.warning(f"⚠️ Gemini outputted {len(words)} words instead of exactly 5. Hit the button again to retry!")
                elif not is_valid:
                    st.warning("⚠️ One of the generated words broke the 8-letter limit barrier. Click generate to try another seed.")
                else:
                    st.balloons()
                    st.success("Perfect alignment! This fits your A4 page layout seamlessly.")
                    
                    # Generate a clean visual box mock-up for the user
                    st.write("### 🗺️ Your A4 Grid Preview:")
                    for word in words:
                        clean_word = word.translate(str.maketrans('', '', '.,!?“”"\'')).upper()
                        # Pad the word out to 8 spaces cleanly
                        padded_word = clean_word.ljust(8, " ")
                        visual_row = " ".join([f"[{char}]" for char in padded_word])
                        st.code(visual_row, language="text")
                        
            except Exception as e:
                st.error(f"Failed to communicate with Gemini API: {e}")
else:
    st.warning("🔑 Please enter your Gemini API key to activate the tool. You can fetch one for free inside Google AI Studio.")