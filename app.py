import streamlit as st
import google.generativeai as genai
from openai import OpenAI
import requests
import json

# --- CONFIG & UI ---
st.set_page_config(page_title="AISO Auditor | Pro Brand Intelligence", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000; color: #fff; }
    .stTextInput>div>div>input { background-color: #111; color: white; border: 1px solid #333; }
    .stButton>button { 
        background: linear-gradient(90deg, #3b82f6, #8b5cf6); 
        color: white; border: none; padding: 15px; font-weight: bold; border-radius: 10px; width: 100%;
    }
    .report-box { background-color: #0a0a0a; border: 1px solid #1a1a1a; padding: 25px; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Secure Logic Hub")
    gemini_api = st.text_input("Gemini API Key", type="password")
    openai_api = st.text_input("OpenAI API Key", type="password")
    tavily_api = st.text_input("Tavily API Key", type="password")

# --- MAIN UI ---
st.title("⚡ AISO Brand Intelligence Hub")
col1, col2 = st.columns(2)
with col1: brand = st.text_input("Your Brand", value="EduTap")
with col2: competitor = st.text_input("Competitor", value="Anuj Jindal")
query = st.text_area("The Strategic Probe", value="Who provides the most comprehensive RBI Grade B course?")

if st.button("EXECUTE PRO FORENSIC AUDIT"):
    if not (gemini_api and openai_api and tavily_api):
        st.error("Missing API Keys.")
    else:
        with st.spinner("Pro Agents are probing LLM Search results..."):
            try:
                # 1. THE INQUISITOR (Gemini 1.5 Pro Fix)
                genai.configure(api_key=gemini_api)
                # Using 'gemini-1.5-pro-latest' for the Pro tier
                gem_model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
                gem_res = gem_model.generate_content(f"Compare {brand} and {competitor}: {query}").text

                # 2. THE ANALYST (GPT-4o)
                oa_client = OpenAI(api_key=openai_api)
                gpt_res = oa_client.chat.completions.create(
                    model="gpt-4o", # Use "gpt-4o" for current pro model
                    messages=[{"role": "user", "content": f"Compare {brand} and {competitor}: {query}"}]
                ).choices[0].message.content

                # 3. FORENSIC SEARCH (Tavily)
                tavily_data = requests.post("https://api.tavily.com/search", json={
                    "api_key": tavily_api, "query": f"Why is {competitor} better than {brand}?", "search_depth": "advanced"
                }).json()

                # 4. THE STRATEGIST
                strat_prompt = f"Data: {gem_res} {gpt_res} {json.dumps(tavily_data)}. Task: Build 3-step action plan."
                action_plan = gem_model.generate_content(strat_prompt).text

                # DISPLAY
                tab1, tab2, tab3 = st.tabs(["AI Perception", "Forensic Evidence", "Action Plan"])
                with tab1:
                    st.info(f"**Gemini 1.5 Pro:** {gem_res}")
                    st.success(f"**GPT-4o:** {gpt_res}")
                with tab2:
                    for r in tavily_data.get('results', []):
                        st.markdown(f"🔗 [{r['title']}]({r['url']})")
                with tab3:
                    st.write(action_plan)
                
            except Exception as e:
                st.error(f"Audit failed: {str(e)}")
