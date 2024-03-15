import streamlit as st
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
# def main():
#     st.title("Chat with CSV using Gemini Pro")

#     # File Uploader
#     uploaded_file = st.sidebar.file_uploader("Choose your CSV file", type="csv")

#     if uploaded_file:
#         temp_dir = tempfile.mkdtemp()
#         path = os.path.join(temp_dir, uploaded_file.name)
#         with open(path, "wb") as f:
#             f.write(uploaded_file.getvalue())

#     # Using temp_file for getting the file path as CSVLoader only accepts file path
#     if uploaded_file is not None:
#         with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
#             tmp_file.write(uploaded_file.getvalue())
#             tmp_file_path = tmp_file.name

#             csv_loader = CSVLoader(
#                 file_path=tmp_file_path, encoding="utf-8", csv_args={"delimiter": ","}
#             )

#             # Loading the data from the CSV file
#             data = csv_loader.load()

#             user_input = st.text_input("Start Chatting...")

#             if user_input:
#                 response = get_model_response(data, user_input)
#                 st.write(response)


def main():
    # Configure Streamlit page
    st.set_page_config(page_title="Ask your CSV")
    st.header("Ask your CSV")

    # Allow the user to upload a CSV file
    file = st.file_uploader("Upload File", type=["csv", "xls", "xlsx"])
    

    if file is not None:
        # Create a temporary file to store the uploaded CSV data
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".csv", delete=False) as f:
            # Convert bytes to a string before writing to the file
            data_str = file.getvalue().decode("utf-8")
            f.write(data_str)
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


if __name__ == "__main__":
    main()