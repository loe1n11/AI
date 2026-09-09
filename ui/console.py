"""
Console UI - Command-line interface for AI Assistant
"""

import os
from typing import Optional
from core.agent import AIAgent
from core.config import Config


class ConsoleUI:
    """Console user interface"""
    
    def __init__(self, agent: AIAgent, config: Config):
        """Initialize console UI"""
        self.agent = agent
        self.config = config
        self.running = False
    
    def run(self) -> None:
        """Run the console interface"""
        self.running = True
        self._print_welcome()
        
        while self.running:
            try:
                self._print_menu()
                choice = input("\n📋 Enter your choice: ").strip().lower()
                self._handle_choice(choice)
            
            except KeyboardInterrupt:
                self.running = False
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    def _print_welcome(self) -> None:
        """Print welcome message"""
        print("\n" + "="*50)
        print("🤖 AI Knowledge Assistant v2.0")
        print("="*50)
        print("Welcome! I'm your AI-powered knowledge assistant.")
        print("I can answer questions based on your knowledge base.\n")
    
    def _print_menu(self) -> None:
        """Print main menu"""
        print("\n" + "-"*50)
        print("📋 MAIN MENU")
        print("-"*50)
        print("1. 🔍 Ask a question")
        print("2. 🌐 Add website to knowledge base")
        print("3. 📊 Show database statistics")
        print("4. 🗑️  Clear knowledge base")
        print("5. ❌ Exit")
        print("-"*50)
    
    def _handle_choice(self, choice: str) -> None:
        """Handle menu choice"""
        if choice == "1":
            self._ask_question()
        elif choice == "2":
            self._add_website()
        elif choice == "3":
            self._show_stats()
        elif choice == "4":
            self._clear_database()
        elif choice == "5":
            self.running = False
        else:
            print("❌ Invalid choice. Please try again.")
    
    def _ask_question(self) -> None:
        """Ask a question"""
        question = input("\n❓ Enter your question: ").strip()
        
        if not question:
            print("❌ Question cannot be empty!")
            return
        
        print("\n🤔 Thinking...")
        answer = self.agent.answer_question(question)
        print(f"\n💬 Answer:\n{answer}")
    
    def _add_website(self) -> None:
        """Add website to knowledge base"""
        url = input("\n🌐 Enter website URL: ").strip()
        
        if not url:
            print("❌ URL cannot be empty!")
            return
        
        print("\n⏳ Processing website...")
        success = self.agent.add_website(url)
        
        if success:
            print(f"✅ Website added successfully!")
        else:
            print(f"❌ Failed to add website")
    
    def _show_stats(self) -> None:
        """Show database statistics"""
        stats = self.agent.get_stats()
        
        print("\n📊 Database Statistics:")
        print("-"*50)
        for key, value in stats.items():
            print(f"  {key}: {value}")
        print("-"*50)
    
    def _clear_database(self) -> None:
        """Clear knowledge base"""
        confirm = input("\n⚠️  Are you sure? (yes/no): ").strip().lower()
        
        if confirm == "yes":
            success = self.agent.clear_database()
            if success:
                print("✅ Knowledge base cleared!")
            else:
                print("❌ Failed to clear database")
        else:
            print("❌ Cancelled.")
