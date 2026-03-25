import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="AI Data Analyzer", layout="wide")

st.title("Smart Data Analyzer AI Assistant")
st.markdown("Upload your dataset and get AI-powered insights")

# -------------------------
# File Upload
# -------------------------
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    st.success("File uploaded successfully")

    if st.button("Analyze Data"):
        with st.spinner("Analyzing..."):
            files = {"file": uploaded_file.getvalue()}

            response = requests.post(f"{API_URL}/api/upload", files={
                "file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")
            })

            if response.status_code == 200:
                data = response.json()

                st.subheader("Basic Info")
                st.json(data["analysis"]["basic_info"])

                st.subheader("Missing Data")
                st.json(data["analysis"]["missing_analysis"])

                st.subheader("Insights")
                st.json(data["analysis"]["insights"])

                st.subheader("ML Results")
                st.json(data["analysis"]["ml_results"])

                st.subheader("AI Explanation")
                st.write(data["analysis"]["llm_explanation"])

                # Save file path for querying
                st.session_state["file_path"] = f"data/{uploaded_file.name}"

            else:
                st.error(response.text)
                # st.error("Error analyzing file")

# -------------------------
# Chat Section
# -------------------------
st.markdown("---")
st.subheader("💬 Chat with your Data")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for role, message in st.session_state.chat_history:
    if role == "user":
        st.chat_message("user").write(message)
    else:
        st.chat_message("assistant").write(message)

# Chat input (IMPORTANT)
user_input = st.chat_input("Ask a question about your data...")

if user_input:
    if "file_path" not in st.session_state:
        st.warning("Please upload and analyze a dataset first")
    else:
        # Add user message
        st.session_state.chat_history.append(("user", user_input))

        with st.spinner("Thinking..."):
            response = requests.post(
                f"{API_URL}/api/query",
                json={
                    "file_path": st.session_state["file_path"],
                    "question": user_input
                }
            )

            if response.status_code == 200:
                answer = response.json()["answer"]
            else:
                answer = "Error processing request"

        # Add AI response
        st.session_state.chat_history.append(("assistant", answer))

        # Rerun to update UI
        st.rerun()