import tkinter as tk
from tkinter import ttk, messagebox
from ..models.user import User
from ..utils.validators import Validator

class UserManagementFrame(ttk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.current_user = user
        self.user_model = User()
        
        # Only allow admin access
        if user['role'] != 'admin':
            ttk.Label(self, text="Access Denied: Admin privileges required", 
                     font=("Arial", 14)).pack(expand=True)
            return
        
        self.setup_ui()
        self.refresh()
    
    def setup_ui(self):
        # Title
        title_frame = ttk.Frame(self)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(title_frame, text="User Management", 
                 font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        
        ttk.Button(title_frame, text="Add New User", 
                  command=self.show_add_user_dialog).pack(side=tk.RIGHT)
        
        # Users list
        columns = ('ID', 'Username', 'Role', 'Created Date')
        self.users_tree = ttk.Treeview(self, columns=columns, show='headings')
        
        for col in columns:
            self.users_tree.heading(col, text=col)
        
        self.users_tree.column('ID', width=50)
        self.users_tree.column('Username', width=150)
        self.users_tree.column('Role', width=100)
        self.users_tree.column('Created Date', width=150)
        
        # Scrollbar
        users_scroll = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=users_scroll.set)
        
        self.users_tree

        self.users_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=5)
        users_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=5, padx=(0, 10))
        
        # Context menu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Delete User", command=self.delete_user)
        
        # Bind right-click
        self.users_tree.bind("<Button-3>", self.show_context_menu)
    
    def refresh(self):
        """Refresh users list"""
        # Clear existing items
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # Load users
        users = self.user_model.get_all_users()
        for user in users:
            user_id, username, role, created_at = user
            
            # Format date
            date_formatted = created_at[:19] if created_at else ""
            
            self.users_tree.insert('', tk.END, values=(
                user_id, username, role.title(), date_formatted
            ))
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        selection = self.users_tree.selection()
        if selection:
            self.context_menu.post(event.x_root, event.y_root)
    
    def show_add_user_dialog(self):
        """Show add user dialog"""
        AddUserDialog(self, self.user_model, self.refresh)
    
    def delete_user(self):
        """Delete selected user"""
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return
        
        item = self.users_tree.item(selection[0])
        user_id = item['values'][0]
        username = item['values'][1]
        
        # Prevent deleting current user
        if user_id == self.current_user['id']:
            messagebox.showerror("Error", "Cannot delete your own account")
            return
        
        # Confirm deletion
        result = messagebox.askyesno("Confirm Delete", 
                                   f"Are you sure you want to delete user '{username}'?\n"
                                   "This action cannot be undone.")
        if not result:
            return
        
        try:
            # Note: We need to add delete_user method to User model
            messagebox.showinfo("Info", "User deletion feature needs to be implemented in the User model")
            # self.user_model.delete_user(user_id)
            # self.refresh()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete user: {str(e)}")

class AddUserDialog:
    def __init__(self, parent, user_model, refresh_callback):
        self.user_model = user_model
        self.refresh_callback = refresh_callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New User")
        self.dialog.geometry("350x250")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
        self.center_dialog(parent)
    
    def center_dialog(self, parent):
        self.dialog.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (350 // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (250 // 2)
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
        
        # Confirm Password
        ttk.Label(main_frame, text="Confirm Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.confirm_password_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.confirm_password_var, show="*", width=20).grid(
            row=2, column=1, pady=5, padx=(10, 0))
        
        # Role
        ttk.Label(main_frame, text="Role:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.role_var = tk.StringVar(value="user")
        role_combo = ttk.Combobox(main_frame, textvariable=self.role_var, 
                                values=["user", "admin"], state="readonly", width=17)
        role_combo.grid(row=3, column=1, pady=5, padx=(10, 0))
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Create User", command=self.create_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def create_user(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()
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
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        # Create user
        if self.user_model.create_user(username, password, role):
            messagebox.showinfo("Success", "User created successfully!")
            self.refresh_callback()
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "Username already exists!")
