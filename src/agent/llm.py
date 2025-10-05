from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from src.core.settings import Settings

settings = Settings()

llm = ChatGoogleGenerativeAI(
    model=settings.llm_model,
    temperature=settings.llm_temperature,
    max_output_tokens=settings.llm_max_tokens,
    timeout=settings.llm_timeout,
    max_retries=settings.max_retries,
    google_api_key=settings.google_api_key 
)

response = llm.invoke([HumanMessage(content="Hola, ¿cómo estás?")])

print(response.content)
