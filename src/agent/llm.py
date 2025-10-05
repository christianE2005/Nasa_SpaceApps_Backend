from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.core.settings import Settings

settings = Settings()


class LLM:
    """Encapsula la instancia del modelo y la generación de prompts urbanos."""

    SYSTEM_URBAN_PLANNER = """Eres un urbanista senior.
    Dispones de modelos de ML (infraestructura y desigualdad) y datos espaciales.
    Tu objetivo: generar recomendaciones urbanas accionables, medibles y equitativas por zona.
    Sé conciso y fundamenta cada decisión en datos o métricas cuando sea posible.
    """

    @staticmethod
    def instance_llm():
        """Crea una instancia configurada del modelo Gemini."""
        return ChatGoogleGenerativeAI(
            model=settings.llm_model,
            temperature=settings.llm_temperature or 0.2,
            max_output_tokens=settings.llm_max_tokens,
            timeout=settings.llm_timeout,
            max_retries=settings.llm_max_retries,
            google_api_key=settings.google_gemini_api_key,
        )

    @staticmethod
    def prompt_template():
        """Crea la plantilla de prompt base del urbanista."""
        return ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(LLM.SYSTEM_URBAN_PLANNER),
            ("human", "{question}")
        ])

    @staticmethod
    def planner_chain():
        """Construye una cadena lista para generar respuestas de planeación urbana."""
        llm = LLM.instance_llm()
        prompt = LLM.prompt_template()
        return prompt | llm | StrOutputParser()

    @staticmethod
    def build_question(model_outputs: dict, filters: dict, objectives: list[str]) -> str:
        """Genera la pregunta contextual que se envía al modelo."""
        return (
            "Genera 5 acciones urbanas priorizadas con KPIs, riesgos y trade-offs.\n"
            f"Objetivos: {', '.join(objectives) or 'generales'}\n"
            f"Filtros: {filters}\n"
            f"Resultados de modelos por zona: {model_outputs}\n"
            "Formato: bullets con KPI esperado y horizonte temporal.\n"
        )
