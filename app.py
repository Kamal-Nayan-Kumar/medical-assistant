import os
import streamlit as st
from dotenv import load_dotenv
from src.google_search_handler import google_search
from src.gemini_ai_handler import generate_gemini_answer

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Medical AI Assistant", page_icon="🩺", layout="centered")

st.title("🩺 Medical AI Assistant")
st.markdown(
    "Ask any medical question. The assistant will answer using only trusted research and official sources, with clickable citations."
)

def format_context(search_results):
    if not search_results:
        return "No relevant information found from trusted medical sources."
    context = ""
    for i, item in enumerate(search_results):
        context += f"Source [{i+1}]: {item['title']} ({item['url']})\nSnippet: {item['snippet']}\n\n"
    return context

def extract_citations(answer, search_results):
    # Replace [number] with clickable links
    for i, item in enumerate(search_results):
        citation_tag = f"[{i+1}]"
        citation_link = f'<a href="{item["url"]}" target="_blank">{citation_tag}</a>'
        answer = answer.replace(citation_tag, citation_link)
    return answer

if "history" not in st.session_state:
    st.session_state.history = []

with st.form("query_form", clear_on_submit=True):
    user_query = st.text_input("Enter your medical question:", "")
    submitted = st.form_submit_button("Ask")

if submitted and user_query.strip():
    with st.spinner("Searching trusted medical sources..."):
        search_results = google_search(user_query, GOOGLE_API_KEY, GOOGLE_CSE_ID, num=5)
    context = format_context(search_results)
    with st.spinner("Generating answer with Gemini..."):
        answer = generate_gemini_answer(GEMINI_API_KEY, user_query, context)
        answer_with_links = extract_citations(answer, search_results)
    # Save to history
    st.session_state.history.append({
        "query": user_query,
        "answer": answer_with_links,
        "sources": search_results,
    })

# Display chat history
for entry in reversed(st.session_state.history):
    st.markdown(f"**You:** {entry['query']}")
    st.markdown(f"**AI Assistant:**", unsafe_allow_html=True)
    st.markdown(entry["answer"], unsafe_allow_html=True)
    if entry["sources"]:
        st.markdown("**Sources:**")
        for i, item in enumerate(entry["sources"]):
            st.markdown(f"[{i+1}] [{item['title']}]({item['url']})")

st.markdown("---")
st.caption("Powered by Google Search API & Gemini | For informational purposes only.")
