from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate


def generate_explanation(ml_results):
    prompt = PromptTemplate(
        input_variables=["ml_results"],
        template="""
        You are a data analyst.

        Explain the following ML results clearly:

        {ml_results}
        """
    )

    llm = ChatOllama(model="llama3")

    chain = prompt | llm

    response = chain.invoke({"ml_results": str(ml_results)})

    return response.content