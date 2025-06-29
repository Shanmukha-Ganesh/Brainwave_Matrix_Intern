import tkinter as tk
from tkinter import ttk, messagebox
from .product_management import ProductManagementFrame
from .inventory_management import InventoryManagementFrame
from .reports import ReportsFrame
from .user_management import UserManagementFrame

class MainWindow:
    def __init__(self, user):
        self.user = user
        
        self.root = tk.Tk()
        self.root.title(f"Inventory Management System - {user['username']} ({user['role']})")
        self.root.geometry("1200x800")
        self.root.state('zoomed')  # Maximize window on Windows
        
        self.setup_ui()
    
    def setup_ui(self):
        # Create menu bar
        self.create_menu()
        
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Add tabs
        self.add_tabs()
        
        # Status bar
        self.create_status_bar()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Refresh All", command=self.refresh_all_tabs)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def add_tabs(self):
        # Product Management Tab
        self.product_frame = ProductManagementFrame(self.notebook, self.user)
        self.notebook.add(self.product_frame, text="Products")
        
        # Inventory Management Tab
        self.inventory_frame = InventoryManagementFrame(self.notebook, self.user)
        self.notebook.add(self.inventory_frame, text="Inventory")
        
        # Reports Tab
        self.reports_frame = ReportsFrame(self.notebook, self.user)
        self.notebook.add(self.reports_frame, text="Reports")
        
        # User Management Tab (Admin only)
        if self.user['role'] == 'admin':
            self.user_frame = UserManagementFrame(self.notebook, self.user)
            self.notebook.add(self.user_frame, text="Users")
    
    def create_status_bar(self):
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(self.status_bar, text="Ready")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # User info
        user_info = ttk.Label(self.status_bar, 
                             text=f"Logged in as: {self.user['username']} ({self.user['role']})")
        user_info.pack(side=tk.RIGHT, padx=5)
    
    def refresh_all_tabs(self):
        try:
            self.product_frame.refresh()
            self.inventory_frame.refresh()
            self.reports_frame.refresh()
            if hasattr(self, 'user_frame'):
                self.user_frame.refresh()
            self.status_label.config(text="All tabs refreshed")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh: {str(e)}")
    
    def show_about(self):
        messagebox.showinfo("About", 
                           "Inventory Management System v1.0\n"
                           "Built with Python and Tkinter\n"
                           "© 2024")
    
    def run(self):
        self.root.mainloop()
