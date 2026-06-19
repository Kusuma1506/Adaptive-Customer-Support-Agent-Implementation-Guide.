"""Main Support Agent Orchestration

This module orchestrates all components of the customer support agent:
- Persona detection
- RAG retrieval
- Response generation
- Escalation handling
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from src.persona_detector import get_persona_detector, Persona
from src.rag_pipeline import get_rag_pipeline, initialize_rag_pipeline
from src.response_generator import get_response_generator
from src.escalation_handler import get_escalation_handler

logger = logging.getLogger(__name__)


class SupportAgent:
    """Main customer support agent"""

    def __init__(self, initialize_kb: bool = True):
        """
        Initialize support agent
        
        Args:
            initialize_kb: Whether to initialize knowledge base on startup
        """
        self.persona_detector = get_persona_detector()
        self.rag_pipeline = get_rag_pipeline()
        self.response_generator = get_response_generator()
        self.escalation_handler = get_escalation_handler()
        
        # Conversation state
        self.conversation_history = []
        self.attempts = []
        self.current_persona = None
        
        # Initialize knowledge base if needed
        if initialize_kb:
            self._initialize_knowledge_base()

    def _initialize_knowledge_base(self):
        """Initialize the knowledge base"""
        logger.info("Initializing knowledge base...")
        stats = initialize_rag_pipeline()
        logger.info(f"Knowledge base stats: {stats}")

    def process_message(self, user_message: str) -> Dict:
        """
        Process user message and generate response
        
        Args:
            user_message: User's input message
            
        Returns:
            Dictionary containing:
                - response: Generated response
                - persona: Detected persona
                - escalated: Whether conversation was escalated
                - metadata: Additional metadata
        """
        # Add to conversation history
        self.conversation_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "user": user_message
        })
        
        # Step 1: Detect persona
        persona, persona_confidence, persona_details = self.persona_detector.detect_persona(user_message)
        self.current_persona = persona
        
        logger.info(f"Detected persona: {persona.value} (confidence: {persona_confidence:.2f})")
        
        # Step 2: Retrieve relevant documents
        retrieved_docs = self.rag_pipeline.retrieve(user_message)
        
        # Step 3: Generate response
        response_data = self.response_generator.generate_response(
            query=user_message,
            retrieved_docs=retrieved_docs,
            persona=persona,
            conversation_history=self.conversation_history[:-1]  # Exclude current message
        )
        
        # Step 4: Check for escalation
        attempt_number = len(self.attempts) + 1
        should_escalate, escalation_reason = self.escalation_handler.should_escalate(
            response=response_data,
            attempt_count=attempt_number
        )
        
        # Record attempt
        attempt_record = {
            "attempt_number": attempt_number,
            "timestamp": datetime.utcnow().isoformat(),
            "persona": persona.value,
            "confidence": persona_confidence,
            "retrieval_count": len(retrieved_docs),
            "retrieval_confidence": response_data.get("confidence", 0),
            "escalation": should_escalate,
            "reason": escalation_reason
        }
        self.attempts.append(attempt_record)
        
        # Step 5: Prepare handoff if escalating
        handoff_summary = None
        if should_escalate:
            handoff_summary = self.escalation_handler.generate_handoff_summary(
                persona=persona,
                issue=user_message,
                conversation_history=self.conversation_history,
                retrieved_docs=retrieved_docs,
                attempts_made=self.attempts,
                escalation_reason=escalation_reason
            )
        
        # Update conversation history with response
        self.conversation_history[-1]["assistant"] = response_data.get("response", "")
        self.conversation_history[-1]["persona"] = persona.value
        
        return {
            "response": response_data.get("response", ""),
            "persona": persona.value,
            "persona_confidence": persona_confidence,
            "persona_keywords": persona_details.get("primary_keywords", []),
            "retrieved_sources": response_data.get("retrieved_sources", []),
            "retrieval_confidence": response_data.get("confidence", 0),
            "escalated": should_escalate,
            "escalation_reason": escalation_reason,
            "handoff_summary": handoff_summary,
            "context_documents_used": response_data.get("context_used", 0),
            "attempt_number": attempt_number,
            "conversation_length": len(self.conversation_history)
        }

    def get_conversation_history(self) -> List[Dict]:
        """Get full conversation history"""
        return self.conversation_history

    def reset_conversation(self):
        """Reset conversation state for new customer"""
        self.conversation_history = []
        self.attempts = []
        self.current_persona = None
        logger.info("Conversation reset")

    def get_session_summary(self) -> Dict:
        """Get summary of current session"""
        if not self.conversation_history:
            return {"status": "no_conversation"}
        
        # Calculate statistics
        escalated = any(attempt.get("escalation") for attempt in self.attempts)
        total_attempts = len(self.attempts)
        avg_confidence = sum(a.get("confidence", 0) for a in self.attempts) / total_attempts if total_attempts > 0 else 0
        
        personas_used = set(msg.get("persona") for msg in self.conversation_history if msg.get("persona"))
        
        return {
            "total_messages": len(self.conversation_history),
            "total_attempts": total_attempts,
            "escalated": escalated,
            "personas_detected": list(personas_used),
            "average_confidence": avg_confidence,
            "session_duration": self._calculate_session_duration(),
            "first_message": self.conversation_history[0] if self.conversation_history else None,
            "last_message": self.conversation_history[-1] if self.conversation_history else None
        }

    def _calculate_session_duration(self) -> str:
        """Calculate session duration"""
        if len(self.conversation_history) < 2:
            return "< 1 minute"
        
        first = self.conversation_history[0].get("timestamp")
        last = self.conversation_history[-1].get("timestamp")
        
        try:
            from datetime import datetime
            first_dt = datetime.fromisoformat(first)
            last_dt = datetime.fromisoformat(last)
            duration = (last_dt - first_dt).total_seconds()
            
            if duration < 60:
                return "< 1 minute"
            elif duration < 3600:
                return f"{int(duration // 60)} minutes"
            else:
                return f"{int(duration // 3600)} hours"
        except:
            return "Unknown"

    def get_knowledge_base_stats(self) -> Dict:
        """Get knowledge base statistics"""
        return self.rag_pipeline.get_collection_stats()


# Singleton instance
_support_agent = None


def get_support_agent(initialize_kb: bool = True) -> SupportAgent:
    """Get or create support agent instance"""
    global _support_agent
    if _support_agent is None:
        _support_agent = SupportAgent(initialize_kb=initialize_kb)
    return _support_agent


def initialize_support_system() -> Dict:
    """Initialize the entire support system"""
    logger.info("Initializing support system...")
    
    try:
        agent = get_support_agent(initialize_kb=True)
        kb_stats = agent.get_knowledge_base_stats()
        
        initialization_result = {
            "status": "initialized",
            "knowledge_base": kb_stats,
            "agent_ready": True
        }
        
        logger.info(f"Support system initialized: {initialization_result}")
        return initialization_result
        
    except Exception as e:
        logger.error(f"Error initializing support system: {str(e)}")
        return {
            "status": "error",
            "error_message": str(e),
            "agent_ready": False
        }
