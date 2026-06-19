"""Streamlit UI for Persona-Adaptive Customer Support Agent"""

import streamlit as st
import json
import logging
from typing import Dict, List
from datetime import datetime
import sys
sys.path.insert(0, '/'.join(__file__.split('/')[:-2]))

from src.main import get_support_agent, initialize_support_system
from src.persona_detector import Persona

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="CloudSync Pro Support Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .persona-badge {
        display: inline-block;
        padding: 8px 12px;
        border-radius: 20px;
        font-weight: bold;
        margin: 5px 0;
    }
    .technical { background-color: #e3f2fd; color: #1976d2; }
    .frustrated { background-color: #fff3e0; color: #f57c00; }
    .executive { background-color: #f3e5f5; color: #7b1fa2; }
    .escalation-warning { background-color: #ffebee; padding: 15px; border-left: 4px solid #d32f2f; border-radius: 4px; }
    .confidence-badge { margin: 5px 0; }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state"""
    if "agent" not in st.session_state:
        st.session_state.agent = None
        st.session_state.initialization_status = None
        
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if "system_initialized" not in st.session_state:
        st.session_state.system_initialized = False


def initialize_system():
    """Initialize the support system"""
    if not st.session_state.system_initialized:
        with st.spinner("🔄 Initializing support system..."):
            result = initialize_support_system()
            st.session_state.system_initialized = result.get("status") == "initialized"
            st.session_state.initialization_status = result
            
            if st.session_state.system_initialized:
                st.session_state.agent = get_support_agent(initialize_kb=False)
                st.success("✅ Support system initialized!")
                st.info(f"📚 Knowledge base: {result['knowledge_base']['total_chunks']} chunks loaded")
            else:
                st.error(f"❌ Initialization failed: {result.get('error_message')}")


def render_persona_badge(persona: str, confidence: float):
    """Render persona detection badge"""
    persona_class = {
        "Technical Expert": "technical",
        "Frustrated User": "frustrated",
        "Business Executive": "executive"
    }.get(persona, "technical")
    
    st.markdown(
        f'<div class="persona-badge {persona_class}">👤 {persona} ({confidence:.1%} confidence)</div>',
        unsafe_allow_html=True
    )


def render_source_badge(sources: List[str], confidence: float):
    """Render source retrieval information"""
    if sources:
        st.markdown(f'📖 **Sources used:** {", ".join([s.replace(".md", "") for s in sources])}')
        st.markdown(f'🎯 **Retrieval confidence:** {confidence:.1%}')
    else:
        st.warning("⚠️ No relevant sources found in knowledge base")


def render_escalation_alert(escalation_reason: str, handoff_summary: Dict):
    """Render escalation alert and handoff summary"""
    st.markdown(
        f'<div class="escalation-warning">⚠️ <b>This conversation has been escalated to a human agent</b><br/>'
        f'<small>Reason: {escalation_reason}</small></div>',
        unsafe_allow_html=True
    )
    
    if handoff_summary:
        with st.expander("📋 View Handoff Summary for Agent"):
            st.json(handoff_summary, expanded=False)


def render_chat_interface():
    """Render main chat interface"""
    st.header("💬 CloudSync Pro Support Agent")
    st.markdown("---")
    
    # Initialize agent if not already done
    if not st.session_state.system_initialized:
        initialize_system()
        return
    
    # Display conversation history
    if st.session_state.messages:
        for i, message in enumerate(st.session_state.messages):
            if message["type"] == "user":
                st.chat_message("user").write(message["content"])
            elif message["type"] == "assistant":
                with st.chat_message("assistant"):
                    st.write(message["content"])
                    
                    # Display metadata
                    col1, col2 = st.columns(2)
                    with col1:
                        render_persona_badge(message["persona"], message["confidence"])
                    with col2:
                        if message.get("retrieval_confidence"):
                            st.markdown(f'🎯 Retrieval confidence: **{message["retrieval_confidence"]:.1%}**')
                    
                    # Display sources
                    if message.get("sources"):
                        render_source_badge(message["sources"], message.get("retrieval_confidence", 0))
                    
                    # Display escalation if applicable
                    if message.get("escalated"):
                        render_escalation_alert(
                            message.get("escalation_reason", "Unknown reason"),
                            message.get("handoff_summary")
                        )
                    
                    st.markdown("---")
    
    # Chat input
    user_input = st.chat_input("Type your message here... (e.g., 'Can you explain the API authentication failure?')")
    
    if user_input:
        # Add user message to history
        st.session_state.messages.append({
            "type": "user",
            "content": user_input
        })
        
        # Process message
        with st.spinner("🔄 Processing your message..."):
            try:
                response_data = st.session_state.agent.process_message(user_input)
                
                # Add assistant response to history
                st.session_state.messages.append({
                    "type": "assistant",
                    "content": response_data["response"],
                    "persona": response_data["persona"],
                    "confidence": response_data["persona_confidence"],
                    "sources": response_data["retrieved_sources"],
                    "retrieval_confidence": response_data["retrieval_confidence"],
                    "escalated": response_data["escalated"],
                    "escalation_reason": response_data["escalation_reason"],
                    "handoff_summary": response_data["handoff_summary"],
                    "attempt_number": response_data["attempt_number"]
                })
                
                # Rerun to display the new message
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error processing message: {str(e)}")
                logger.error(f"Error: {str(e)}", exc_info=True)


def render_sidebar():
    """Render sidebar with options and statistics"""
    with st.sidebar:
        st.title("⚙️ Configuration")
        
        # System status
        if st.session_state.system_initialized:
            st.success("✅ System Ready")
            
            if st.session_state.agent:
                kb_stats = st.session_state.agent.get_knowledge_base_stats()
                st.info(f"📚 **Knowledge Base**: {kb_stats.get('total_chunks', 0)} chunks")
        else:
            st.warning("⏳ Initializing system...")
        
        st.markdown("---")
        
        # Session controls
        st.subheader("📊 Session Info")
        
        if st.session_state.messages and st.session_state.agent:
            session_summary = st.session_state.agent.get_session_summary()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Messages", session_summary["total_messages"])
                st.metric("Attempts", session_summary["total_attempts"])
            with col2:
                st.metric("Avg Confidence", f"{session_summary['average_confidence']:.1%}")
                escalated = "Yes ⚠️" if session_summary["escalated"] else "No ✅"
                st.metric("Escalated", escalated)
            
            # Personas detected
            if session_summary["personas_detected"]:
                st.markdown("**Personas Detected:**")
                for persona in session_summary["personas_detected"]:
                    st.caption(f"• {persona}")
        
        st.markdown("---")
        
        # Test scenarios
        st.subheader("🧪 Test Scenarios")
        
        test_scenarios = {
            "Technical Expert": "Can you explain the API authentication failure and provide error details?",
            "Frustrated User": "I've been trying to set up my sync for hours and nothing works! Please help me!",
            "Business Executive": "How does this issue impact operations and when will it be resolved?"
        }
        
        selected_scenario = st.selectbox(
            "Load test message:",
            ["None"] + list(test_scenarios.keys())
        )
        
        if selected_scenario != "None":
            st.session_state.test_message = test_scenarios[selected_scenario]
            if st.button("📨 Use Test Message"):
                st.session_state.messages.append({
                    "type": "user",
                    "content": st.session_state.test_message
                })
                st.rerun()
        
        st.markdown("---")
        
        # Reset conversation
        if st.button("🔄 New Conversation", use_container_width=True):
            if st.session_state.agent:
                st.session_state.agent.reset_conversation()
            st.session_state.messages = []
            st.success("Conversation reset!")
            st.rerun()
        
        # Download conversation
        if st.session_state.messages:
            conversation_json = json.dumps(st.session_state.messages, indent=2)
            st.download_button(
                label="📥 Download Conversation",
                data=conversation_json,
                file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        st.markdown("---")
        
        # Help and documentation
        st.subheader("📖 Help")
        
        st.markdown("""
        **How to use:**
        1. Type your support question
        2. Agent detects your persona
        3. System retrieves relevant docs
        4. Adaptive response is generated
        5. Escalates if needed

        **Supported Personas:**
        - 👨‍💻 **Technical Expert**: Detailed, technical responses
        - 😤 **Frustrated User**: Empathetic, simple steps
        - 💼 **Business Executive**: Concise, outcome-focused
        """)
        
        st.markdown("---")
        st.caption("🚀 CloudSync Pro Support Agent v1.0")


def main():
    """Main application entry point"""
    initialize_session_state()
    
    # Layout: sidebar + main content
    render_sidebar()
    render_chat_interface()


if __name__ == "__main__":
    main()
