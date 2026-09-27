import langchain
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from langchain.messages import SystemMessage, HumanMessage
from system_prompts import systm_prompt

load_dotenv()
os.environ["GEMINI_API_KEY"]= os.getenv("GEMINI_API_KEY")

model= ChatGoogleGenerativeAI(model="gemini-3.8-flash")

class TasksOwners(BaseModel):
    task:str= Field(description="what is the task that has to be performed?")
    owner:str|None= Field(description="Who is the person responsible for the task")
    deadline:str|None= Field(description="Task needs to be done by which day or date")
    status:str= Field(description="Whether the task has been already completed or pending or delayed ")
    confidence:float= Field(description="How much confidence does LLM have on the specific details of a single task given by it, must be between 0 and 1 , 0 being not confident at all , and 1 being fully confident")

class Action_items(BaseModel):
    tasks:list[TasksOwners]= Field(description="it is a list of all the tasks ,their owners, deadlines , status and confidence of LLM on them")

new_model=model.with_structured_output(Action_items)

transcript=input("Paste your meeting transcripts:  ")

messages= [
    SystemMessage(systm_prompt),
    HumanMessage(transcript)
]

response2= new_model.invoke(messages)

print(response2)