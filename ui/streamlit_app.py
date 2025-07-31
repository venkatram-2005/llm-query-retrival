import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000/hackrx/run")
API_KEY = os.getenv("API_KEY")

st.set_page_config(page_title="LLM Query Retrieval", layout="centered")
st.title("📄 LLM-Powered Document Q&A")
st.markdown("Ask natural language questions against your PDF, DOCX, or email documents.")

# Form Inputs
with st.form("query_form"):
    document_url = st.text_input("🔗 Document Blob URL / Public Link", "")
    questions_input = st.text_area("❓ Your Questions (one per line)", "")
    submitted = st.form_submit_button("🔍 Run Query")

    if submitted:
        if not document_url or not questions_input.strip():
            st.warning("Please provide both the document URL and at least one question.")
        else:
            questions = [q.strip() for q in questions_input.splitlines() if q.strip()]
            payload = {
                "documents": document_url,
                "questions": questions
            }
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            with st.spinner("Processing your query..."):
                try:
                    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
                    response.raise_for_status()
                    result = response.json()

                    if "answers" not in result:
                        st.error("Response format invalid: missing 'answers' field.")
                    else:
                        st.success("✅ Answers Retrieved")
                        for idx, answer in enumerate(result["answers"]):
                            st.markdown(f"### Q{idx+1}: {questions[idx]}")
                            st.markdown(f"**Answer:** {answer}")
                            st.markdown("---")

                except Exception as e:
                    st.error(f"🚫 Error: {str(e)}")
