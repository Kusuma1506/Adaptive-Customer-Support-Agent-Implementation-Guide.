"""Command-Line Interface for Support Agent Testing

Run this script to test the support agent from command line:
    python -m src.cli
"""

import sys
import logging
from typing import List
from src.main import get_support_agent, initialize_support_system
from src.persona_detector import Persona

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CLIInterface:
    """Command-line interface for support agent"""

    def __init__(self):
        """Initialize CLI"""
        self.agent = None
        self.test_queries = {
            "1": {
                "query": "Can you explain the API authentication failure and provide error details?",
                "expected_persona": Persona.TECHNICAL_EXPERT.value
            },
            "2": {
                "query": "I've been trying to set up my sync for hours and nothing works! Please help me!",
                "expected_persona": Persona.FRUSTRATED_USER.value
            },
            "3": {
                "query": "How does this issue impact operations and when will it be resolved?",
                "expected_persona": Persona.BUSINESS_EXECUTIVE.value
            }
        }

    def initialize(self) -> bool:
        """Initialize the support system"""
        print("\n" + "="*60)
        print("🚀 Initializing Persona-Adaptive Support Agent")
        print("="*60)
        
        result = initialize_support_system()
        
        if result.get("status") == "initialized":
            print("✅ System initialized successfully!")
            print(f"📚 Knowledge base: {result['knowledge_base']['total_chunks']} chunks")
            self.agent = get_support_agent(initialize_kb=False)
            return True
        else:
            print(f"❌ Initialization failed: {result.get('error_message')}")
            return False

    def run(self):
        """Run CLI interface"""
        if not self.initialize():
            return
        
        self.show_menu()

    def show_menu(self):
        """Show main menu"""
        while True:
            print("\n" + "="*60)
            print("📋 Main Menu")
            print("="*60)
            print("1. Run Test Scenario (Technical Expert)")
            print("2. Run Test Scenario (Frustrated User)")
            print("3. Run Test Scenario (Business Executive)")
            print("4. Custom Query")
            print("5. View Conversation History")
            print("6. View Session Summary")
            print("7. Reset Conversation")
            print("8. Exit")
            print("="*60)
            
            choice = input("Select option (1-8): ").strip()
            
            if choice in ["1", "2", "3"]:
                self.run_test_scenario(choice)
            elif choice == "4":
                self.run_custom_query()
            elif choice == "5":
                self.show_conversation_history()
            elif choice == "6":
                self.show_session_summary()
            elif choice == "7":
                self.reset_conversation()
            elif choice == "8":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid option. Please try again.")

    def run_test_scenario(self, scenario_id: str):
        """Run predefined test scenario"""
        if scenario_id not in self.test_queries:
            print("❌ Invalid scenario")
            return
        
        scenario = self.test_queries[scenario_id]
        query = scenario["query"]
        expected_persona = scenario["expected_persona"]
        
        print(f"\n{'='*60}")
        print(f"🧪 Test Scenario {scenario_id}")
        print(f"{'='*60}")
        print(f"📝 Query: {query}")
        print(f"👤 Expected Persona: {expected_persona}")
        print(f"{'='*60}\n")
        
        self.process_query(query)

    def run_custom_query(self):
        """Process custom user query"""
        print("\n" + "="*60)
        print("✍️  Enter Your Query")
        print("="*60)
        query = input("Query: ").strip()
        
        if not query:
            print("❌ Query cannot be empty")
            return
        
        self.process_query(query)

    def process_query(self, query: str):
        """Process a query and display response"""
        print("\n⏳ Processing message...")
        
        try:
            response = self.agent.process_message(query)
            
            print("\n" + "="*60)
            print("💬 Support Agent Response")
            print("="*60)
            
            # Display response
            print(f"\n📝 Response:\n{response['response']}\n")
            
            # Display metadata
            print(f"{'─'*60}")
            print("📊 Metadata:")
            print(f"{'─'*60}")
            print(f"👤 Detected Persona: {response['persona']}")
            print(f"📈 Confidence: {response['persona_confidence']:.1%}")
            
            if response['persona_keywords']:
                print(f"🔑 Keywords: {', '.join(response['persona_keywords'][:5])}")
            
            if response['retrieved_sources']:
                print(f"📚 Sources Used: {', '.join([s.split('/')[-1].replace('.md', '') for s in response['retrieved_sources']])}")
                print(f"🎯 Retrieval Confidence: {response['retrieval_confidence']:.1%}")
            
            print(f"📋 Documents Used: {response['context_documents_used']}")
            print(f"🔄 Attempt #: {response['attempt_number']}")
            
            # Display escalation if applicable
            if response['escalated']:
                print(f"\n{'─'*60}")
                print("⚠️  ESCALATION ALERT")
                print(f"{'─'*60}")
                print(f"Reason: {response['escalation_reason']}")
                
                if response['handoff_summary']:
                    print(f"\n📋 Handoff Summary:")
                    self.print_handoff_summary(response['handoff_summary'])
            
            print(f"\n{'='*60}\n")
            
        except Exception as e:
            print(f"❌ Error processing query: {str(e)}")
            logger.error(f"Error: {str(e)}", exc_info=True)

    def print_handoff_summary(self, summary: dict, indent: int = 0):
        """Pretty print handoff summary"""
        prefix = "  " * indent
        
        for key, value in summary.items():
            if isinstance(value, dict):
                print(f"{prefix}{key}:")
                self.print_handoff_summary(value, indent + 1)
            elif isinstance(value, list):
                print(f"{prefix}{key}: {', '.join(str(v) for v in value)}")
            else:
                print(f"{prefix}{key}: {value}")

    def show_conversation_history(self):
        """Display conversation history"""
        history = self.agent.get_conversation_history()
        
        if not history:
            print("❌ No conversation history yet")
            return
        
        print("\n" + "="*60)
        print("📜 Conversation History")
        print("="*60)
        
        for i, msg in enumerate(history, 1):
            role = "👤 User" if msg.get("user") else "🤖 Agent"
            text = msg.get("user", msg.get("assistant", ""))
            persona = msg.get("persona", "")
            
            print(f"\n[{i}] {role}")
            if persona:
                print(f"   📌 Persona: {persona}")
            print(f"   {text[:100]}..." if len(text) > 100 else f"   {text}")

    def show_session_summary(self):
        """Display session summary"""
        summary = self.agent.get_session_summary()
        
        print("\n" + "="*60)
        print("📊 Session Summary")
        print("="*60)
        
        if summary.get("status") == "no_conversation":
            print("❌ No active conversation")
            return
        
        print(f"Total Messages: {summary['total_messages']}")
        print(f"Total Attempts: {summary['total_attempts']}")
        print(f"Average Confidence: {summary['average_confidence']:.1%}")
        print(f"Escalated: {'Yes ⚠️' if summary['escalated'] else 'No ✅'}")
        print(f"Session Duration: {summary['session_duration']}")
        
        if summary['personas_detected']:
            print(f"Personas Detected: {', '.join(summary['personas_detected'])}")

    def reset_conversation(self):
        """Reset conversation"""
        confirm = input("\n⚠️  Reset conversation? (y/n): ").strip().lower()
        
        if confirm == 'y':
            self.agent.reset_conversation()
            print("✅ Conversation reset")
        else:
            print("❌ Reset cancelled")


def main():
    """Main entry point"""
    cli = CLIInterface()
    cli.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
