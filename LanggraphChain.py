#Use of chains in langgrapgh and how are we using it in basic.py file. Generate Node is a twitter  techie influencer assistent tasked with writing excellent twitter posts.  Reflection Node : You are a viral twitter  grading a tweet. Generate critique and recommendations for user's tweet. how are we calling Agents and askingto generate twitter tweets and also recommendations on the same tweet.

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from llm_commons.proxy.base import get_proxy_client
from llm_commons.langchain.proxy import ChatOpenAI


proxy_client = get_proxy_client()
 
chat = ChatOpenAI(proxy_model_name='gpt-4o', proxy_client=proxy_client)

generative_prompt = ChatPromptTemplate.from_messages(
    [
       ( 
        "system", 
        "You are a twitter techie influencer assistent tasked with writing excellent twitter posts."
        "If the user provides critique, respond with a revised version of your previous attempts.",
       ),
       MessagesPlaceholder(variable_name="messages"),

    ]
)

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a viral twitter  grading a tweet. Generate critique and recommendations for user's tweet."
            "Always provide detailed recommendations, including requests for length, virality, style, etc."
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

generative_chain =  generative_prompt | chat
reflection_chain = reflection_prompt | chat
