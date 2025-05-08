from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
import streamlit as st
from pydantic import BaseModel

load_dotenv()

class Settings(BaseSettings):
    """
    This Settings class is designed to load and manage environment variables for an
    application using Pydantic's BaseSettings and python-dotenv

    write all your env variables here so you can access them easily.

    """

    MSSQL_SERVER:str = os.environ.get("MSSQL_SERVER")
    MSSQL_DATABASE:str = os.environ.get("MSSQL_DATABASE")
    MSSQL_USER : str = os.environ.get("MSSQL_USER")
    MSSQL_PASSWORD : str = os.environ.get("MSSQL_PASSWORD")
    MSQL_DRIVERS: list = ['{SQL Server}', '{ODBC Driver 17 for SQL Server}']    
    OPENAI_API_KEY : str = os.environ.get("OPENAI_API_KEY")
    OPENAI_MODEL_NAME : str = "gpt-4o-mini"

    class Config:
        env_file = ".env"


# class Settings(BaseModel):
#     """
#     This Settings class is designed to load and manage configuration variables
#     from Streamlit Cloud's st.secrets.
#     """

#     # Define your environment variables
#     MSSQL_SERVER: str = st.secrets["MSSQL_SERVER"]
#     MSSQL_DATABASE: str = st.secrets["MSSQL_DATABASE"]
#     MSSQL_USER: str = st.secrets["MSSQL_USER"]
#     MSSQL_PASSWORD: str = st.secrets["MSSQL_PASSWORD"]
#     OPENAI_API_KEY: str = st.secrets["OPENAI_API_KEY"]

# Create an instance of the settings
settings = Settings()