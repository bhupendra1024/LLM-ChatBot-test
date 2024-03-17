import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from decouple import config

prompt = PromptTemplate(
  input_variables = ["chat_history", "question"],
  template="""You are a finance advisor and your aim is to ask questions from use to develop a budgeting plan, 
              Question user in a consultant tone and get details of age, marital status, annual income, cost of living etc and devise
              a budgeting plan after you necessary information
            
              chat_history: {chat_history}
              Human: {question} 

              AI:"""
)

llm = ChatOpenAI(openai_api_key = config("OPEN_API_KEY"))
memory = ConversationBufferMemory(memory_key="chat_history", k=10)
llm_chain = LLMChain(
  llm=llm,
  memory=memory,
  prompt=prompt,
)


st.set_page_config(
  page_title="GPT Bot",
  page_icon="🤖",
  layout="wide"
)

st.title("GPT Bot")

if "messages" not in st.session_state.keys():
  st.session_state.messages = [
    {"role": "assistant", "content": "Hi I am your financial advisor, will you be willing to share a few details with me"}
  ]


for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.write(message["content"])


user_prompt = st.chat_input()

if user_prompt is not None:
  st.session_state.messages.append({"role": "user", "content": user_prompt})
  with st.chat_message("user"):
    st.write(user_prompt)

if st.session_state.messages[-1]["role"] != "assistant":
  with st.chat_message("assistant"):
    with st.spinner("Loading..."):
      ai_response = llm_chain.predict(question=user_prompt)
      st.write(ai_response)
  new_ai_message = {"role": "assistant", "content": ai_response}
  st.session_state.messages.append(new_ai_message)



