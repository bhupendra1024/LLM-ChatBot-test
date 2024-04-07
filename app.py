import os
import re
import streamlit as st

from typing import List

# Google sheets as DB

import pandas as pd
from streamlit_gsheets import GSheetsConnection


#############
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from langchain_core.pydantic_v1 import BaseModel, Field

from langchain_community.chat_models import ChatOpenAI
from decouple import config

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

class user_detail(BaseModel):
    annual_income: int = Field(description="take annual income from the user")
    marital_status: str = Field(description="take the marital status from user")


# os.environ['OPEN_API_KEY'] = ''
st.set_page_config(
  page_title="FinX",
  page_icon="🤖",
  layout="wide"
)




# Function to extract user information from the prompt
def extract_user_info(arg):
    user_info = {}

    print(user_info)
    # Extract annual income
    income_match = re.search(r'"Annual Income": (\d+)', arg, re.IGNORECASE)
    if income_match:
        user_info['Annual Income ₹'] = int(income_match.group(1))
  
    #Extracting Martal Status 
    # marital_status_match = re.search(r'Marital Status: (\w+)', arg, re.IGNORECASE)
    marital_status_match = re.search(r'"Marital Status": (\w+)', arg, re.IGNORECASE)
    if marital_status_match:
        user_info['Marital Status'] = marital_status_match.group(1)
    
    
    # Extract cost of living
    cost_of_living_match = re.search(r'"Cost of Living": (\d+)', arg, re.IGNORECASE)
    if cost_of_living_match:
        user_info['Cost of Living ₹'] = int(cost_of_living_match.group(1))
    
    # Extract age
    age_match = re.search(r'"Age": (\d+)', arg, re.IGNORECASE)
    if age_match:
        user_info['Age'] = int(age_match.group(1))

    return user_info


user_prompt = st.chat_input()


prompt1 = PromptTemplate(
  input_variables = ["chat_history", "human_input"],
  template="""You are a financial advisor to help user with budgeting plans. 
              Keep all of the currency in INR ₹
              Follow these steps 

              1. Ask user questions to Gather following information
                  a. Annual Income 
                  b. Marital Status 
                  c. Cost of living 
                  d. Age 

              
              2. If user has trouble figuring out cost of living ask general questions and give it a general amount yourself 

              3. Once you have received all of these information generate a budgeting plan for the next 5 years of this person for comfortable retirement plan by age 50 
              chat_history: {chat_history}
              Human: {human_input}


              AI:"""
)

parser = JsonOutputParser(pydantic_object=user_detail)
print(parser)
# for extracting user info
prompt2 = PromptTemplate(
  input_variables = ["chat_history", "human_input"],
  template="""You are a financial advisor to help user with budgeting plans. 
              Keep all of the currency in INR ₹
              Follow these steps 

              If user tries to give information about 
                  a. Annual Income 
                  b. Marital Status 
                  c. Cost of living 
                  d. age 

              all at once or step by step then just output a dictionry of each input and please make sure the money amount is all in numbers and the String starts with capital letter

              
                  Annual Income 
                  Marital Status 
                  Cost of living 
                  Age 


              update keys if user updates any 
            
              only reply with dictionary and nothing else 
              chat_history: {chat_history}
              Human: {human_input} 

              AI:""",
              # partial_variables={"format_instructions": parser.get_format_instructions()},
)

prompt3 = PromptTemplate(
    template='''You are a financial advisor to help user with budgeting plans. 
              Keep all of the currency in INR ₹
              Follow these steps 

              If user tries to give information about 
                  a. Annual Income 
                  b. Marital Status 
                  c. Cost of living 
                  d. age 

              all at once or step by step then just output a dictionry of each input and please make sure the money amount is all in numbers and the String starts with capital letter

              
                  Annual Income 
                  Marital Status 
                  Cost of living 
                  Age \n{format_instructions}\n{chat_history}\n''',
    input_variables=["chat_history"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)


llm = ChatOpenAI(openai_api_key = config("OPEN_API_KEY"),  temperature=0.6, model="gpt-4")  #model="gpt-4",


memory = ConversationBufferMemory(memory_key="chat_history", llm=llm)
llm_chain = LLMChain(
  llm=llm,
  memory=memory,
  prompt=prompt1,
)

## LLM chain 2 used in prompt2
memory2 = ConversationBufferMemory(memory_key="chat_history", llm=llm)
llm_chain_2  = LLMChain(
  llm=llm,
  memory=memory2,
  prompt=prompt2,
  
)




chain = prompt3 | llm | parser
print(type(chain))

chain.invoke({"chat_history" : user_detail})






hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


st.title("FinX")

if "messages" not in st.session_state.keys():
  st.session_state.messages = [
    {"role": "assistant", "content": "Hi I am your financial advisor, will you be willing to share a few details with me"}
  ]


for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.write(message["content"])


# user_prompt = st.chat_input()

if user_prompt is not None:
  st.session_state.messages.append({"role": "user", "content": user_prompt})
  with st.chat_message("user"):
    st.write(user_prompt)

if st.session_state.messages[-1]["role"] != "assistant":
  with st.chat_message("assistant"):
    with st.spinner("Loading..."):
      ai_response = llm_chain.predict(human_input=user_prompt)

      st.write(ai_response)

      ai_dict = llm_chain_2.predict(human_input=user_prompt)
      print(ai_dict)
      print(type(ai_dict))
      extracted_info = extract_user_info(ai_dict)
      # print(extracted_info)

      st.session_state.user_info.update(extracted_info)


  new_ai_message = {"role": "assistant", "content": ai_response}
  st.session_state.messages.append(new_ai_message)



###############################
  


##############################
  

# Initialize session state for user info if not already set
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}


# Collect user prompt from atop
# user_prompt = st.chat_input()


# Extract and store user information in session state
if user_prompt:
    extracted_info = extract_user_info(user_prompt)
    st.session_state.user_info.update(extracted_info)

# Display user info in the sidebar
with st.sidebar:
    st.subheader("User Information")
    if 'user_info' in st.session_state and st.session_state.user_info:
        for key, value in st.session_state.user_info.items():
            st.write(f"{key.capitalize()}: {value}")



#-------------------------------------------#



#Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)
data = conn.read(worksheet="Sheet1")


#extracted data to pd.dataframe
# ex_data = pd.DataFrame(ai_dict)

# conn.update(worksheet="Sheet1", data=ex_data)

#print(data)
# st.dataframe(data)

# if st.button("New Worksheet"):
#     conn.create(worksheet="Orders", data=extracted_info)
#     st.success("Worksheet Created 🎉")
  

#-------------------------------------------#
