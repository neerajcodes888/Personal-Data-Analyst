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

def visualize_data(data, visualization_type):
    # Convert list to DataFrame if necessary
    if isinstance(data, list):
        data = pd.DataFrame(data)

    if visualization_type == "Line Chart":
        fig = px.line(data, x=data.columns[0], y=data.columns[1])
    elif visualization_type == "Bar Chart":
        fig = px.bar(data, x=data.columns[0], y=data.columns[1])
    elif visualization_type == "Scatter Plot":
        fig = px.scatter(data, x=data.columns[0], y=data.columns[1])
    else:
        fig = None
    return fig

def main():
    # Configure Streamlit page
    st.set_page_config(page_title="Ask your CSV")
    st.header("Ask your CSV")

    # Allow the user to upload a CSV file
    file = st.file_uploader("Upload File", type=["csv", "xls", "xlsx"])
    visualization_type = st.selectbox("Select Visualization Type", ["Line Chart", "Bar Chart", "Scatter Plot"])

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

                # Load the CSV data for visualization
                csv_loader = CSVLoader(file_path=f.name, encoding="utf-8", csv_args={"delimiter": ","})
                data = csv_loader.load()

                # Visualize the data based on the user's selection
                if data is not None:
                    fig = visualize_data(data, visualization_type)
                    if fig:
                        # Save plot as image
                        image_path = "plot_image.png"
                        fig.write_image(image_path)

                        # Display the saved image
                        st.image(image_path)

if __name__ == "__main__":
    main()
