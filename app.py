import streamlit as st
from google import genai
from openai import OpenAI
import requests
import json

# --- PRE-CONFIG & UI ---
st.set_page_config(page_title="AISO Brand Auditor Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d0d0d; color: #ffffff; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { 
        background-color: #1a1a1a; color: white; border: 1px solid #333; border-radius: 8px;
    }
    .stButton>button { 
        background: linear-gradient(90deg, #2563eb, #7c3aed); 
        color: white; border: none; padding: 12px; font-weight: bold; border-radius: 10px; width: 100%;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: KEYS ---
with st.sidebar:
    st.title("🔐 API Logic Center")
    gemini_api = st.text_input("Gemini API Key", type="password")
    openai_api = st.text_input("OpenAI API Key", type="password")
    tavily_api = st.text_input("Tavily API Key", type="password")
    st.markdown("---")
    st.caption("Running: Gemini 3.1 Pro & GPT-4o")

# --- MAIN DASHBOARD ---
st.title("⚡ AISO Brand Intelligence Hub")
st.markdown("#### Audit your reputation in the AI Search Economy")

col1, col2 = st.columns(2)
with col1:
    brand = st.text_input("Target Brand", value="EduTap")
with col2:
    competitor = st.text_input("Competitors (Comma separated)", value="Anuj Jindal, Oliveboard")

query = st.text_area("Strategic Search Probe", value="Who provides the most comprehensive RBI Grade B course with the best toppers record?")

if st.button("EXECUTE PRO FORENSIC AUDIT"):
    if not (gemini_api and openai_api and tavily_api):
        st.error("Missing API Keys in the sidebar.")
    else:
        with st.spinner("Pro Agents are analyzing LLM perceptions and search evidence..."):
            try:
                # 1. INITIALIZE CLIENTS
                client_gemini = genai.Client(api_key=gemini_api)
                client_openai = OpenAI(api_key=openai_api)

                # 2. PHASE 1: GEMINI PROBE (Gemini 3 Flash)
                # Using exact slug from documentation - no prefix
                gem_res = client_gemini.models.generate_content(
                    model='gemini-3-flash-preview', 
                    contents=f"Conduct a detailed brand audit. Compare {brand} vs {competitor} for this query: {query}"
                ).text

                # 3. PHASE 2: CHATGPT PROBE (GPT-4o)
                gpt_res = client_openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": f"Conduct a detailed brand audit. Compare {brand} vs {competitor} for this query: {query}"}]
                ).choices[0].message.content

                # 4. PHASE 3: TAVILY FORENSIC SEARCH
                tavily_data = requests.post("https://api.tavily.com/search", json={
                    "api_key": tavily_api,
                    "query": f"Why is {competitor} often preferred over {brand}? Find criticisms and authority gaps.",
                    "search_depth": "advanced"
                }).json()

                # 5. PHASE 4: THE STRATEGIST (Gemini 3.1 Pro)
                # Using Pro for the heavy-lifting strategic summary
                strat_input = f"Gemini Sentiment: {gem_res}\n\nGPT Sentiment: {gpt_res}\n\nSearch Evidence: {json.dumps(tavily_data)}"
                action_plan = client_gemini.models.generate_content(
                    model='gemini-3.1-pro-preview', 
                    contents=f"You are a Senior Strategist. Based on this data, create a 3-step revenue recovery plan for {brand}:\n\n{strat_input}"
                ).text

                # --- DASHBOARD OUTPUT ---
                st.divider()
                tab1, tab2, tab3 = st.tabs(["📊 AI Perception", "🔍 Forensic Evidence", "💡 Strategic Fix"])

                with tab1:
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("### Gemini Verdict")
                        st.info(gem_res)
                    with c2:
                        st.markdown("### ChatGPT Verdict")
                        st.success(gpt_res)

                with tab2:
                    st.markdown("### Top Sources Influencing AI Decisions")
                    if 'results' in tavily_data:
                        for r in tavily_data['results']:
                            st.markdown(f"📍 **[{r['title']}]({r['url']})**")
                            st.caption(f"Relevance Score: {r.get('score', 'N/A')}")
                            st.write(r.get('content', '')[:300] + "...")
                            st.markdown("---")

                with tab3:
                    st.markdown("### Executive Action Plan")
                    st.markdown(action_plan)

            except Exception as e:
                st.error(f"Audit failed: {str(e)}")
