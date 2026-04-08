import os
from typing import TypedDict
from langgraph.graph import StateGraph, END, START
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from pydantic import BaseModel, Field
from dotenv import load_dotenv




def get_llm():
    """
    Initialize the LLM with API key from environment variable.
    Returns:
        An instance of ChatOpenAI."""
    
    load_dotenv()  # Load environment variables from .env file
    llm = ChatOpenAI(
        model=os.getenv("MODEL"),
        temperature=0
    )
    return llm

#=============================================================================
# Define the State for the graph
#=============================================================================
class TicketState(TypedDict):
    text: str
    category: str
    priority: str
    summary: str
    resolution: str

class TicketAnalysis(BaseModel):
    category: str = Field(description="Ticket category")
    priority: str = Field(description="Ticket priority")
    summary: str = Field(description="Short summary")
    resolution: str = Field(description="Suggested resolution")    


#=============================================================================
# Define the Prompt     
#=============================================================================
SYSTEM_MESSAGE = """You are an IT service desk assistant."""
USER_PROMPT = """
    ### Analyze the following ticket and return:

    1. Category (🛜 Network, 🫧 Software, 💽 Hardware, 👤 Access, 📧 Email, 🔑 Security, Other)
    2. Priority (🟢 Low, 🔵 Medium, 🟠 High, 🔴 Critical)
    3. Short Summary
    4. Suggested Resolution

    ### Ticket:
    {ticket_description}
    

    {format_instructions}

"""

#=============================================================================
# LLM Node
#=============================================================================
def analyze_ticket_node(state: TicketState) -> TicketState:

    
    llm = get_llm()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_MESSAGE),
        ("human", USER_PROMPT)
    ])

    parser = PydanticOutputParser(pydantic_object=TicketAnalysis)

    chain = prompt_template | llm | parser


    response = chain.invoke({
        "ticket_description": state['text'],
        "format_instructions": parser.get_format_instructions()
    })

    return {
            **state,
            "category": response.category,
            "priority": response.priority,
            "summary": response.summary,
            "resolution": response.resolution,
        }

#=============================================================================
# Build Graph for Incidenty Analysis
#=============================================================================
def get_incident_analysis_graph():
    graph = StateGraph(TicketState)

    # Add the main node to analyze the ticket
    graph.add_node("analyze", analyze_ticket_node)

    graph.add_edge(START, "analyze")
    graph.add_edge("analyze", END)

    app = graph.compile()

    return app



def get_incident_analysis_result(text: str):
    app = get_incident_analysis_graph()
    result = app.invoke({
        "text": text,
        "category": "",
        "priority": "",
        "summary": "",
        "resolution": ""
    })
    return result