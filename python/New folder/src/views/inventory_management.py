import tkinter as tk
from tkinter import ttk, messagebox
from ..models.product import Product
from ..models.transaction import Transaction

class InventoryManagementFrame(ttk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.product_model = Product()
        self.transaction_model = Transaction()
        
        self.setup_ui()
        self.refresh()
    
    def setup_ui(self):
        # Create notebook for sub-tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Stock Management Tab
        self.stock_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stock_frame, text="Stock Management")
        self.setup_stock_management()
        
        # Transaction History Tab
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="Transaction History")
        self.setup_transaction_history()
    
    def setup_stock_management(self):
        # Main container
        main_container = ttk.PanedWindow(self.stock_frame, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Products list
        left_frame = ttk.Frame(main_container)
        main_container.add(left_frame, weight=2)
        
        ttk.Label(left_frame, text="Products", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        # Products treeview
        columns = ('ID', 'Name', 'Current Stock', 'Min Stock', 'Status')
        self.stock_tree = ttk.Treeview(left_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.stock_tree.heading(col, text=col)
        
        self.stock_tree.column('ID', width=50)
        self.stock_tree.column('Name', width=200)
        self.stock_tree.column('Current Stock', width=100)
        self.stock_tree.column('Min Stock', width=100)
        self.stock_tree.column('Status', width=100)
        
        # Scrollbar
        stock_scroll = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.stock_tree.yview)
        self.stock_tree.configure(yscrollcommand=stock_scroll.set)
        
        self.stock_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        stock_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection
        self.stock_tree.bind('<<TreeviewSelect>>', self.on_stock_select)
        
        # Right panel - Stock operations
        right_frame = ttk.Frame(main_container)
        main_container.add(right_frame, weight=1)
        
        ttk.Label(right_frame, text="Stock Operations", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        # Selected product info
        info_frame = ttk.LabelFrame(right_frame, text="Selected Product", padding="10")
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.selected_product_label = ttk.Label(info_frame, text="No product selected")
        self.selected_product_label.pack()
        
        self.current_stock_label = ttk.Label(info_frame, text="")
        self.current_stock_label.pack()
        
        # Stock adjustment form
        adjustment_frame = ttk.LabelFrame(right_frame, text="Adjust Stock", padding="10")
        adjustment_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Transaction type
        ttk.Label(adjustment_frame, text="Transaction Type:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.transaction_type_var = tk.StringVar(value="restock")
        type_combo = ttk.Combobox(adjustment_frame, textvariable=self.transaction_type_var,
                                values=["restock", "sale", "adjustment", "return"], state="readonly")
        type_combo.grid(row=0, column=1, pady=5, sticky=tk.W)
        
        # Quantity
        ttk.Label(adjustment_frame, text="Quantity:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.adjustment_quantity_var = tk.StringVar()
        ttk.Entry(adjustment_frame, textvariable=self.adjustment_quantity_var, width=15).grid(
            row=1, column=1, pady=5, sticky=tk.W)
        
        # Notes
        ttk.Label(adjustment_frame, text="Notes:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.notes_var = tk.StringVar()
        ttk.Entry(adjustment_frame, textvariable=self.notes_var, width=25).grid(
            row=2, column=1, pady=5, sticky=tk.W)
        
        # Buttons
        btn_frame = ttk.Frame(adjustment_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Apply Transaction", command=self.apply_transaction).pack(side=tk.LEFT, padx=5)

        ttk.Button(btn_frame, text="Apply Transaction", command=self.apply_transaction).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_adjustment_form).pack(side=tk.LEFT, padx=5)
        
        # Quick actions
        quick_frame = ttk.LabelFrame(right_frame, text="Quick Actions", padding="10")
        quick_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(quick_frame, text="View Low Stock Items", 
                  command=self.show_low_stock).pack(fill=tk.X, pady=2)
        ttk.Button(quick_frame, text="Refresh Stock List", 
                  command=self.refresh_stock).pack(fill=tk.X, pady=2)
    
    def setup_transaction_history(self):
        # Transaction history treeview
        columns = ('ID', 'Product', 'Type', 'Quantity', 'Price', 'User', 'Date', 'Notes')
        self.history_tree = ttk.Treeview(self.history_frame, columns=columns, show='headings')
        
        for col in columns:
            self.history_tree.heading(col, text=col)
        
        self.history_tree.column('ID', width=50)
        self.history_tree.column('Product', width=150)
        self.history_tree.column('Type', width=80)
        self.history_tree.column('Quantity', width=80)
        self.history_tree.column('Price', width=80)
        self.history_tree.column('User', width=100)
        self.history_tree.column('Date', width=150)
        self.history_tree.column('Notes', width=200)
        
        # Scrollbars
        h_scroll = ttk.Scrollbar(self.history_frame, orient=tk.HORIZONTAL, command=self.history_tree.xview)
        v_scroll = ttk.Scrollbar(self.history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X, padx=5)
    
    def refresh(self):
        """Refresh all data"""
        self.refresh_stock()
        self.refresh_history()
    
    def refresh_stock(self):
        """Refresh stock list"""
        # Clear existing items
        for item in self.stock_tree.get_children():
            self.stock_tree.delete(item)
        
        # Load products
        products = self.product_model.get_all_products()
        for product in products:
            product_id, name, _, _, _, quantity, min_stock, _, _, _ = product
            
            # Determine status
            if quantity <= 0:
                status = "Out of Stock"
                tags = ['out_of_stock']
            elif quantity <= min_stock:
                status = "Low Stock"
                tags = ['low_stock']
            else:
                status = "In Stock"
                tags = ['in_stock']
            
            self.stock_tree.insert('', tk.END, values=(
                product_id, name, quantity, min_stock, status
            ), tags=tags)
        
        # Configure tag colors
        self.stock_tree.tag_configure('out_of_stock', background='#ffcccc')
        self.stock_tree.tag_configure('low_stock', background='#fff2cc')
        self.stock_tree.tag_configure('in_stock', background='#ccffcc')
    
    def refresh_history(self):
        """Refresh transaction history"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Load transactions
        transactions = self.transaction_model.get_all_transactions()
        for transaction in transactions:
            trans_id, product_name, trans_type, quantity, price, username, notes, created_at = transaction
            
            # Format price
            price_formatted = f"${price:.2f}" if price else "N/A"
            
            # Format date
            date_formatted = created_at[:19] if created_at else ""
            
            self.history_tree.insert('', tk.END, values=(
                trans_id, product_name, trans_type.title(), quantity,
                price_formatted, username, date_formatted, notes or ""
            ))
    
    def on_stock_select(self, event):
        """Handle stock item selection"""
        selection = self.stock_tree.selection()
        if selection:
            item = self.stock_tree.item(selection[0])
            values = item['values']
            
            self.selected_product_id = values[0]
            self.selected_product_label.config(text=f"Product: {values[1]}")
            self.current_stock_label.config(text=f"Current Stock: {values[2]}")
    
    def apply_transaction(self):
        """Apply stock transaction"""
        if not hasattr(self, 'selected_product_id'):
            messagebox.showwarning("Warning", "Please select a product first")
            return
        
        try:
            quantity_str = self.adjustment_quantity_var.get().strip()
            if not quantity_str:
                messagebox.showerror("Error", "Please enter quantity")
                return
            
            quantity = int(quantity_str)
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be positive")
                return
            
            transaction_type = self.transaction_type_var.get()
            notes = self.notes_var.get().strip()
            
            # Determine quantity change based on transaction type
            if transaction_type in ['sale']:
                quantity_change = -quantity  # Decrease stock
            elif transaction_type in ['restock', 'return']:
                quantity_change = quantity   # Increase stock
            else:  # adjustment
                # For adjustments, let user specify positive or negative
                quantity_change = quantity
            
            # Apply transaction
            success = self.product_model.update_stock(
                product_id=self.selected_product_id,
                quantity_change=quantity_change,
                transaction_type=transaction_type,
                user_id=self.user['id'],
                notes=notes
            )
            
            if success:
                messagebox.showinfo("Success", f"Transaction applied successfully!")
                self.clear_adjustment_form()
                self.refresh()
            else:
                messagebox.showerror("Error", "Transaction failed. Check if sufficient stock is available.")
        
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity")
        except Exception as e:
            messagebox.showerror("Error", f"Transaction failed: {str(e)}")
    
    def clear_adjustment_form(self):
        """Clear adjustment form"""
        self.adjustment_quantity_var.set("")
        self.notes_var.set("")
        self.transaction_type_var.set("restock")
    
    def show_low_stock(self):
        """Show low stock items"""
        low_stock_products = self.product_model.get_low_stock_products()
        
        if not low_stock_products:
            messagebox.showinfo("Low Stock Alert", "No products are currently low in stock!")
            return
        
        # Create popup window
        popup = tk.Toplevel(self)
        popup.title("Low Stock Alert")
        popup.geometry("600x400")
        popup.transient(self)
        popup.grab_set()
        
        # Title
        ttk.Label(popup, text="Products with Low Stock", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Treeview for low stock items
        columns = ('Name', 'Current Stock', 'Min Stock', 'Supplier')
        low_stock_tree = ttk.Treeview(popup, columns=columns, show='headings')
        
        for col in columns:
            low_stock_tree.heading(col, text=col)
        
        for product in low_stock_products:
            low_stock_tree.insert('', tk.END, values=(
                product[1],  # Name
                product[5],  # Current quantity
                product[6],  # Min stock level
                product[7] or "N/A"  # Supplier
            ))
        
        low_stock_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Close button
        ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)