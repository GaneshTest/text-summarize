from openai import OpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import YoutubeLoader
import bs4
import streamlit as st
import validators
from langchain_groq import ChatGroq
from langchain.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
import os 
from dotenv import load_dotenv

load_dotenv()

groq_api_key= os.getenv('GROQ_API_KEY')
model_groq=ChatGroq(model="llama-3.1-8b-instant",groq_api_key=groq_api_key)

# System prompt
system_prompt = """
You are an expert assistant specialized in analyzing content from  YouTube videos and websites.
You will be given the full transcript or text content, and you need to summarize it clearly and concisely.
"""

#User prompt
userPrompt="""
Provide the summary of the following content
"""

# Create a simple prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{input}")
])


# Streamlit page setup
st.set_page_config(page_title="Summarize text from YouTube or Website", page_icon="📄")
st.title("OpenAI: Summarize Content from YouTube or Website")
st.subheader("Enter a URL below")

# Input URL
generic_url = st.text_input("URL", label_visibility="collapsed").strip()

# Custom headers for web scraping
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36 "
        "Edg/120.0.0.0"
    )
}

def summarizeWeb(url)->str:
    loader = WebBaseLoader(
    web_paths=(url,),
   
   )
    documents=loader.load()
    return documents
    
                        
def summarizeYoutbe(youtube_url)->str:
      loader = YoutubeLoader.from_youtube_url(youtube_url= youtube_url)
      return loader.load()
  
  
if st.button("Summarize the content from URL or YouTube"):
    if not validators.url(generic_url):
        st.error("Please enter a valid URL.")
    else :
          try:
              with st.spinner("Fetching and summarizing content..."):
                # Load content
                if "youtube.com" in generic_url:
                    documents = summarizeYoutbe(generic_url)
                    
                else :
                    documents= summarizeWeb(generic_url)
                page_text= userPrompt
                if  documents is not None:
                    for doc in documents:
                        page_text += doc.page_content + "\n"
                    if page_text.strip():
                        chain =prompt|model_groq
                        result = chain.invoke({"input": page_text})
                        st.success("Summary:")
                        st.write(result.content)
                    else :
                        st.error("No text content could be extracted.")
                else :
                    st.error("No text content could be extracted.")
                        
                                
          except Exception as e:
              st.exception(f"An error occurred: {e}")
              
               
            
                    
                            
        
            
        
              
                         
            
     
    

    
