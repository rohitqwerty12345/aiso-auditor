import streamlit as st
from google import genai
from openai import OpenAI
import requests
import json

# --- PRE-CONFIG & UI STYLING ---
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
    .report-card { background-color: #111; padding: 20px; border-radius: 10px; border-left: 5px solid #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: KEYS ---
with st.sidebar:
    st.title("🔐 AISO Logic Hub")
    st.markdown("Enter your Pro API keys to begin the forensic audit.")
    gemini_api = st.text_input("Gemini API Key", type="password")
    openai_api = st.text_input("OpenAI API Key", type="password")
    tavily_api = st.text_input("Tavily API Key", type="password")
    st.markdown("---")
    st.caption("Models: Gemini 3.1 Pro Preview & GPT-4o")

# --- MAIN DASHBOARD ---
st.title("⚡ AISO Brand Intelligence Hub")
st.markdown("#### Audit and Re-Engineer your Reputation in the AI Search Economy")

col1, col2 = st.columns(2)
with col1:
    brand = st.text_input("Your Brand", value="EduTap")
with col2:
    competitor = st.text_input("Competitor(s)", value="Anuj Jindal, Oliveboard")

query = st.text_area("The Strategic Search Probe", 
                     value="Who provides the most comprehensive RBI Grade B course with the best toppers record?")

if st.button("EXECUTE PRO FORENSIC AUDIT"):
    if not (gemini_api and openai_api and tavily_api):
        st.error("Please provide all API keys in the sidebar.")
    else:
        with st.spinner("Pro Agents are analyzing LLM training data and search evidence..."):
            try:
                # 1. INITIALIZE CLIENTS
                client_gem = genai.Client(api_key=gemini_api)
                client_oa = OpenAI(api_key=openai_api)

                # 2. PHASE 1: GEMINI PROBE (Gemini 3 Flash for speed)
                gem_res = client_gem.models.generate_content(
                    model='gemini-3-flash-preview', 
                    contents=f"You are a neutral buyer. Answer this: {query}. Explicitly compare {brand} and {competitor}."
                ).text

                # 3. PHASE 2: CHATGPT PROBE (GPT-4o)
                gpt_res = client_oa.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": f"You are a neutral buyer. Answer this: {query}. Explicitly compare {brand} and {competitor}."}]
                ).choices[0].message.content

                # 4. PHASE 3: TAVILY FORENSIC SEARCH (The 'Training Data')
                search_query = f"Why do people prefer {competitor} over {brand}? Find specific criticisms and mentor data gaps."
                tavily_data = requests.post("https://api.tavily.com/search", json={
                    "api_key": tavily_api,
                    "query": search_query,
                    "search_depth": "advanced"
                }).json()

                # 5. PHASE 4: THE STRATEGIST (AISO Specific Intelligence)
                # This prompt forces the AI to focus on DATA and SEARCH results, not general marketing.
                strat_prompt = f"""
                You are a Senior AISO (AI Search Optimization) Specialist. 
                
                INPUT DATA:
                1. Gemini Verdict: {gem_res}
                2. GPT Verdict: {gpt_res}
                3. Search Evidence: {json.dumps(tavily_data)}
                
                TASK:
                Identify why AI models are biased toward {competitor} and create an 'AI Data Correction Plan' for {brand}.
                
                FOCUS AREAS:
                - STEP 1: SOURCE SUPPRESSION: Identify the URLs feeding negative info and tell us how to 'neutralize' their impact on AI training.
                - STEP 2: AUTHORITY INJECTION: What specific keywords or credentials (e.g., 'Ph.D.', '65% Success Rate') are we missing in our web-data?
                - STEP 3: TECHNICAL SCHEMA: Provide the exact JSON-LD code needed to fix our Brand perception for LLM crawlers.
                """
                
                action_plan = client_gem.models.generate_content(
                    model='gemini-3.1-pro-preview', 
                    contents=strat_prompt
                ).text

                # --- DASHBOARD OUTPUT ---
                st.divider()
                tab1, tab2, tab3 = st.tabs(["📊 AI Perception", "🔍 Forensic Evidence", "💡 AISO Action Plan"])

                with tab1:
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("### Gemini 3.1 Pro Verdict")
                        st.info(gem_res)
                    with c2:
                        st.markdown("### GPT-4o Verdict")
                        st.success(gpt_res)

                with tab2:
                    st.markdown("### Top Sources Influencing the AI 'Hive-Mind'")
                    if 'results' in tavily_data:
                        for r in tavily_data['results']:
                            st.markdown(f"📍 **[{r['title']}]({r['url']})**")
                            st.write(r.get('content', '')[:300] + "...")
                            st.markdown("---")

                with tab3:
                    st.markdown("### Executive AISO Correction Plan")
                    st.markdown(action_plan)

            except Exception as e:
                st.error(f"Audit failed: {str(e)}")
