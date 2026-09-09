"""
AI Agent - Main intelligence engine
"""

from typing import List, Optional
import openai
from core.config import Config
from core.database import VectorDatabase
from core.processor import WebProcessor


class AIAgent:
    """AI Agent for answering questions using knowledge base"""
    
    def __init__(self, config: Config):
        """Initialize AI Agent"""
        self.config = config
        self.api_key = config.get_api_key()
        openai.api_key = self.api_key
        self.db = VectorDatabase(config)
        self.processor = WebProcessor(config)
        self.chat_model = config.get("chat_model", "gpt-3.5-turbo")
        self.max_context = config.get("max_context_length", 2000)
    
    def answer_question(self, question: str) -> str:
        """Answer a question using knowledge base"""
        try:
            # Search for relevant context
            context = self.db.search(question, limit=3)
            
            if not context:
                # Use general knowledge
                return self._generate_answer(question, "")
            
            # Prepare context string
            context_str = "\n".join([f"- {doc}" for doc in context])
            
            # Generate answer with context
            return self._generate_answer(question, context_str)
        
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def _generate_answer(self, question: str, context: str) -> str:
        """Generate answer using OpenAI API"""
        try:
            if context:
                prompt = f"""Based on the following context, answer the question:

Context:
{context}

Question: {question}

Answer:"""
            else:
                prompt = f"Question: {question}\n\nAnswer:"
            
            response = openai.ChatCompletion.create(
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            return f"❌ Error generating answer: {str(e)}"
    
    def add_website(self, url: str) -> bool:
        """Add website to knowledge base"""
        try:
            # Process website
            documents = self.processor.process_url(url)
            
            if not documents:
                return False
            
            # Add to database
            return self.db.add_documents(documents, url)
        
        except Exception as e:
            print(f"❌ Error adding website: {str(e)}")
            return False
    
    def get_stats(self) -> dict:
        """Get database statistics"""
        return self.db.get_stats()
    
    def clear_database(self) -> bool:
        """Clear knowledge base"""
        return self.db.clear()
