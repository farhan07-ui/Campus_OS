import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 1. Configuration & API Key Setup
# Replace with your actual key or set the environment variable
os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"

DB_DIR = "./chroma_db"
EMBEDDING_MODEL = OpenAIEmbeddings(model="text-embedding-3-small")

def upload_and_process_syllabus(pdf_path: str):
    """
    Loads a syllabus PDF, splits it into chunks, converts it to vector embeddings,
    and stores it in the local ChromaDB database.
    """
    print(f"🔄 Processing {pdf_path}...")
    
    # Load the PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    # Split text into manageable chunks so the AI can pinpoint specific sections
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )
    docs = text_splitter.split_documents(documents)
    
    # Create vector database and save it locally
    vector_store = Chroma.from_documents(
        documents=docs, 
        embedding=EMBEDDING_MODEL, 
        persist_directory=DB_DIR
    )
    
    print(f"✅ Syllabus successfully processed and saved to database at '{DB_DIR}'!")
    return vector_store

def query_syllabus(question: str):
    """
    Connects to the stored database, retrieves relevant syllabus chunks,
    and uses the LLM to answer the user's question.
    """
    # Load the existing database
    if not os.path.exists(DB_DIR):
        print("❌ No syllabus database found. Please upload a syllabus first.")
        return
        
    vector_store = Chroma(
        persist_directory=DB_DIR, 
        embedding_function=EMBEDDING_MODEL
    )
    
    # Configure retriever to fetch the top 3 most relevant chunks
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    
    # Initialize the LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # Define the system prompt rules for the AI Teacher
    system_prompt = (
        "You are an AI Campus Assistant. Answer the student's question using only the provided "
        "syllabus context below. If you do not know the answer or if it's not in the syllabus, "
        "say 'That information is not stated in the syllabus.' Do not make up information.\n\n"
        "Context:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    # Create the RAG Chain
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    # Run the query
    response = rag_chain.invoke({"input": question})
    return response["answer"]

# --- 🎯 Step-by-Step Execution Example ---
if __name__ == "__main__":
    # Step 1: Simulated Upload (Provide a path to a real syllabus PDF on your machine)
    # create a dummy file or use an actual syllabus.pdf
    syllabus_file = "cs101_syllabus.pdf" 
    
    if os.path.exists(syllabus_file):
        upload_and_process_syllabus(syllabus_file)
        
        # Step 2: Interactive Chat Loop
        print("\n--- 💬 Chat with your Syllabus (Type 'exit' to quit) ---")
        while True:
            user_question = input("\nStudent: ")
            if user_question.lower() == 'exit':
                break
                
            ai_response = query_syllabus(user_question)
            print(f"AI Assistant: {ai_response}")
    else:
        print(f"Please place a valid PDF named '{syllabus_file}' in this directory to test.")
