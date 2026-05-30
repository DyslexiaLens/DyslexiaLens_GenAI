import os
import re
import streamlit as st
from google import genai
from google.genai import types

# ──────────────────────────────────────────────────────────────────────────────
# 1. GEMINI PROMPT GENERATION UTILITY
# ──────────────────────────────────────────────────────────────────────────────
def fetch_assessment_sentence() -> str:
    """
    Calls Gemini 1.5 Flash to generate a unique 5-word handwriting prompt.
    Enforces a strict validation loop to prevent grid overflow.
    """
    # The client automatically picks up GEMINI_API_KEY from the system environment
    try:
        client = genai.Client()
    except Exception:
        # Graceful handling if the API key environment variable isn't set yet
        return "Write clear words right now."

    system_instruction = (
        "You are a clinical linguistic assistant generating text for a handwriting test grid.\n"
        "Rules:\n"
        "1. Generate exactly ONE simple, meaningful sentence.\n"
        "2. The sentence must contain EXACTLY 5 words.\n"
        "3. Each individual word must be between 1 and 8 letters long maximum.\n"
        "4. No punctuation except a single period at the end."
    )

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents="Generate a new 5-word clinical handwriting evaluation phrase.",
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.8,
                )
            )
            raw_text = response.text.strip()
            
            # Validation logic
            clean_text = re.sub(r'[^\w\s]', '', raw_text)
            words = clean_text.split()
            
            if len(words) == 5 and all(len(w) <= 8 for w in words):
                return raw_text
        except Exception:
            continue
            
    # Bulletproof fallback sentence matching the exact structural bounds
    return "Great minds build bright ideas."

# ──────────────────────────────────────────────────────────────────────────────
# 2. STREAMLIT INTERFACE COMPONENT
# ──────────────────────────────────────────────────────────────────────────────
def render_genai_assessment_tab():
    st.header("📝 Dynamic Clinical Handwriting Assessment")
    st.write(
        "Generate a randomized, structurally constrained sentence for the patient "
        "to write on the physical custom test grid. This sentence is optimized to prevent "
        "spatial layout overflows while capturing baseline motor phenotypes."
    )
    
    # Initialize session state for the prompt text so it doesn't clear on every rerun
    if "handwriting_prompt" not in st.session_state:
        st.session_state.handwriting_prompt = "Click the button below to generate a sentence."

    # Action button
    if st.button("✨ Generate New Custom Prompt", type="primary"):
        with st.spinner("Analyzing linguistic constraints via Gemini..."):
            st.session_state.handwriting_prompt = fetch_assessment_sentence()

    # Display the prompt visually to the user/clinician
    st.info(f"**Target Sentence to Write:** \n\n ## `{st.session_state.handwriting_prompt}`")
    
    # Instructions for the custom grid layout
    st.subheader("📋 Custom Printed Grid Alignment Check")
    words = re.sub(r'[^\w\s]', '', st.session_state.handwriting_prompt).split()
    
    if len(words) == 5:
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.metric(
                    label=f"Box {i+1} (Max 8 Chars)", 
                    value=f"{len(words[i])} Letters", 
                    delta=f"Word: {words[i]}"
                )

if __name__ == "__main__":
    render_genai_assessment_tab()