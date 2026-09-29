import langchain
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from langchain.messages import SystemMessage, HumanMessage
from system_prompts import systm_prompt1 , systm_prompt2
import streamlit as st
import pandas as pd
from cleaner import clean_transcripts
from validator import validate_action_items
from evaluation_data import (SAMPLE_TRANSCRIPTS,EVALUATION_DATA)
from evaluator import evaluate_action_items

load_dotenv()
os.environ["GEMINI_API_KEY2"]= os.getenv("GEMINI_API_KEY2")

model= ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

class TasksOwners(BaseModel):
    task:str= Field(description="what is the task that has to be performed?")
    owner:str|None= Field(description="Who is the person responsible for the task")
    deadline:str|None= Field(description="Task needs to be done by which day or date")
    status:str= Field(description="Whether the task has been already completed or pending or delayed ")
    confidence:float= Field(description="How much confidence does LLM have on the specific details of a single task given by it, must be between 0 and 1 , 0 being not confident at all , and 1 being fully confident")

class Action_items(BaseModel):
    tasks:list[TasksOwners]= Field(description="it is a list of all the tasks ,their owners, deadlines , status and confidence of LLM on them")

new_model=model.with_structured_output(Action_items)
validation_model = model.with_structured_output(Action_items)


st.title("Welcome to AI Meeting Action Item Extractor!!")
st.subheader("Paste your transcripts below.")
transcript=st.text_area("Type here: ")
if st.button("Go", type="primary"):

    if not transcript.strip():
        st.warning("Please enter a meeting transcript first.")

    else:
        with st.spinner("Cleaning transcript..."):
            cleaned_transcript = clean_transcripts(transcript)

        if cleaned_transcript == transcript.strip():
            st.success("Transcript is already clean.")

        else:
            st.success("Transcript cleaned successfully.")

        with st.expander("View cleaned transcript"):
            st.text(cleaned_transcript)

        with st.spinner("Extracting action items...\n\nHang on, it may take a little while..."):

            messages = [
                SystemMessage(systm_prompt1),
                HumanMessage(cleaned_transcript)
            ]

            response2 = new_model.invoke(messages)

        st.success("Action items extracted successfully!")

        validation_issues = validate_action_items(response2)

        if validation_issues:

            with st.expander("Validation checks"):
                for issue in validation_issues:
                    st.warning(issue)

        else:
            st.success("Rule-based validation passed.")

        with st.spinner(
            "Verifying and refining action items...\n\n"
            "Hang on, it may take a little while..."
        ):

            validation_input = f"""
ORIGINAL MEETING TRANSCRIPT:

{cleaned_transcript}


EXTRACTED ACTION ITEMS:

{response2.model_dump_json(indent=2)}


RULE-BASED VALIDATION FINDINGS:

{validation_issues}
"""

            validation_messages = [
                SystemMessage(systm_prompt2),
                HumanMessage(validation_input)
            ]

            final_response = validation_model.invoke(validation_messages)


        st.success("Action items verified successfully!")

        data = [
            {
                "Task": task.task,
                "Owner": task.owner,
                "Deadline": task.deadline,
                "Status": task.status,
                "Confidence": task.confidence
            }

            for task in final_response.tasks
        ]

        df = pd.DataFrame(data)
        st.subheader("Final Action Items")
        st.dataframe(df,width="stretch",)

