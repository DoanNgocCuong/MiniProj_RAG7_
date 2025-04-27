from langchain.schema import BaseRetriever
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

class Generation:
    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0):
        self.model_name = model_name
        self.temperature = temperature
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature)

    def create_qa_chain(self, retriever: BaseRetriever) -> RetrievalQA:
        """Create QA chain with retriever"""
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
        
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        ) 