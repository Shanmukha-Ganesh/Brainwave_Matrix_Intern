import tkinter as tk
from tkinter import ttk, messagebox
from ..models.user import User
from ..utils.validators import Validator

class LoginWindow:
    def __init__(self, on_login_success):
        self.on_login_success = on_login_success
        self.user_model = User()
        self.current_user = None
        
        self.root = tk.Tk()
        self.root.title("Inventory Management System - Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        self.setup_ui()
        self.center_window()
    
    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (300 // 2)
        self.root.geometry(f"400x300+{x}+{y}")
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Inventory Management System", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Username
        ttk.Label(main_frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(main_frame, textvariable=self.username_var, width=25)
        username_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Password
        ttk.Label(main_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(main_frame, textvariable=self.password_var, 
                                 show="*", width=25)

        password_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # Login button
        login_btn = ttk.Button(main_frame, text="Login", command=self.login)
        login_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Create user button (for admin)
        create_user_btn = ttk.Button(main_frame, text="Create New User", 
                                   command=self.show_create_user_dialog)
        create_user_btn.grid(row=4, column=0, columnspan=2, pady=5)
        
        # Default credentials info
        info_label = ttk.Label(main_frame, text="Default: admin / admin123", 
                              font=("Arial", 9), foreground="gray")
        info_label.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda e: self.login())
        username_entry.focus()
    
    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        user = self.user_model.authenticate(username, password)
        if user:
            self.current_user = user
            self.root.destroy()
            self.on_login_success(user)
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.password_var.set("")
    
    def show_create_user_dialog(self):
        CreateUserDialog(self.root, self.user_model)
    
    def run(self):
        self.root.mainloop()

class CreateUserDialog:
    def __init__(self, parent, user_model):
        self.user_model = user_model
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Create New User")
        self.dialog.geometry("350x250")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
        self.center_dialog(parent)
    
    def center_dialog(self, parent):
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (350 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (250 // 2)
        self.dialog.geometry(f"350x250+{x}+{y}")
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Username
        ttk.Label(main_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.username_var, width=20).grid(
            row=0, column=1, pady=5, padx=(10, 0))
        
        # Password
        ttk.Label(main_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.password_var, show="*", width=20).grid(
            row=1, column=1, pady=5, padx=(10, 0))
        
        # Role
        ttk.Label(main_frame, text="Role:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.role_var = tk.StringVar(value="user")
        role_combo = ttk.Combobox(main_frame, textvariable=self.role_var, 
                                values=["user", "admin"], state="readonly", width=17)
        role_combo.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Create", command=self.create_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def create_user(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        role = self.role_var.get()
        
        # Validate input
        valid, msg = Validator.validate_username(username)
        if not valid:
            messagebox.showerror("Error", msg)
            return
        
        valid, msg = Validator.validate_password(password)
        if not valid:
            messagebox.showerror("Error", msg)
            return
        
        # Create user
        if self.user_model.create_user(username, password, role):
            messagebox.showinfo("Success", "User created successfully!")
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "Username already exists!")
