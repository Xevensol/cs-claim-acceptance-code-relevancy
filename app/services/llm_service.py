from langchain_openai import ChatOpenAI
from app.core.config import settings

OPENAI_API_KEY = settings.OPENAI_API_KEY

def get_openai_model(model):
    try:
        llm = ChatOpenAI(model=model, temperature=0, openai_api_key=OPENAI_API_KEY)
        return llm
    except Exception as e:
        raise Exception(f"Error initializing OpenAI model: {e}")


def get_chain(prompt, parser):
    try:
        llm = get_openai_model(model=settings.OPENAI_MODEL_NAME)
        chain = prompt | llm | parser
        return chain
    except Exception as e:
        raise Exception(f"Error creating chain: {e}")

