from langchain.schema import BaseRetriever
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

def create_hybrid_qa_chain(retriever: BaseRetriever) -> RetrievalQA:
    """Create QA chain with Hybrid Retriever"""
    # Use OpenAI language model
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    # Define template for prompt
    template = """
    Bạn là trợ lý hỗ trợ khách hàng của Robot Pika, một robot học tiếng Anh cho trẻ em.
    Hãy trả lời câu hỏi của khách hàng dựa trên thông tin sau đây:
    
    {context}
    
    Câu hỏi: {question}
    
    Trả lời một cách lịch sự, ngắn gọn và rõ ràng. Nếu không có thông tin trong context, hãy thông báo bạn không có thông tin để trả lời câu hỏi đó.
    """
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )
    
    # Create chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
    
    return qa_chain 