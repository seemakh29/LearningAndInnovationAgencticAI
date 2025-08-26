Setup LLM in local:
1. https://github.tools.sap/AI-Playground-Projects/llm-commons?tab=readme-ov-file

For connecting to LLM :
from llm_commons.proxy.base import set_proxy_version
set_proxy_version('gen-ai-hub') #
from llm_commons.langchain.proxy import ChatOpenAI
 
To be added in new directory called .btp_llm as config.json
llm = ChatOpenAI(proxy_model_name='gpt-4-32k')
prompt = PromptTemplate.from_template("Summarize the following file content:\n\n{content}")
summarizer = LLMChain(llm=llm, prompt=prompt)

{
    "BTP_LLM_AUTH_URL": "https://shared-ai-core-service-w2r9b71q.authentication.eu12.hana.ondemand.com",
    "BTP_LLM_CLIENT_ID": "sb-4717407f-69b4-4d41-9a32-205c8ebf82e5!b268558|xsuaa_std!b318061",
    "BTP_LLM_CLIENT_SECRET": "1a49d4f7-3e33-4f0e-939a-55860b766d30$6m_PZu9sSGXtuVQi9PIrFZxYorXE-Gf_C3Fs7TnFDGI=",
    "BTP_LLM_API_BASE": "https://api.ai.intprod-eu12.eu-central-1.aws.ml.hana.ondemand.com"
}

Register llm model before using it :
Model has been retired. Please follow the instructions at https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/update-deployment to update your deployment with a new model.'}
AI-LEARNING Portal : https://sap.sharepoint.com/sites/126802/SitePages/AI-Learning.aspx
https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/create-deployment-for-generative-ai-model-in-sap-ai-core


Basiclanggrapgh.py output : This code is just a basic langgrapgh code to understand why to use langgrapgh,  how is it different from langchain. Why do a agent need a Grapgh like structure? What are the components used in langgrapgh

Components in Langgraph:

LangGraph : Nodes, Edges, Condition Edges
 nodes : Agent / Function
Edges - > connect nodes
Condition edges : decision


Node is an agent/function.
Edges : edges connect this node.
Condition edges : required to make decisions.
State: 
Agent state : state is tracked always

Output :
<img width="2354" height="1508" alt="image" src="https://github.com/user-attachments/assets/507099dc-6e82-4025-bbe2-092a15ef9cc8" />



React_agent.ipynb

<img width="1091" height="662" alt="image" src="https://github.com/user-attachments/assets/2e759556-2521-43a4-b803-7dd41846c02e" />




