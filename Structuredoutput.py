from llm_commons.proxy.base import get_proxy_client
from llm_commons.langchain.proxy import ChatOpenAI


proxy_client = get_proxy_client()

chat = ChatOpenAI(proxy_model_name='gpt-4o', proxy_client=proxy_client)

json_schema = {
    "title": "joke",
    "description": "Information about SAP Concur.",
    "type": "object",
    "properties": {
        "setup": {
            "type": "string",
            "description": "The setup of the  Company",
        },
        "punchline": {
            "type": "string",
            "description": "The punchline to the Company",
        },
        "rating": {
            "type": "integer",
            "description": "How great is the company, from 1 to 10",
            "default": None,
        },
    },
    "required": ["setup", "punchline", "rating"],
}
structured_llm = chat.with_structured_output(json_schema)

print(structured_llm.invoke("Describe about SAP Concur "))
