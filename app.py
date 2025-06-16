import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(page_title="chatbot", layout="wide")
st.title("ChatBot: Llama 3.2 on Ollama")

# building the model
model=ChatOllama(
    model="llama3.2:1b",
    base_url="http://localhost:11434"
)

# system message template
system_message=SystemMessagePromptTemplate.from_template("You are a helpful AI assistant. You give responses in only 100 words. You provide responses according to the context only.")

# Chat histroy using session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"]=[]

# form for Questions
#with st.form("Form"):
    #text=st.text_area("Enter your question here...")
    #submit=st.form_submit_button("Submit")
    
text=st.chat_input("Type Here....")

# Function to generate responses
def generate_response(chat_history):
    chat_template=ChatPromptTemplate.from_messages(chat_history)
    chain=chat_template|model|StrOutputParser()
    response=chain.invoke({})
    return response

# function to get chat history user message in 'user' key
# and ai message in 'assistant' key
def get_history():
    chat_history=[system_message]
    for chat in st.session_state["chat_history"]:
        prompt=HumanMessagePromptTemplate.from_template(chat['user'])
        chat_history.append(prompt)
        ai_message=AIMessagePromptTemplate.from_template(chat['assistant'])
        chat_history.append(ai_message)
    return chat_history
    
# Human Message
#if submit and text:
if text:
    with st.spinner("Thinking...."):
        prompt=HumanMessagePromptTemplate.from_template(text)
        chat_history=get_history()
        chat_history.append(prompt)
        response=generate_response(chat_history)
        st.session_state["chat_history"].append({'user':text,'assistant':response})

with st.sidebar:
    st.title("DashBoard")
    st.write("Chat about anything with your AI friendly Assistant")
    
    st.markdown("---")
    st.subheader("🕓 Conversation History")
    
    # Display all user questions in the sidebar
    if st.session_state["chat_history"]:
        for i, chat in enumerate(reversed(st.session_state["chat_history"])):
            st.markdown(f"**{len(st.session_state['chat_history']) - i}.** {chat['user']}")
    else:
        st.write("No messages yet.")

# Add some CSS for alignment
st.markdown("""
<style>
.user-message {
    padding: 10px;
    border-radius: 10px;
    max-width: 70%;
    margin-left: auto;
    margin-right: 200px;
    text-align: right;
}

.bot-message {
    padding: 10px;
    border-radius: 10px;
    max-width: 70%;
    margin-right: auto;
    margin-left: 10px;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

# Render messages like a real chat interface
for chat in st.session_state['chat_history']:
    # User on right
    st.markdown(f"<div class='user-message'>👱‍♀️ {chat['user']}</div>", unsafe_allow_html=True)
    # Assistant on left
    st.markdown(f"<div class='bot-message'>🤖 {chat['assistant']}</div>", unsafe_allow_html=True)


    st.markdown("---")
