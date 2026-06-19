"""Adaptive Response Generation

This module generates responses tailored to each persona using LLM
with context from the RAG pipeline.
"""

import logging
import json
from typing import Dict, List, Tuple
import requests
from config import config
from src.persona_detector import Persona

logger = logging.getLogger(__name__)


class ResponseGenerator:
    """Generate persona-adaptive responses using Ollama"""

    def __init__(self):
        """Initialize response generator"""
        self.base_url = config.OLLAMA_BASE_URL
        self.model = config.LLM_MODEL
        self._test_connection()

    def _test_connection(self):
        """Test connection to Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                logger.info(f"Connected to Ollama at {self.base_url}")
            else:
                logger.warning(f"Ollama connection failed with status {response.status_code}")
        except Exception as e:
            logger.warning(f"Could not connect to Ollama: {str(e)}")

    def generate_response(
        self,
        query: str,
        retrieved_docs: List[Dict],
        persona: Persona,
        conversation_history: List[Dict] = None
    ) -> Dict:
        """
        Generate persona-adaptive response
        
        Args:
            query: User query
            retrieved_docs: Retrieved documents from RAG
            persona: Detected persona
            conversation_history: Previous conversation context
            
        Returns:
            Dictionary with response and metadata
        """
        if not retrieved_docs:
            return self._no_docs_response(query, persona)
        
        # Build context from retrieved documents
        context = self._build_context(retrieved_docs, persona)
        
        # Build persona-specific prompt
        prompt = self._build_persona_prompt(
            query=query,
            context=context,
            persona=persona,
            history=conversation_history
        )
        
        try:
            # Generate response using Ollama
            response_text = self._call_ollama(prompt)
            if self._is_generation_error(response_text):
                logger.warning("LLM generation failed; using knowledge-base fallback response")
                response_text = self._fallback_response_from_docs(query, retrieved_docs, persona)
            
            result = {
                "response": response_text,
                "persona": persona.value,
                "retrieved_sources": [doc["source"] for doc in retrieved_docs],
                "confidence": self._calculate_confidence(retrieved_docs),
                "context_used": len(retrieved_docs),
                "escalation_required": False,
                "escalation_reason": None
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return {
                "response": f"I encountered an error processing your request. Please try again.",
                "persona": persona.value,
                "error": str(e),
                "escalation_required": True,
                "escalation_reason": "System error - escalating to support"
            }

    def _build_context(self, retrieved_docs: List[Dict], persona: Persona) -> str:
        """Build context string from retrieved documents"""
        context_parts = ["Based on our knowledge base:"]
        
        for i, doc in enumerate(retrieved_docs, 1):
            source = doc.get("source", "Unknown").split("/")[-1]
            similarity = doc.get("similarity", 0)
            content = doc.get("content", "")
            
            # Truncate content for technical experts
            if persona == Persona.TECHNICAL_EXPERT:
                max_len = 500
            elif persona == Persona.FRUSTRATED_USER:
                max_len = 300
            else:
                max_len = 200
            
            if len(content) > max_len:
                content = content[:max_len] + "..."
            
            context_parts.append(f"\n[Source {i}: {source}]")
            context_parts.append(content)
        
        return "\n".join(context_parts)

    def _build_persona_prompt(
        self,
        query: str,
        context: str,
        persona: Persona,
        history: List[Dict] = None
    ) -> str:
        """Build persona-specific prompt"""
        
        persona_instructions = {
            Persona.TECHNICAL_EXPERT: {
                "style": "technical and detailed",
                "instructions": [
                    "Include technical details, error codes, and explanations",
                    "Provide step-by-step troubleshooting if applicable",
                    "Reference API documentation or code examples",
                    "Explain the root cause of issues",
                    "Use technical terminology appropriately"
                ]
            },
            Persona.FRUSTRATED_USER: {
                "style": "empathetic and reassuring",
                "instructions": [
                    "Acknowledge their frustration and validate their concerns",
                    "Use simple, plain language",
                    "Provide clear, actionable steps",
                    "Be concise and avoid jargon",
                    "Offer to help further if needed"
                ]
            },
            Persona.BUSINESS_EXECUTIVE: {
                "style": "professional and concise",
                "instructions": [
                    "Focus on business impact and outcomes",
                    "Provide brief, bullet-pointed information",
                    "Include timeline estimates when relevant",
                    "Highlight ROI or business benefits",
                    "Keep explanation under 150 words"
                ]
            }
        }
        
        instr = persona_instructions[persona]
        
        prompt = f"""You are a customer support agent for CloudSync Pro, a cloud data synchronization platform.

Style: Respond in a {instr['style']} manner.

Instructions:
{chr(10).join(f"- {i}" for i in instr['instructions'])}

User Query: {query}

Knowledge Base Context:
{context}

Conversation History:
"""
        
        if history:
            for msg in history[-2:]:  # Last 2 messages for context
                prompt += f"\nUser: {msg.get('user', '')}\nAssistant: {msg.get('assistant', '')}"
        else:
            prompt += "No previous context."
        
        prompt += "\n\nPlease respond based on the knowledge base content provided above. If the knowledge base doesn't contain sufficient information, indicate that and suggest escalation to a human agent."
        
        return prompt

    def _call_ollama(self, prompt: str, temperature: float = 0.7) -> str:
        """Call Ollama API for text generation"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": temperature,
                    "stream": False,
                    "num_predict": 500
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            else:
                logger.error(f"Ollama error: {response.status_code} - {response.text}")
                return f"Error generating response (HTTP {response.status_code})"
                
        except requests.exceptions.ConnectionError:
            return "Unable to connect to Ollama service. Please ensure Ollama is running at " + self.base_url
        except Exception as e:
            logger.error(f"Error calling Ollama: {str(e)}")
            return f"Error generating response: {str(e)}"

    def _is_generation_error(self, response_text: str) -> bool:
        """Detect transport/model errors returned by the local LLM call."""
        error_prefixes = (
            "Unable to connect to Ollama service.",
            "Error generating response",
        )
        return response_text.startswith(error_prefixes)

    def _fallback_response_from_docs(
        self,
        query: str,
        retrieved_docs: List[Dict],
        persona: Persona
    ) -> str:
        """Build a concise support answer directly from retrieved KB snippets."""
        top_doc = retrieved_docs[0]
        content = top_doc.get("content", "").strip()
        source = top_doc.get("source", "knowledge base").split("\\")[-1].split("/")[-1]

        if len(content) > 900:
            content = content[:900].rsplit(" ", 1)[0] + "..."

        if persona == Persona.FRUSTRATED_USER:
            intro = "I found a relevant support article. Let's try these steps:"
        elif persona == Persona.BUSINESS_EXECUTIVE:
            intro = "I found relevant guidance in our support documentation:"
        else:
            intro = "I found relevant technical documentation for this issue:"

        return f"{intro}\n\n{content}\n\nSource: {source}"

    def _calculate_confidence(self, retrieved_docs: List[Dict]) -> float:
        """Calculate confidence based on retrieval scores"""
        if not retrieved_docs:
            return 0.0
        
        similarities = [doc.get("similarity", 0) for doc in retrieved_docs]
        return max(similarities)

    def _no_docs_response(self, query: str, persona: Persona) -> Dict:
        """Generate response when no relevant documents found"""
        responses = {
            Persona.TECHNICAL_EXPERT: {
                "response": "I apologize, but I couldn't find relevant technical documentation in our knowledge base for your query. "
                           "Could you provide more specific details about your issue? "
                           "If this is a critical technical matter, I recommend escalating to our engineering team.",
                "escalation_reason": "No relevant documentation found"
            },
            Persona.FRUSTRATED_USER: {
                "response": "I'm sorry, but I don't have enough information in our support resources to help with this issue right away. "
                           "I want to make sure you get the help you need! Let me connect you with one of our support specialists who can assist you directly.",
                "escalation_reason": "Unable to find solution in knowledge base"
            },
            Persona.BUSINESS_EXECUTIVE: {
                "response": "Unfortunately, this issue isn't covered in our standard documentation. "
                           "To best address your business needs, I'm escalating this to our support team for immediate attention.",
                "escalation_reason": "Issue requires specialized support"
            }
        }
        
        response_data = responses.get(persona, responses[Persona.TECHNICAL_EXPERT])
        
        return {
            "response": response_data["response"],
            "persona": persona.value,
            "retrieved_sources": [],
            "confidence": 0.0,
            "context_used": 0,
            "escalation_required": True,
            "escalation_reason": response_data["escalation_reason"]
        }


# Singleton instance
_response_generator = None


def get_response_generator() -> ResponseGenerator:
    """Get or create response generator instance"""
    global _response_generator
    if _response_generator is None:
        _response_generator = ResponseGenerator()
    return _response_generator
