"""
Configuration settings for the Inventory Management System
"""

import os

# Database configuration
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'inventory.db')

# Application settings
APP_NAME = "Inventory Management System"
APP_VERSION = "1.0.0"

# Default user settings
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"

# UI settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Report settings
EXPORT_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'exports')

# Low stock alert settings
DEFAULT_MIN_STOCK_LEVEL = 10
LOW_STOCK_WARNING_COLOR = "#fff2cc"
OUT_OF_STOCK_ERROR_COLOR = "#ffcccc"
IN_STOCK_SUCCESS_COLOR = "#ccffcc"
