Agentic AI Jira output :

<img width="615" height="461" alt="image" src="https://github.com/user-attachments/assets/8fa87d32-d56a-43fe-a08c-f01d57a18c41" />

Why we are not going ahead with  open source langchain and lang graph model :
1. Earlier we have used CSV agent to read through CSV files and get required output. But problem with csv agent was as soon as jira tickets/ data was increasing we would get very inaccurate results. Reason being models can't handle large amount of data without being properly trained.
2. Using  langchain agents (any agent) it always gives an indefinite loop output. By which a user can never get a specified output to a given question.
3. Langchain as always meant to be an indefinite loop.

Langgraph:
1. Tried to create the jira assistant solution  with langgraph.
   -> Problems Noticed
   1. With langgrapgh with creating a State grapgh diagram, it is possible to build agentic solution for jira. But as in jira there  is always large amount of data we have to use tools ( which or similar to function) to get accurate results.
   2. Creating tools for most of the user question asked can help llm to understand better and get accurate output. But how many tools/functions will be create  as such?? As it's unpredictable what will be the user's prompt on Jira tickets.
   3. Langgrapgh needs to be used with langchain. as langgraph create a state grapgh which holds state of each node and possibly always give one  results not indefinite results as langchain.
   4. Langgraph is an REACT model. which does  the reasoning and thinking process as provided in prompts. It takes up three stages thought, action, process and then talk to llm.
   5. Also tried to move .csv data to chroma db but not supported all the time as it has a limit to use the database.
   6. The above uploaded jira agentic ai solution is created only using langchain for now. we can easily move to langgraph if needed.
  
   <img width="1146" height="513" alt="image" src="https://github.com/user-attachments/assets/54df61ba-d2d3-41e5-a219-09590f447a79" />

   BTP CREATE YOUR OWN tool ON BTP
   1. Finalized this approach as most the interface is already created and no need to do things from sctrach.
   2. Easy to connect to SAP HANA Database to store data received from JIRA API.
   3. using odata or open source API its easy process to connect to JIRA API.
   4. User interface is laready present in Agentic tool.
   5. 

   


