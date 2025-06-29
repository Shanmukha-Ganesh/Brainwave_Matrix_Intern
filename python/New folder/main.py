#!/usr/bin/env python3
"""
Inventory Management System
A comprehensive inventory management application with GUI
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.controllers.app_controller import AppController

def main():
    """Main application entry point"""
    try:
        app = AppController()
        app.start_application()
    except Exception as e:
        print(f"Application error: {str(e)}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
