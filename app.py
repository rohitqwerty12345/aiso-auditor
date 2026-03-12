import streamlit as st
from google import genai
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
                # 1. THE INQUISITOR (New Google GenAI SDK)
                client_gemini = genai.Client(api_key=gemini_api)
                # Using the stable 'gemini-1.5-pro' identifier for the new SDK
                gem_res = client_gemini.models.generate_content(
                    model='gemini-1.5-pro', 
                    contents=f"Compare {brand} and {competitor}: {query}"
                ).text

                # 2. THE ANALYST (GPT-4o)
                oa_client = OpenAI(api_key=openai_api)
                gpt_res = oa_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": f"Compare {brand} and {competitor}: {query}"}]
                ).choices[0].message.content

                # 3. FORENSIC SEARCH (Tavily)
                tavily_data = requests.post("https://api.tavily.com/search", json={
                    "api_key": tavily_api, 
                    "query": f"Why is {competitor} recommended over {brand} for RBI Grade B preparation?", 
                    "search_depth": "advanced"
                }).json()

                # 4. THE STRATEGIST (Agentic Logic)
                strat_prompt = f"""
                Data: {gem_res} 
                {gpt_res} 
                Search Results: {json.dumps(tavily_data)}
                
                Task: Build a 3-step action plan for {brand} to fix their AI reputation.
                """
                action_plan = client_gemini.models.generate_content(
                    model='gemini-1.5-pro', 
                    contents=strat_prompt
                ).text

                # --- DISPLAY ---
                tab1, tab2, tab3 = st.tabs(["AI Perception", "Forensic Evidence", "Action Plan"])
                with tab1:
                    st.info(f"**Gemini 1.5 Pro Verdict:**\n\n{gem_res}")
                    st.success(f"**GPT-4o Verdict:**\n\n{gpt_res}")
                with tab2:
                    st.markdown("**Top Sources Feeding the AI Perception:**")
                    for r in tavily_data.get('results', []):
                        st.markdown(f"🔗 [{r['title']}]({r['url']})")
                with tab3:
                    st.write(action_plan)
                
            except Exception as e:
                st.error(f"Audit failed: {str(e)}")
