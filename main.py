#!/usr/bin/env python3
"""
AI Knowledge Assistant - Main Entry Point
🤖 Intelligent Question Answering System with Knowledge Base
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from ui.console import ConsoleUI
from core.config import Config
from core.agent import AIAgent


def main():
    """Main application entry point"""
    try:
        # Load configuration
        config = Config()
        
        # Initialize AI Agent
        agent = AIAgent(config)
        
        # Initialize Console UI
        ui = ConsoleUI(agent, config)
        
        # Run the application
        ui.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thank you for using AI Knowledge Assistant.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
