"""Escalation Handler and Human Handoff

This module manages conversation escalation and generates
structured handoff summaries for human agents.
"""

import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from src.persona_detector import Persona
from config import config

logger = logging.getLogger(__name__)


class EscalationHandler:
    """Handle escalation of conversations to human agents"""

    # Keywords that trigger escalation
    ESCALATION_TRIGGERS = {
        "billing": ["billing", "invoice", "payment", "charge", "refund", "subscription"],
        "account": ["account", "locked", "suspended", "ban", "deleted"],
        "legal": ["legal", "lawsuit", "terms", "contract", "violation"],
        "security": ["security", "breach", "leak", "hack", "compromised"],
    }

    def __init__(self):
        """Initialize escalation handler"""
        self.max_attempts = 3
        self.confidence_threshold = config.ESCALATION_THRESHOLD

    def should_escalate(
        self,
        response: Dict,
        attempt_count: int,
        user_satisfied: bool = False
    ) -> Tuple[bool, str]:
        """
        Determine if conversation should be escalated
        
        Args:
            response: Generated response with metadata
            attempt_count: Number of previous attempts
            user_satisfied: Whether user is satisfied
            
        Returns:
            Tuple of (should_escalate, reason)
        """
        # Check if escalation was already flagged by response generator
        if response.get("escalation_required"):
            return True, response.get("escalation_reason", "Automatic escalation requested")
        
        # Check if confidence is too low
        if response.get("confidence", 1.0) < self.confidence_threshold:
            return True, "Low confidence response - escalating to specialist"
        
        # Check if user has tried multiple times without satisfaction
        if attempt_count >= self.max_attempts and not user_satisfied:
            return True, f"Maximum attempts ({self.max_attempts}) reached without resolution"
        
        # Check for escalation trigger keywords in response or previous context
        # (would need access to full context in real implementation)
        
        return False, ""

    def check_trigger_keywords(self, message: str) -> Optional[str]:
        """
        Check if message contains keywords that trigger escalation
        
        Args:
            message: User message
            
        Returns:
            Escalation category if found, None otherwise
        """
        message_lower = message.lower()
        
        for category, keywords in self.ESCALATION_TRIGGERS.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return category
        
        return None

    def generate_handoff_summary(
        self,
        persona: Persona,
        issue: str,
        conversation_history: List[Dict],
        retrieved_docs: List[Dict],
        attempts_made: List[Dict],
        escalation_reason: str
    ) -> Dict:
        """
        Generate structured handoff summary for human agent
        
        Args:
            persona: Detected customer persona
            issue: User's issue description
            conversation_history: Full conversation history
            retrieved_docs: Documents retrieved during resolution attempt
            attempts_made: List of resolution attempts
            escalation_reason: Reason for escalation
            
        Returns:
            Structured handoff summary
        """
        
        # Extract key information
        sources_used = list(set(doc.get("source", "").split("/")[-1] for doc in retrieved_docs))
        attempted_steps = [attempt.get("action", "") for attempt in attempts_made if attempt.get("action")]
        
        handoff_summary = {
            "timestamp": datetime.utcnow().isoformat(),
            "customer_persona": persona.value,
            "issue_summary": {
                "description": issue,
                "category": self._categorize_issue(issue)
            },
            "conversation_overview": {
                "total_messages": len(conversation_history),
                "last_message": conversation_history[-1] if conversation_history else None,
                "sentiment": self._analyze_sentiment(conversation_history)
            },
            "attempted_resolution": {
                "attempts_count": len(attempts_made),
                "steps_taken": attempted_steps,
                "documents_referenced": sources_used,
                "success_indicators": self._extract_success_indicators(attempts_made)
            },
            "escalation_details": {
                "reason": escalation_reason,
                "escalation_triggers": self._identify_escalation_triggers(issue),
                "required_access": self._determine_required_access(persona, issue)
            },
            "customer_context": {
                "frustration_level": self._assess_frustration_level(persona, conversation_history),
                "technical_proficiency": self._assess_technical_level(persona),
                "preferred_communication": self._determine_communication_preference(persona)
            },
            "recommended_next_steps": self._generate_recommendations(
                persona, issue, sources_used, attempted_steps
            ),
            "urgency_level": self._assess_urgency(issue, escalation_reason)
        }
        
        logger.info(f"Handoff summary generated for {persona.value} with urgency {handoff_summary['urgency_level']}")
        
        return handoff_summary

    def _categorize_issue(self, issue: str) -> str:
        """Categorize the issue"""
        categories = {
            "billing": ["billing", "invoice", "payment", "charge", "refund"],
            "technical": ["error", "api", "sync", "configuration", "debug"],
            "account": ["account", "login", "password", "profile"],
            "performance": ["slow", "latency", "timeout", "speed"],
            "security": ["security", "breach", "encryption", "access"],
            "other": []
        }
        
        issue_lower = issue.lower()
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in issue_lower:
                    return category
        
        return "other"

    def _analyze_sentiment(self, conversation_history: List[Dict]) -> str:
        """Analyze overall sentiment from conversation"""
        if not conversation_history:
            return "neutral"
        
        # Simple sentiment analysis based on keywords
        positive_words = ["thank", "great", "perfect", "excellent", "working"]
        negative_words = ["frustrated", "angry", "broken", "not working", "terrible"]
        
        text = " ".join([msg.get("user", "") for msg in conversation_history]).lower()
        
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        if negative_count > positive_count:
            return "negative"
        elif positive_count > negative_count:
            return "positive"
        else:
            return "neutral"

    def _extract_success_indicators(self, attempts_made: List[Dict]) -> Dict:
        """Extract indicators of what worked or didn't work"""
        indicators = {
            "partial_success": False,
            "patterns_identified": [],
            "failed_solutions": []
        }
        
        for attempt in attempts_made:
            if attempt.get("success"):
                indicators["partial_success"] = True
            if attempt.get("pattern"):
                indicators["patterns_identified"].append(attempt["pattern"])
            if attempt.get("failed"):
                indicators["failed_solutions"].append(attempt.get("attempted_solution"))
        
        return indicators

    def _identify_escalation_triggers(self, issue: str) -> List[str]:
        """Identify specific escalation triggers"""
        triggers = []
        issue_lower = issue.lower()
        
        for category, keywords in self.ESCALATION_TRIGGERS.items():
            for keyword in keywords:
                if keyword in issue_lower:
                    triggers.append(category.upper())
        
        return list(set(triggers))  # Remove duplicates

    def _determine_required_access(self, persona: Persona, issue: str) -> Dict:
        """Determine what access human agent needs"""
        access = {
            "requires_account_access": "account" in issue.lower() or "billing" in issue.lower(),
            "requires_backend_access": "database" in issue.lower() or "server" in issue.lower(),
            "requires_logs_access": "error" in issue.lower() or "debug" in issue.lower(),
            "requires_api_access": "api" in issue.lower()
        }
        return access

    def _assess_frustration_level(self, persona: Persona, history: List[Dict]) -> str:
        """Assess customer frustration level"""
        if persona == Persona.FRUSTRATED_USER:
            return "high"
        
        # Check history for escalating frustration
        frustration_words = ["frustrated", "angry", "help", "please", "desperate"]
        recent_text = " ".join([msg.get("user", "") for msg in history[-3:]]).lower()
        
        count = sum(1 for word in frustration_words if word in recent_text)
        
        if count >= 2:
            return "high"
        elif count == 1:
            return "medium"
        else:
            return "low"

    def _assess_technical_level(self, persona: Persona) -> str:
        """Assess customer's technical proficiency"""
        if persona == Persona.TECHNICAL_EXPERT:
            return "high"
        elif persona == Persona.BUSINESS_EXECUTIVE:
            return "low"
        else:
            return "medium"

    def _determine_communication_preference(self, persona: Persona) -> str:
        """Determine preferred communication style"""
        preferences = {
            Persona.TECHNICAL_EXPERT: "detailed_technical",
            Persona.FRUSTRATED_USER: "empathetic_simple",
            Persona.BUSINESS_EXECUTIVE: "concise_executive"
        }
        return preferences.get(persona, "standard")

    def _generate_recommendations(
        self,
        persona: Persona,
        issue: str,
        sources: List[str],
        attempts: List[str]
    ) -> List[str]:
        """Generate recommendations for human agent"""
        recommendations = []
        
        # Generic recommendations
        if not sources:
            recommendations.append("Review knowledge base for similar cases")
        
        if len(attempts) > 0:
            recommendations.append(f"Note that {len(attempts)} solutions were already attempted")
        
        # Persona-specific recommendations
        if persona == Persona.TECHNICAL_EXPERT:
            recommendations.append("Provide detailed technical explanation and code examples")
            recommendations.append("Offer direct access to logs or debugging tools")
        elif persona == Persona.FRUSTRATED_USER:
            recommendations.append("Lead with empathy and reassurance")
            recommendations.append("Provide step-by-step guidance")
        else:
            recommendations.append("Focus on business impact and timeline")
            recommendations.append("Provide executive summary of solution")
        
        return recommendations

    def _assess_urgency(self, issue: str, escalation_reason: str) -> str:
        """Assess urgency of escalation"""
        critical_keywords = ["critical", "down", "broken", "loss", "security", "breach"]
        high_keywords = ["urgent", "asap", "important", "business impact"]
        
        full_text = (issue + " " + escalation_reason).lower()
        
        for keyword in critical_keywords:
            if keyword in full_text:
                return "CRITICAL"
        
        for keyword in high_keywords:
            if keyword in full_text:
                return "HIGH"
        
        return "NORMAL"


# Singleton instance
_escalation_handler = None


def get_escalation_handler() -> EscalationHandler:
    """Get or create escalation handler instance"""
    global _escalation_handler
    if _escalation_handler is None:
        _escalation_handler = EscalationHandler()
    return _escalation_handler
