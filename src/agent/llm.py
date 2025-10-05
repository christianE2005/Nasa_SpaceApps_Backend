from langchain_google_genai import ChatGoogleGenerativeAI
from src.core.settings import Settings

settings = Settings()

class LLM:
    @staticmethod
    def instance_llm():
        llm = ChatGoogleGenerativeAI(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            max_output_tokens=settings.llm_max_tokens,  
            timeout=settings.llm_timeout,                
            max_retries=settings.llm_max_retries,
            google_api_key=settings.google_gemini_api_key
        )
        return llm
