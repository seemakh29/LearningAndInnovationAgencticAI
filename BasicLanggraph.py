from typing import List,Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph import END, StateGraph
from langgrapgh_chains import generative_chain,reflection_chain
from IPython.display import Image, display

load_dotenv()

graph = StateGraph(state_schema= list)

REFLECT = "reflect"
GENERATE = "generate"

def generate_node(state):  #lIST OF ALL MESSAGES
    """Node to generate a tweet based on the current state. Appends all before messages  and add to new state"""
    new_message =  generative_chain.invoke({"messages": state })
    return state + [new_message]



def reflection_node(state):
    new_message =  reflection_chain.invoke({"messages": state })
    return state + [new_message]

graph.add_node(GENERATE, generate_node)
graph.add_node(REFLECT, reflection_node)

graph.set_entry_point(GENERATE)

def should_continue(state):
    return len(state) >4

graph.add_conditional_edges(GENERATE, should_continue,{True : END, False: REFLECT} )
graph.add_edge(REFLECT,GENERATE)

app = graph.compile()

print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()
display(Image(app.get_graph().draw_mermaid_png()))

#append the new human message to exixting  state system message

response = app.invoke([HumanMessage(content="AI agent taking over content creation")])

print(response)
