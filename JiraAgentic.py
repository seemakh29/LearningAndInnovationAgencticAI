import csv
from datetime import datetime, timezone
from  dotenv import load_dotenv, find_dotenv
_ = load_dotenv()
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
# from langgraph.graph import StateGraph, END,  START
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
import operator
from llm_commons.langchain.proxy import ChatOpenAI
from IPython.display import Image, display
# from langchain_core.tools import tool
# from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
import requests
import json
import os
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.agents import AgentExecutor, Tool, create_react_agent
from llm_commons.proxy.base import get_proxy_client
from langchain.prompts import PromptTemplate
from langchain.agents import tool
import pandas as pd
import glob

proxy_client = get_proxy_client()
 
chat = ChatOpenAI(proxy_model_name='gpt-4o', proxy_client=proxy_client)
jiratoken = "OTAwMjk4MzE4MTAxOkgnkt/+bs2rP+hKyjirRJv7KFcg"

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class Agent:
    def __init__(self, model, system= "", messages=[]):
        self.model = model
        self.system = system  # Saving system message
        self.messages = messages
 
    
    def get_issues_from_status(self) -> str:
        try:
       # Combine the system message with the existing state messages
           
            headers = {
                "Authorization": f"Bearer {jiratoken}",
                "Content-Type": "application/json"
            }
            projectKey = 'ISBNPAY'
            status = 'Blocked'
            parameters = {'jql': f"project = '{projectKey}' AND issuetype = 'Task'"}

            response = requests.get(
                f'https://jira.concur.com//rest/api/2/search',
                headers=headers, params=parameters
            )
            formatted_issues_list = [] 
            for issue in response.json()["issues"]:
                my_dict = {'key': issue['key'], 'status': issue['fields']['status']['name']}
                formatted_issues_list.append(my_dict)
                formatted_issues = json.dumps(formatted_issues_list)
            
            prompt = f"Print all issues with issue key and status for issues with closed status only from received response from JIRA API:\n {formatted_issues}"

            message = [HumanMessage(content= prompt)]


            # print(f"Formatted Issues: {formatted_issues}")
# Define the state
            # state = {"messages": [HumanMessage(content="Give me the list  of all issues with status Closed from this formatted_issues:\n " + formatted_issues)]}
             # Invoke the model with the prepared message
            response1 = self.model.invoke(message)
            print (response1)
            for issue in response.json()["issues"]:
                print ("Hello")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def createCsvFile(self, file, folderpath):
            # file_path = os.path.join(folderpath,f'project_{file}.csv')
            # print(file_path)
            # Ensure that the directory exists
            try:
                if not os.path.exists(folderpath):
                    os.makedirs(folderpath)
                file_path = os.path.join(folderpath,f'project_{file}.csv')
                data_file = open(file_path, 'w+', newline='')
                csv_handler = csv.writer(data_file)
                # fileList.append(f'csv_files/project_{file}.csv')
                    # fileList.append(f'project_{file}.csv')
                print(f"CSV file '{file_path}' creating in '{folderpath}'")
                return csv_handler
            except FileNotFoundError:
                return "Error: File 'example.csv' not found.", 404

            except Exception as e:
                return f"An error occurred: {str(e)}", 500  # Handle other potential errors
            
    def createCSV(self, projectKey):
        if len(projectKey) != 0:
            #delete all files in csv_files folder
            for fileName in os.listdir("csv_files"):
                filePath = os.path.join("csv_files", fileName)
                try:
                    if os.path.isfile(filePath):
                        os.unlink(filePath)
                except Exception as e:
                    print(f"Error deleting file {filePath}: {e}")

            folderpath = "csv_files"
            csv_writer = self.createCsvFile(0, folderpath)
            count = 0
            csvRow = {}
            batch_size = 2000
            jql_query = f"project={projectKey}"
            params = {"jql": jql_query}
            # query1 = {
            # 'jql': 'project = ISBNPAY'}
        headers = {
            "Authorization":  f"Bearer {jiratoken}",
            "Content-Type": "application/json"
        }
        #get total count
        jiraResponse = requests.get(f'https://jira.concur.com//rest/api/2/search',
                                headers=headers, params= params)
        
        data = jiraResponse.json()
        totalIssues = data["total"]
        nor = (totalIssues+ batch_size-1)//batch_size #3
        maxResults = 0
        counter = 0
        for n in range(nor):
            s = n*batch_size
            query = {
                'jql': jql_query, "startAt": s,"maxResults": batch_size, "fields": 'key,summary,status,customfield_10572,created,customfield_11002,issuetype'}

            response = requests.get(f'https://jira.concur.com//rest/api/2/search',
                                    headers=headers, params= query)
        
            for issue in response.json()["issues"]:
                if (issue["fields"]["issuetype"]["name"]!= "Vulnerability") and (issue["fields"]["customfield_11002"] is not None):
                    csvRow["key"] = issue["key"]
                    csvRow["summary"] = issue["fields"]["summary"]
                    csvRow["Status"] = issue["fields"]["status"]["name"]
                    csvRow["StoryPoints"] = issue["fields"]["customfield_10572"]
                    csvRow["created"] = issue["fields"]["created"]
                    if issue["fields"]["customfield_11002"] is not None:
                        sprintArray = {}
                        sprintDict = {}
                        rawSprintData = issue["fields"]["customfield_11002"][-1]
                        
                        sprintArray = rawSprintData.split(',')[3:6]
                        for item in sprintArray:
                            if item is not None:
                                sprintDict[item.split("=")[0]] = item.split("=")[1]
                        csvRow["Sprint"] = sprintDict["name"]
                        # start_date = pd.to_datetime(sprintDict["startDate"])
                        # end_date = pd.to_datetime(sprintDict["endDate"])
                        csvRow["Sprint Start Date"] = sprintDict["startDate"]
                        csvRow["Sprint Completed Date"] = sprintDict["endDate"]    
                        if(sprintDict["name"] == "Feature Back Log"):
                            csvRow["Sprint Start Date"] = "2023-11-21T09:58:00.000Z"
                            csvRow["Sprint Completed Date"] = "2023-11-21T09:58:00.000Z"
                
                    csvRow["Issue-Type"] = issue["fields"]["issuetype"]["name"]    
                    csvRow["Comment"] = ""
                    if (issue["fields"]["status"]["name"] == 'Blocked'):
                        if self.get_issue_comment(issue["key"]).json()["issues"][0]["fields"]["comment"]["comments"]:
                            csvRow["Comment"] = self.get_issue_comment(issue["key"]).json()["issues"][0]["fields"]["comment"]["comments"][-1]["body"]
                    if count == 0:
                        csv_writer.writerow(csvRow.keys())
                        count =1
                    csv_writer.writerow(csvRow.values())
                    maxResults = maxResults + 1
                    if maxResults>900:
                        counter = counter + 1
                        csv_writer = self.createCsvFile(counter,folderpath)
                        maxResults = 0
                        count = 0
            self.call_agent()

    def call_agent(self):
        fileList = []
        for fileName in os.listdir("csv_files"):
               # Construct the full path to the file
            fileList.append(os.path.join("csv_files", fileName))
        print("CSV files created successfully!")
        print(fileList)
        

agent = Agent(model=chat, system= """Your name is Jira AI-Powered Assistant if anyone asks what is your name you should reply Hi I am Jira AI-Powered Assistant and nothing else.
              If you are asked to get the last 'N' sprints, combine all the data frames and then sort sprints based on  descending order of Sprint Start Date column and give the data regarding the last 'N' sprints, donot give data for each data frame
                        
If you are asked on a sprint velocity then combine all the data frames and then give sprint velocity on that particular sprint. """)


response = agent.call_agent()

custom_prompt = PromptTemplate(
    input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
    template="""
Example session:

Question: Calculate the sprint velocity for the last 3 sprints using the provided CSV files.
Thought: I should use the calculate_sprint_velocity tool.
Action: calculate_sprint_velocity
Action Input: csv_files/project_0.csv, csv_files/project_1.csv, csv_files/project_2.csv, csv_files/project_3.csv


Question: Give me the list of ageing tickets using the provided CSV files.
Thought: I should use the ageing_tickets tool.
Action: ageing_tickets
Action Input: csv_files/project_0.csv, csv_files/project_1.csv, csv_files/project_2.csv, csv_files/project_3.csv

Observation: [tool output here]

Answer: [final answer here]

Question: Give me the list of closed tickets or  If your asked to  List down top 3 aging tickets with days not having status as "Closed", ageing means the number of days since the ticket was Created
Thought: I can answer this by reasoning over the file_paths provided  without using a tool.
Answer: [final answer here]


You can use the function combined_dataframe(filepath: str) to combine the CSV files into a single DataFrame and read the content inside CSV files.
Tools available: {tools}
Tool names: {tool_names}

Question: {input}
{agent_scratchpad}
"""
)




def combined_dataframe(filepath: str):
    file_list = [f.strip() for f in filepath.split(",")]
    valid_files = [f for f in file_list if os.path.exists(f)]
    if not valid_files:
        return "No valid CSV files found in input."
    df_list = [pd.read_csv(f) for f in valid_files]
    combined_df = pd.concat(df_list, ignore_index=True)
    # ... your logic ...
    return combined_df

@tool()
def calculate_sprint_velocity(filepath: str):
    """ If you are asked on a sprint velocity for a particular Sprint,
        then filter that particular Sprint on Status as Closed.
        If you are asked to get the last 3 sprints, then sort sprints based on descending order of Sprint Start Date column """

    file_list = [f.strip() for f in filepath.split(",")]
    valid_files = [f for f in file_list if os.path.exists(f)]
    if not valid_files:
        return "No valid CSV files found in input."
    df_list = [pd.read_csv(f) for f in valid_files]
    combined_df = pd.concat(df_list, ignore_index=True)

    # Ensure 'Sprint Start Date' is datetime
    combined_df['Sprint Start Date'] = pd.to_datetime(combined_df['Sprint Start Date'], errors='coerce')

    # Sort by Sprint Start Date descending
    sorted_df = combined_df.sort_values(by='Sprint Start Date', ascending=False)

    # Get the top 3 most recent sprints
    top_3_sprints = sorted_df['Sprint'].dropna().unique()[:3]

    # Calculate velocity for each sprint
    velocity_dict = {}
    for sprint in top_3_sprints:
        sprint_data = sorted_df[(sorted_df['Sprint'] == sprint) & (sorted_df['Status'] == 'Closed')]
        velocity = sprint_data['StoryPoints'].sum()
        velocity_dict[sprint] = velocity

    return velocity_dict
   

@tool()
def ageing_tickets(filepath: str):
    """ If your asked to  List down top 10 aging tickets with days not having status as "Closed", ageing means the number of days since the ticket was Created """

    file_list = [f.strip() for f in filepath.split(",")]
    valid_files = [f for f in file_list if os.path.exists(f)]
    if not valid_files:
        return "No valid CSV files found in input."
    df_list = [pd.read_csv(f) for f in valid_files]
    df = pd.concat(df_list, ignore_index=True)


    # Ensure the 'Created Date' column is in datetime format
    df['created'] = pd.to_datetime(df['created'])

    # Filter tickets that are not closed
    non_closed_tickets = df[df['Status'] != 'Closed']

    # Calculate the age of each ticket
    current_date = datetime.now(timezone.utc)
    non_closed_tickets['Age'] = (current_date - non_closed_tickets['created']).dt.days

    # Sort tickets by age
    sorted_tickets = non_closed_tickets.sort_values(by='Age', ascending=False)

    # List the top 3 aging tickets
    top_3_aging_tickets = sorted_tickets.head(10)
    return top_3_aging_tickets[['key', 'Age']]

tools = [calculate_sprint_velocity, ageing_tickets]

    # Get all CSV file paths
csv_files = glob.glob("csv_files/*.csv")

combined_result = combined_dataframe(','.join(csv_files))



agent = create_react_agent(llm = chat, tools = tools, prompt= custom_prompt)
# agent = create_pandas_dataframe_agent(llm = chat, df= combined_result, agent_type="tool-calling",
#     verbose=True, allow_dangerous_code=True, extra_tools= tools, return_intermediate_steps=True)



agent_executor = AgentExecutor(agent=agent, tools= tools, verbose=True, handle_parsing_errors=True)

result = agent_executor.invoke({"input": 
                                "Give me the list of ageing tickets",
})

# result = agent.invoke({"input": "Calculate the sprint velocity for the last 3 sprints"})


print(result['output'])
