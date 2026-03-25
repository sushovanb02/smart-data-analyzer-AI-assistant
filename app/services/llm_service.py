from langchain_classic.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from app.services.llm_client import get_llm

memory = ConversationBufferMemory(return_messages=True)

def generate_explanation(ml_results):
    history = memory.load_memory_variables({}).get("history", "")

    prompt = ChatPromptTemplate.from_messages([
        (
            "system", 
            """
            You are an expert data analyst. Your job is to explain machine learning results clearly and concisely to non-technical stakeholders.
            Use past conversation context if available.

            Conversation history:
            {history}
            """
        ),
        (
            "human", 
            "Please explain the following ML results:\n\n{ml_results}"
        )
    ])

    llm = get_llm()

    chain = prompt | llm

    response = chain.invoke({
            "ml_results": str(ml_results),
            "history": history
        })
    
    memory.save_context(
        {"input": str(ml_results)},
        {"output": response.content}
    )

    return response.content