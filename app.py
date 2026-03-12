import streamlit as st
from google import genai
from openai import OpenAI
import requests
import json
import pandas as pd

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
    .stMetric { background-color: #111; padding: 15px; border-radius: 10px; border: 1px solid #222; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: KEYS ---
with st.sidebar:
    st.title("🔐 AISO Logic Hub")
    gemini_api = st.text_input("Gemini API Key", type="password")
    openai_api = st.text_input("OpenAI API Key", type="password")
    tavily_api = st.text_input("Tavily API Key", type="password")
    st.markdown("---")
    st.info("**CEO Pitch Tip:** Use the 'Evidence' tab to show clients exactly which links are poisoning their AI reputation.")

# --- MAIN DASHBOARD ---
st.title("⚡ AISO Brand Intelligence Hub")
st.markdown("#### Audit and Re-Engineer your Reputation in the AI Search Economy")

col1, col2 = st.columns(2)
with col1:
    brand = st.text_input("Your Brand", value="EduTap")
with col2:
    competitor = st.text_input("Primary Competitor", value="Anuj Jindal")

query = st.text_area("The Strategic Search Probe", 
                     value="Who provides the most comprehensive RBI Grade B course with the best toppers record?")

if st.button("EXECUTE PRO FORENSIC AUDIT"):
    if not (gemini_api and openai_api and tavily_api):
        st.error("Please provide all API keys in the sidebar.")
    else:
        with st.spinner("Pro Agents are probing the AI Hive-Mind..."):
            try:
                # 1. INITIALIZE CLIENTS
                client_gem = genai.Client(api_key=gemini_api)
                client_oa = OpenAI(api_key=openai_api)

                # 2. PHASE 1: GEMINI PROBE
                gem_res = client_gem.models.generate_content(
                    model='gemini-3-flash-preview', 
                    contents=f"Compare {brand} and {competitor}: {query}"
                ).text

                # 3. PHASE 2: CHATGPT PROBE
                gpt_res = client_oa.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": f"Compare {brand} and {competitor}: {query}"}]
                ).choices[0].message.content

                # 4. PHASE 3: TAVILY FORENSIC SEARCH
                tavily_data = requests.post("https://api.tavily.com/search", json={
                    "api_key": tavily_api,
                    "query": f"Why is {competitor} better than {brand}? Find criticisms.",
                    "search_depth": "advanced"
                }).json()

                # 5. PHASE 4: QUANTITATIVE SCORING (For the Chart)
                scoring_prompt = f"Based on: {gem_res} and {gpt_res}, give a Trust Score (0-100) for {brand} and {competitor}. Return ONLY JSON: {{\"brand_score\": X, \"comp_score\": Y}}"
                score_json = client_gem.models.generate_content(model='gemini-3-flash-preview', contents=scoring_prompt).text
                scores = json.loads(score_json.strip().replace("```json", "").replace("```", ""))

                # 6. PHASE 5: THE STRATEGIST (AISO Specific)
                strat_prompt = f"Data: {gem_res} {gpt_res} {json.dumps(tavily_data)}. Create a 3-step AISO plan to fix {brand} perception."
                action_plan = client_gem.models.generate_content(model='gemini-3.1-pro-preview', contents=strat_prompt).text

                # --- DASHBOARD VISUALS ---
                st.divider()
                st.subheader("📊 Competitor Benchmarking (AI Trust Score)")
                
                chart_data = pd.DataFrame({
                    "Entity": [brand, competitor],
                    "Trust Score": [scores['brand_score'], scores['comp_score']]
                })
                st.bar_chart(data=chart_data, x="Entity", y="Trust Score", color="Entity")
                
                m1, m2 = st.columns(2)
                m1.metric(f"{brand} Trust", f"{scores['brand_score']}%", f"{scores['brand_score'] - scores['comp_score']}%")
                m2.metric(f"{competitor} Trust", f"{scores['comp_score']}%")

                # --- TABS ---
                st.divider()
                t1, t2, t3 = st.tabs(["🤖 AI Perception", "🔍 Forensic Evidence", "🎯 AISO Action Plan"])

                with t1:
                    c1, c2 = st.columns(2)
                    c1.info(f"**Gemini Verdict:**\n\n{gem_res}")
                    c2.success(f"**GPT-4o Verdict:**\n\n{gpt_res}")

                with t2:
                    st.markdown("### Evidence identified in AI Training Data")
                    for r in tavily_data.get('results', []):
                        st.markdown(f"📍 **[{r['title']}]({r['url']})**")
                        st.write(r.get('content', '')[:250] + "...")

                with t3:
                    st.markdown(action_plan)

            except Exception as e:
                st.error(f"Audit failed: {str(e)}")
