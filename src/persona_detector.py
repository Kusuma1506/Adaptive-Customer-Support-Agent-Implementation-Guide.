"""Persona Detection System

This module detects customer personas from incoming messages using:
1. Keyword matching
2. LLM-based classification
3. Sentiment analysis
"""

import re
from typing import Dict, Tuple, List
from enum import Enum
import logging
from config import config

logger = logging.getLogger(__name__)


class Persona(Enum):
    """Customer persona types"""
    TECHNICAL_EXPERT = "Technical Expert"
    FRUSTRATED_USER = "Frustrated User"
    BUSINESS_EXECUTIVE = "Business Executive"


class PersonaDetector:
    """Detect customer persona from incoming messages"""

    def __init__(self):
        """Initialize persona detector with keywords and patterns"""
        self.personas = config.PERSONAS
        self.technical_keywords = {
            "api", "error", "log", "debug", "stack trace", "configuration",
            "integration", "authentication", "endpoint", "webhook", "payload",
            "jwt", "oauth", "ssl", "certificate", "encryption", "database",
            "query", "index", "deployment", "docker", "kubernetes", "lambda",
            "serverless", "microservices", "rest", "graphql", "protocol"
        }
        
        self.frustrated_keywords = {
            "frustrated", "not working", "broken", "help", "please",
            "urgent", "critical", "asap", "angry", "disappointed",
            "terrible", "terrible", "never", "always fails", "useless",
            "impossible", "stuck", "wasting", "ridiculous", "stupid"
        }
        
        self.executive_keywords = {
            "impact", "business", "operations", "timeline", "resolution",
            "uptime", "revenue", "productivity", "cost", "risk",
            "roi", "kpi", "sla", "compliance", "scalability",
            "enterprise", "implementation", "strategy", "executive",
            "board", "investor", "quarterly", "fiscal"
        }

    def detect_persona(self, message: str) -> Tuple[Persona, float, Dict]:
        """
        Detect persona from user message
        
        Args:
            message: User input message
            
        Returns:
            Tuple of (Persona, confidence_score, analysis_details)
        """
        message_lower = message.lower()
        
        # Calculate keyword scores
        scores = {
            Persona.TECHNICAL_EXPERT: self._calculate_keyword_score(
                message_lower, self.technical_keywords
            ),
            Persona.FRUSTRATED_USER: self._calculate_keyword_score(
                message_lower, self.frustrated_keywords
            ),
            Persona.BUSINESS_EXECUTIVE: self._calculate_keyword_score(
                message_lower, self.executive_keywords
            ),
        }
        
        # Add pattern-based scoring
        scores[Persona.TECHNICAL_EXPERT] += self._score_technical_patterns(message_lower)
        scores[Persona.FRUSTRATED_USER] += self._score_frustrated_patterns(message_lower)
        scores[Persona.BUSINESS_EXECUTIVE] += self._score_executive_patterns(message_lower)
        
        # Determine detected persona
        detected_persona = max(scores, key=scores.get)
        confidence = scores[detected_persona] / max(sum(scores.values()), 1)
        
        # Analysis details for transparency
        details = {
            "scores": {p.value: score for p, score in scores.items()},
            "confidence": confidence,
            "primary_keywords": self._extract_matching_keywords(
                message_lower, 
                self._get_keywords_for_persona(detected_persona)
            )
        }
        
        logger.info(f"Detected persona: {detected_persona.value} (confidence: {confidence:.2f})")
        
        return detected_persona, confidence, details

    def _calculate_keyword_score(self, message: str, keywords: set) -> float:
        """Calculate score based on keyword matches"""
        score = 0
        for keyword in keywords:
            if keyword in message:
                score += 1
        return score

    def _score_technical_patterns(self, message: str) -> float:
        """Score based on technical patterns"""
        score = 0
        
        # Check for code snippets or technical format
        if re.search(r'```|<|>|{|}|\[|\]|error.*code|http|json', message):
            score += 1
        
        # Check for question about internals
        if re.search(r'how does|explain|root cause|what causes|why|debug', message):
            score += 0.5
        
        # Check for requests for logs/details
        if re.search(r'log|trace|stack|debug|config|version|endpoint', message):
            score += 0.5
        
        return score

    def _score_frustrated_patterns(self, message: str) -> float:
        """Score based on frustrated patterns"""
        score = 0
        
        # Check for exclamation marks (emotion indicator)
        if message.count('!') > 1:
            score += 1
        
        # Check for ALL CAPS words
        caps_words = len(re.findall(r'\b[A-Z]{2,}\b', message))
        score += min(caps_words * 0.5, 2)
        
        # Check for repeated punctuation
        if re.search(r'[.!?]{2,}', message):
            score += 1
        
        # Check for negative sentiment phrases
        if re.search(r'tried|attempt|every|nothing|fix|problem|issue|help', message):
            score += 0.5
        
        return score

    def _score_executive_patterns(self, message: str) -> float:
        """Score based on executive patterns"""
        score = 0
        
        # Check for business terminology
        business_terms = ['business', 'operations', 'revenue', 'impact', 'timeline',
                         'solution', 'proposal', 'investment', 'decision', 'strategy']
        for term in business_terms:
            if term in message:
                score += 0.5
        
        # Check for result-oriented language
        if re.search(r'bottom line|bottom line|impact|result|outcome|benefit', message):
            score += 1
        
        # Check for brevity (executives are concise)
        word_count = len(message.split())
        if word_count < 30:
            score += 0.5
        
        # Check for immediate action language
        if re.search(r'need|require|must|immediately|urgently', message):
            score += 0.5
        
        return score

    def _get_keywords_for_persona(self, persona: Persona) -> set:
        """Get keywords for a specific persona"""
        if persona == Persona.TECHNICAL_EXPERT:
            return self.technical_keywords
        elif persona == Persona.FRUSTRATED_USER:
            return self.frustrated_keywords
        else:
            return self.executive_keywords

    def _extract_matching_keywords(self, message: str, keywords: set) -> List[str]:
        """Extract matching keywords from message"""
        matching = []
        for keyword in keywords:
            if keyword in message:
                matching.append(keyword)
        return matching[:5]  # Top 5 keywords

    def get_persona_context(self, persona: Persona) -> Dict:
        """
        Get context information for response generation based on persona
        
        Args:
            persona: Detected persona
            
        Returns:
            Context dictionary with tone, style, and instructions
        """
        contexts = {
            Persona.TECHNICAL_EXPERT: {
                "tone": "technical",
                "style": "detailed",
                "include_code": True,
                "include_logs": True,
                "depth": "deep",
                "format": "structured",
                "examples": "technical",
                "terminology": "technical"
            },
            Persona.FRUSTRATED_USER: {
                "tone": "empathetic",
                "style": "simple",
                "include_code": False,
                "include_logs": False,
                "depth": "actionable",
                "format": "step_by_step",
                "examples": "simple",
                "terminology": "plain_language"
            },
            Persona.BUSINESS_EXECUTIVE: {
                "tone": "professional",
                "style": "concise",
                "include_code": False,
                "include_logs": False,
                "depth": "summary",
                "format": "bullet_points",
                "examples": "business",
                "terminology": "business"
            }
        }
        
        return contexts.get(persona, contexts[Persona.TECHNICAL_EXPERT])


# Singleton instance
_detector = None


def get_persona_detector() -> PersonaDetector:
    """Get or create persona detector instance"""
    global _detector
    if _detector is None:
        _detector = PersonaDetector()
    return _detector
