import streamlit as st
import pandas as pd
import plotly.express as px
from langchain.document_loaders.csv_loader import CSVLoader
import tempfile
import os
import google.generativeai as genai
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def main():
    # Configure Streamlit page
    st.set_page_config(page_title="Ask your CSV")
    st.header("Ask your CSV")

    # Allow the user to upload a file
    file = st.file_uploader("Upload File", type=["csv", "xls", "xlsx"])

    if file is not None:
        # Create a temporary file to store the uploaded data
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".csv", delete=False) as f:
            # Write the uploaded file content to the temporary file
            f.write(file.getvalue())
            f.flush()

            model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.8)

            # Ask the user to input a question
            user_input = st.text_input("Question here:")

            # Create a CSV agent using the OpenAI language model and the temporary file
            agent = create_csv_agent(model, f.name, verbose=True)

            if user_input:
                # Run the agent on the user's question and get the response
                response = agent.run(user_input)
                st.write(response)

                try:
                    # Attempt to load the data directly using Pandas
                    data = pd.read_csv(f.name)
                except UnicodeDecodeError:
                    try:
                        # Try loading as an Excel file
                        data = pd.read_excel(f.name)
                    except Exception as e:
                        st.error(f"Error loading file: {e}")


if __name__ == "__main__":
    main()
