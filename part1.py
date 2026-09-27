import langchain
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

load_dotenv()
os.environ["GROQ_API_KEY"]= os.getenv("GROQ_API_KEY")

model= ChatGroq(model="openai/gpt-oss-20b")

class TasksOwners(BaseModel):
    task:str= Field(description="what is the task that has to be performed?")
    owner:str= Field(description="Who is the person responsible for the task")
    deadline:str= Field(description="Task needs to be done by which day or date")
    status:str= Field(description="Whether the task has been already completed or pending or delayed ")
    confidence:float= Field(description="How much confidence does LLM have on the specific details of a single task given by it, must be between 0 and 1 , 0 being not confident at all , and 1 being fully confident")


# class Tasks(BaseModel):
#     task:str= Field(description="Task discussed in the meeting which is need to be done")
#     deadline:str= Field(description="Task needs to be done by which day or date")

# class OwnersWTasks(BaseModel):
#     person:str= Field(description="person who who has been assigned a task in the meeting")
#     tasks:list[Tasks]= Field(description="the list of all the tasks that has been been assigned to a particular person with deadlines of each")
#     status:str= Field(description="Whether the task has been already completed or pending or delayed ")
#     confidence:str= Field(description="How much confidence does LLM have on the specified details by")

# class People(BaseModel):
#     person:str= Field(description="person who is present in the meeting")


class Action_items(BaseModel):
    tasks:list[TasksOwners]= Field(description="it is a list of all the tasks ,their owners, deadlines , status and confidence of LLM on them")

new_model=model.with_structured_output(Action_items)

transcript=input("Paste your meeting transcripts:  ")

response2= new_model.invoke(transcript)

print(response2)