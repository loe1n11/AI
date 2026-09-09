"""
AI Agent - Advanced intelligence engine with multi-step reasoning
"""

from typing import List, Optional, Dict, Tuple
import openai
from core.config import Config
from core.database import VectorDatabase
from core.processor import WebProcessor
import json
from datetime import datetime


class AIAgent:
    """Advanced AI Agent with intelligent reasoning capabilities"""
    
    def __init__(self, config: Config):
        """Initialize AI Agent with advanced features"""
        self.config = config
        self.api_key = config.get_api_key()
        openai.api_key = self.api_key
        self.db = VectorDatabase(config)
        self.processor = WebProcessor(config)
        self.chat_model = config.get("chat_model", "gpt-3.5-turbo")
        self.max_context = config.get("max_context_length", 2000)
        
        # Advanced features
        self.conversation_history: List[Dict] = []
        self.reasoning_cache: Dict = {}
        self.question_reformulations: List[str] = []
        self.confidence_scores: Dict = {}
    
    def answer_question(self, question: str, use_advanced_reasoning: bool = True) -> str:
        """Answer a question using intelligent multi-step reasoning"""
        try:
            if use_advanced_reasoning:
                return self._advanced_answer_pipeline(question)
            else:
                return self._simple_answer(question)
        
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def _advanced_answer_pipeline(self, question: str) -> str:
        """Multi-step reasoning pipeline for better answers"""
        # Step 1: Analyze question intent
        intent = self._analyze_question_intent(question)
        print(f"\n🔍 Question Intent: {intent}")
        
        # Step 2: Generate question reformulations
        reformulations = self._reformulate_question(question)
        print(f"🔄 Searching with {len(reformulations)} query variations...")
        
        # Step 3: Intelligent context gathering
        context_docs = self._gather_intelligent_context(question, reformulations)
        
        # Step 4: Check if question requires sub-questions
        if self._requires_subquestions(question):
            return self._answer_complex_question(question, context_docs)
        
        # Step 5: Generate answer with chain-of-thought
        answer = self._generate_intelligent_answer(question, context_docs, intent)
        
        # Step 6: Verify and improve answer
        improved_answer = self._verify_and_improve_answer(answer, question, context_docs)
        
        return improved_answer
    
    def _analyze_question_intent(self, question: str) -> str:
        """Analyze what type of question this is"""
        try:
            response = openai.ChatCompletion.create(
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": "Analyze the intent of the question in one short phrase. Categories: factual, conceptual, how-to, comparison, opinion, evaluation, definition."},
                    {"role": "user", "content": question}
                ],
                temperature=0.3,
                max_tokens=50
            )
            return response.choices[0].message.content.strip()
        except:
            return "factual"
    
    def _reformulate_question(self, question: str) -> List[str]:
        """Generate multiple reformulations of the question"""
        try:
            response = openai.ChatCompletion.create(
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": "Generate 3 different ways to ask the same question. Format: 1. ... 2. ... 3. ..."},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            text = response.choices[0].message.content.strip()
            # Parse reformulations
            reformulations = [question]  # Include original
            for line in text.split('\n'):
                if line.strip() and '.' in line:
                    reformulated = line.split('.', 1)[1].strip()
                    if reformulated:
                        reformulations.append(reformulated)
            
            return reformulations[:4]  # Return up to 4 queries
        except:
            return [question]
    
    def _gather_intelligent_context(self, question: str, reformulations: List[str]) -> List[Tuple[str, float]]:
        """Gather context using multiple queries with confidence scores"""
        all_docs = []
        
        for query in reformulations:
            docs = self.db.search(query, limit=2)
            
            if docs:
                # Calculate relevance score
                relevance = self._calculate_relevance_score(question, docs[0])
                for doc in docs:
                    all_docs.append((doc, relevance))
        
        # Remove duplicates and sort by relevance
        unique_docs = {}
        for doc, score in all_docs:
            if doc not in unique_docs or score > unique_docs[doc]:
                unique_docs[doc] = score
        
        sorted_docs = sorted(unique_docs.items(), key=lambda x: x[1], reverse=True)
        return sorted_docs[:5]  # Return top 5 most relevant docs
    
    def _calculate_relevance_score(self, question: str, document: str) -> float:
        """Calculate relevance score between question and document"""
        try:
            # Simple scoring based on keyword overlap
            question_words = set(question.lower().split())
            doc_words = set(document.lower().split())
            
            overlap = len(question_words & doc_words)
            total = len(question_words | doc_words)
            
            return overlap / total if total > 0 else 0.0
        except:
            return 0.5
    
    def _requires_subquestions(self, question: str) -> bool:
        """Check if question is complex and needs decomposition"""
        complex_keywords = ["how", "why", "compare", "analyze", "explain", "relationship", "impact", "process"]
        question_lower = question.lower()
        
        # Count complex keywords
        keyword_count = sum(1 for keyword in complex_keywords if keyword in question_lower)
        
        return keyword_count >= 2 or len(question.split()) > 15
    
    def _answer_complex_question(self, question: str, context_docs: List[Tuple[str, float]]) -> str:
        """Break down and answer complex questions"""
        try:
            # Generate sub-questions
            response = openai.ChatCompletion.create(
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": "Break down this complex question into 2-3 simpler sub-questions. Format: 1. ... 2. ... 3. ..."},
                    {"role": "user", "content": question}
                ],
                temperature=0.5,
                max_tokens=200
            )
            
            subquestions_text = response.choices[0].message.content.strip()
            
            # Parse and answer sub-questions
            sub_answers = []
            for line in subquestions_text.split('\n'):
                if line.strip() and '.' in line:
                    subq = line.split('.', 1)[1].strip()
                    if subq:
                        sub_context = self.db.search(subq, limit=2)
                        sub_answer = self._generate_intelligent_answer(subq, [(doc, 1.0) for doc in sub_context], "sub-question")
                        sub_answers.append(sub_answer)
            
            # Synthesize answers
            context_str = "\n".join([f"- {doc}" for doc, _ in context_docs[:3]])
            synthesis_prompt = f"""Based on the following sub-question answers, provide a comprehensive answer to the main question:

Main Question: {question}

Context Information:
{context_str}

Sub-Question Answers:
{chr(10).join([f'{i+1}. {ans}' for i, ans in enumerate(sub_answers)])}

Comprehensive Answer:"""
            
            response = openai.ChatCompletion.create(
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant. Synthesize the sub-answers into a comprehensive response."},
                    {"role": "user", "content": synthesis_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            return self._generate_intelligent_answer(question, context_docs, "fallback")
    
    def _generate_intelligent_answer(self, question: str, context_docs: List[Tuple[str, float]], intent: str) -> str:
        """Generate answer using chain-of-thought reasoning"""
        try:
            if not context_docs:
                # Generate without context
                return self._generate_general_answer(question)
            
            context_str = "\n".join([f"- {doc}" for doc, _ in context_docs[:3]])
            
            # Chain-of-thought prompt
            prompt = f"""Based on the following context, answer the question using step-by-step reasoning:

Context:
{context_str}

Question: {question}

Please think through this step-by-step:
1. What is the main topic?
2. What key information is relevant?
3. How do these pieces connect?
4. What is the answer?

Answer:"""
            
            response = openai.ChatCompletion.create(
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": "You are an expert AI assistant. Reason through questions carefully and provide detailed, accurate answers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=600
            )
            
            answer = response.choices[0].message.content.strip()
            
            # Store in conversation history
            self.conversation_history.append({
                "question": question,
                "answer": answer,
                "intent": intent,
                "timestamp": datetime.now().isoformat(),
                "context_count": len(context_docs)
            })
            
            return answer
        
        except Exception as e:
            return f"❌ Error generating answer: {str(e)}"
    
    def _generate_general_answer(self, question: str) -> str:
        """Generate answer using general knowledge"""
        try:
            response = openai.ChatCompletion.create(
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": "You are a helpful, knowledgeable AI assistant."},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def _verify_and_improve_answer(self, answer: str, question: str, context_docs: List[Tuple[str, float]]) -> str:
        """Verify answer quality and improve if needed"""
        try:
            # Calculate confidence
            confidence = self._calculate_answer_confidence(answer, question, context_docs)
            
            if confidence < 0.5 and context_docs:
                # Try to improve low-confidence answer
                context_str = "\n".join([f"- {doc}" for doc, _ in context_docs])
                
                improvement_prompt = f"""The following answer might be incomplete. Based on the context, provide a more complete and accurate answer:

Original Answer: {answer}

Question: {question}

Context:
{context_str}

Improved Answer:"""
                
                response = openai.ChatCompletion.create(
                    model=self.chat_model,
                    messages=[
                        {"role": "system", "content": "Improve the answer to be more accurate and complete."},
                        {"role": "user", "content": improvement_prompt}
                    ],
                    temperature=0.6,
                    max_tokens=500
                )
                
                return response.choices[0].message.content.strip()
            
            return answer
        
        except:
            return answer
    
    def _calculate_answer_confidence(self, answer: str, question: str, context_docs: List[Tuple[str, float]]) -> float:
        """Calculate confidence score for the answer"""
        if not context_docs:
            return 0.3  # Low confidence without context
        
        # Average relevance score
        avg_relevance = sum(score for _, score in context_docs) / len(context_docs)
        
        # Bonus for detailed answers
        answer_length = len(answer.split())
        length_bonus = min(0.2, answer_length / 100)
        
        confidence = min(1.0, avg_relevance + length_bonus)
        self.confidence_scores[question] = confidence
        
        return confidence
    
    def _simple_answer(self, question: str) -> str:
        """Simple answer without advanced reasoning"""
        try:
            context = self.db.search(question, limit=3)
            
            if not context:
                return self._generate_general_answer(question)
            
            context_str = "\n".join([f"- {doc}" for doc in context])
            
            prompt = f"""Based on the following context, answer the question:

Context:
{context_str}

Question: {question}

Answer:"""
            
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
            return f"❌ Error: {str(e)}"
    
    def add_website(self, url: str) -> bool:
        """Add website to knowledge base"""
        try:
            documents = self.processor.process_url(url)
            
            if not documents:
                return False
            
            return self.db.add_documents(documents, url)
        
        except Exception as e:
            print(f"❌ Error adding website: {str(e)}")
            return False
    
    def get_stats(self) -> dict:
        """Get database statistics and reasoning stats"""
        db_stats = self.db.get_stats()
        
        return {
            **db_stats,
            "conversation_history_size": len(self.conversation_history),
            "average_confidence": sum(self.confidence_scores.values()) / len(self.confidence_scores) if self.confidence_scores else 0.0,
            "reasoning_cache_size": len(self.reasoning_cache)
        }
    
    def clear_database(self) -> bool:
        """Clear knowledge base"""
        success = self.db.clear()
        if success:
            # Also clear conversation history
            self.conversation_history = []
            self.reasoning_cache = {}
            self.confidence_scores = {}
        return success
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history for learning"""
        return self.conversation_history
