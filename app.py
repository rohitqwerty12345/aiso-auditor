import streamlit as st
import google.generativeai as genai
from openai import OpenAI
import requests
import json

# --- CONFIGURATION & UI ---
st.set_page_config(page_title="AISO Auditor | Pro Brand Intelligence", layout="wide")

# Custom CSS for Premium Dark Mode
st.markdown("""
    <style>
    .main { background-color: #000000; color: #ffffff; }
    .stTextInput>div>div>input { background-color: #111; color: white; border: 1px solid #333; }
    .stButton>button { 
        background: linear-gradient(90deg, #3b82f6, #8b5cf6); 
        color: white; border: none; padding: 15px; font-weight: bold; border-radius: 10px;
    }
    .report-box { background-color: #0a0a0a; border: 1px solid #1a1a1a; padding: 25px; border-radius: 15px; }
    .metric-text { font-size: 24px; font-weight: bold; color: #60a5fa; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: CREDENTIALS ---
with st.sidebar:
    st.title("🛡️ Secure Logic Hub")
    st.subheader("API Access (Pro Models)")
    gemini_api = st.text_input("Gemini API Key", type="password")
    openai_api = st.text_input("OpenAI API Key", type="password")
    tavily_api = st.text_input("Tavily API Key", type="password")
    st.markdown("---")
    st.caption("This tool uses Gemini 1.5 Pro & GPT-4o for enterprise-grade analysis.")

# --- MAIN INTERFACE ---
st.title("⚡ AISO Brand Intelligence Hub")
st.markdown("##### The Auditor for the AI Search Economy")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        brand = st.text_input("Enter Your Brand", value="EduTap")
    with col2:
        competitor = st.text_input("Enter Competitor", value="Anuj Jindal")
    
    query = st.text_area("The Strategic Probe (The question buyers ask AI)", 
                         value="Who provides the most comprehensive RBI Grade B course with the best toppers record?")

if st.button("EXECUTE PRO FORENSIC AUDIT"):
    if not (gemini_api and openai_api and tavily_api):
        st.error("Missing API Keys. Please configure the sidebar.")
    else:
        with st.spinner("Pro Agents are probing LLM Search results..."):
            
            try:
                # 1. THE INQUISITOR (Gemini 1.5 Pro)
                genai.configure(api_key=gemini_api)
                gem_model = genai.GenerativeModel('gemini-1.5-pro')
                gem_res = gem_model.generate_content(f"Answer this specifically comparing {brand} and {competitor}: {query}").text

                # 2. THE ANALYST (GPT-4o)
                oa_client = OpenAI(api_key=openai_api)
                gpt_res = oa_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": f"Answer this specifically comparing {brand} and {competitor}: {query}"}]
                ).choices[0].message.content

                # 3. THE FORENSIC SCOUT (Tavily)
                search_payload = {
                    "api_key": tavily_api,
                    "query": f"Why is {competitor} recommended over {brand} for RBI Grade B prep?",
                    "search_depth": "advanced",
                    "include_answer": True
                }
                tavily_data = requests.post("https://api.tavily.com/search", json=search_payload).json()

                # 4. THE STRATEGIST (Agentic Logic for Action Plan)
                strat_prompt = f"""
                DATA INPUTS:
                Gemini Pro Verdict: {gem_res}
                GPT-4o Verdict: {gpt_res}
                Search Evidence: {json.dumps(tavily_data)}

                TASK:
                1. Identify why {brand} is being ignored or criticized.
                2. List 3 specific Revenue Recovery actions.
                3. Create a technical AISO Schema (JSON-LD) to fix this.
                """
                action_plan = gem_model.generate_content(strat_prompt).text

                # --- DASHBOARD DISPLAY ---
                st.markdown("### 📊 Live Reputation Dashboard")
                
                tab1, tab2, tab3 = st.tabs(["AI Perception", "Forensic Evidence", "Strategic Action Plan"])
                
                with tab1:
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("**Gemini 1.5 Pro Verdict**")
                        st.info(gem_res)
                    with c2:
                        st.markdown("**GPT-4o Verdict**")
                        st.success(gpt_res)
                
                with tab2:
                    st.markdown("**Top Sources Influencing AI Perception**")
                    for result in tavily_data.get('results', []):
                        st.write(f"🔗 [{result['title']}]({result['url']})")
                        st.caption(result['content'][:200] + "...")

                with tab3:
                    st.markdown("**The Fix: Executive Action Plan**")
                    st.write(action_plan)
                
            except Exception as e:
                st.error(f"Error during audit: {str(e)}")
