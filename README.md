# LLM-ChatBot-test

Streamlit application that leverages the LangChain library to create a financial advisor bot. The bot is designed to interact with users, asking for personal details such as age, marital status, annual income, and cost of living to devise a budgeting plan. The application uses a custom prompt template and an LLMChain for generating responses based on the user's input.

Features

Custom Prompt Template: The bot uses a custom prompt template to guide the conversation, ensuring it asks the right questions to gather necessary information for budgeting.

LLMChain Integration: The application integrates with LangChain's LLMChain to generate responses based on the user's input and the conversation history.

Memory Management: Utilizes ConversationBufferMemory to maintain the conversation history, ensuring context is preserved across interactions.

Streamlit Interface: The application is built with Streamlit, providing a user-friendly interface for the chatbot.
