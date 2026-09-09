#!/usr/bin/env python3
"""
AI Knowledge Assistant - Main Entry Point
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.config import Config
from core.agent import AIAgent
from ui.console import ConsoleUI


def main():
    """Main application entry point"""
    try:
        # Initialize configuration
        config = Config("config.json")
        print(f"✅ Configuration loaded: {config.get('app_name')} v{config.get('version')}")
        
        # Initialize AI Agent
        agent = AIAgent(config)
        print("✅ AI Agent initialized")
        
        # Initialize Console UI
        ui = ConsoleUI(agent, config)
        
        # Run application
        ui.run()
        
        print("\n✅ Thank you for using AI Knowledge Assistant!")
        print("Goodbye! 👋\n")
    
    except ValueError as e:
        print(f"\n❌ Configuration Error: {str(e)}")
        print("\n📝 Setup Instructions:")
        print("1. Copy .env.example to .env")
        print("2. Add your OpenAI API key to .env")
        print("3. See SETUP.md for detailed instructions\n")
        sys.exit(1)
    
    except ImportError as e:
        print(f"\n❌ Import Error: {str(e)}")
        print("\n📝 Please install dependencies:")
        print("pip install -r requirements.txt\n")
        sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n✅ Application terminated by user")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ Unexpected Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
