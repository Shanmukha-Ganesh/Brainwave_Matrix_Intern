import tkinter as tk
from tkinter import ttk, messagebox
from ..models.product import Product
from ..utils.validators import Validator

class ProductManagementFrame(ttk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.product_model = Product()
        self.selected_product_id = None
        
        self.setup_ui()
        self.refresh()
    
    def setup_ui(self):
        # Main container
        main_container = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Product list
        left_frame = ttk.Frame(main_container)
        main_container.add(left_frame, weight=2)
        
        # Search frame
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        search_entry.bind('<KeyRelease>', self.on_search)
        
        ttk.Button(search_frame, text="Clear", command=self.clear_search).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Products treeview
        columns = ('ID', 'Name', 'Category', 'Price', 'Quantity', 'Min Stock', 'Supplier')
        self.products_tree = ttk.Treeview(left_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.products_tree.heading('ID', text='ID')
        self.products_tree.heading('Name', text='Name')
        self.products_tree.heading('Category', text='Category')
        self.products_tree.heading('Price', text='Price')
        self.products_tree.heading('Quantity', text='Quantity')
        self.products_tree.heading('Min Stock', text='Min Stock')
        self.products_tree.heading('Supplier', text='Supplier')
        
        self.products_tree.column('ID', width=50)
        self.products_tree.column('Name', width=150)
        self.products_tree.column('Category', width=100)
        self.products_tree.column('Price', width=80)
        self.products_tree.column('Quantity', width=80)
        self.products_tree.column('Min Stock', width=80)
        self.products_tree.column('Supplier', width=120)
        
        # Scrollbar for treeview
        tree_scroll = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.products_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.products_tree.bind('<<TreeviewSelect>>', self.on_product_select)
        
        # Right panel - Product form
        right_frame = ttk.Frame(main_container)
        main_container.add(right_frame, weight=1)
        
        # Form title
        form_title = ttk.Label(right_frame, text="Product Details", font=("Arial", 12, "bold"))
        form_title.pack(pady=(0, 10))
        
        # Form fields
        form_frame = ttk.Frame(right_frame)
        form_frame.pack(fill=tk.X, padx=10)
        
        # Name
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.name_var, width=30).grid(row=0, column=1, pady=5, sticky=tk.W)
        
        # Description
        ttk.Label(form_frame, text="Description:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.description_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.description_var, width=30).grid(row=1, column=1, pady=5, sticky=tk.W)
        
        # Category
        ttk.Label(form_frame, text="Category:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.category_var, width=30).grid(row=2, column=1, pady=5, sticky=tk.W)
        
        # Price
        ttk.Label(form_frame, text="Price:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.price_var = tk.StringVar()

        ttk.Entry(form_frame, textvariable=self.price_var, width=30).grid(row=3, column=1, pady=5, sticky=tk.W)
        
        # Quantity
        ttk.Label(form_frame, text="Quantity:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.quantity_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.quantity_var, width=30).grid(row=4, column=1, pady=5, sticky=tk.W)
        
        # Min Stock Level
        ttk.Label(form_frame, text="Min Stock Level:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.min_stock_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.min_stock_var, width=30).grid(row=5, column=1, pady=5, sticky=tk.W)
        
        # Supplier
        ttk.Label(form_frame, text="Supplier:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.supplier_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.supplier_var, width=30).grid(row=6, column=1, pady=5, sticky=tk.W)
        
        # Buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=20)
        
        ttk.Button(btn_frame, text="Add Product", command=self.add_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update Product", command=self.update_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Product", command=self.delete_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=5)
    
    def refresh(self):
        """Refresh the products list"""
        # Clear existing items
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Load products
        products = self.product_model.get_all_products()
        for product in products:
            # Format price
            price_formatted = f"${product[4]:.2f}"
            
            # Check if low stock
            tags = []
            if product[5] <= product[6]:  # quantity <= min_stock_level
                tags = ['low_stock']
            
            self.products_tree.insert('', tk.END, values=(
                product[0],  # ID
                product[1],  # Name
                product[3],  # Category
                price_formatted,  # Price
                product[5],  # Quantity
                product[6],  # Min Stock Level
                product[7]   # Supplier
            ), tags=tags)
        
        # Configure tag colors
        self.products_tree.tag_configure('low_stock', background='#ffcccc')
    
    def on_search(self, event=None):
        """Handle search functionality"""
        search_term = self.search_var.get().strip()
        
        # Clear existing items
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Load filtered products
        if search_term:
            products = self.product_model.search_products(search_term)
        else:
            products = self.product_model.get_all_products()
        
        for product in products:
            price_formatted = f"${product[4]:.2f}"
            tags = []
            if product[5] <= product[6]:
                tags = ['low_stock']
            
            self.products_tree.insert('', tk.END, values=(
                product[0], product[1], product[3], price_formatted,
                product[5], product[6], product[7]
            ), tags=tags)
        
        self.products_tree.tag_configure('low_stock', background='#ffcccc')
    
    def clear_search(self):
        """Clear search and refresh all products"""
        self.search_var.set("")
        self.refresh()
    
    def on_product_select(self, event):
        """Handle product selection"""
        selection = self.products_tree.selection()
        if selection:
            item = self.products_tree.item(selection[0])
            product_id = item['values'][0]
            
            # Load product details
            product = self.product_model.get_product_by_id(product_id)
            if product:
                self.selected_product_id = product_id
                self.name_var.set(product[1])
                self.description_var.set(product[2] or "")
                self.category_var.set(product[3] or "")
                self.price_var.set(str(product[4]))
                self.quantity_var.set(str(product[5]))
                self.min_stock_var.set(str(product[6]))
                self.supplier_var.set(product[7] or "")
    
    def validate_form(self):
        """Validate form data"""
        # Validate name
        valid, msg = Validator.validate_product_name(self.name_var.get())
        if not valid:
            messagebox.showerror("Validation Error", msg)
            return False
        
        # Validate price
        valid, msg = Validator.validate_price(self.price_var.get())
        if not valid:
            messagebox.showerror("Validation Error", msg)
            return False
        
        # Validate quantity
        valid, msg = Validator.validate_quantity(self.quantity_var.get())
        if not valid:
            messagebox.showerror("Validation Error", msg)
            return False
        
        # Validate min stock level
        valid, msg = Validator.validate_quantity(self.min_stock_var.get())
        if not valid:
            messagebox.showerror("Validation Error", f"Min stock level: {msg}")
            return False
        
        return True
    
    def add_product(self):
        """Add new product"""
        if not self.validate_form():
            return
        
        try:
            product_id = self.product_model.add_product(
                name=self.name_var.get().strip(),
                description=self.description_var.get().strip(),
                category=self.category_var.get().strip(),
                price=float(self.price_var.get()),
                quantity=int(self.quantity_var.get()),
                min_stock_level=int(self.min_stock_var.get()),
                supplier=self.supplier_var.get().strip()
            )
            
            if product_id:
                messagebox.showinfo("Success", "Product added successfully!")
                self.clear_form()
                self.refresh()
            else:
                messagebox.showerror("Error", "Failed to add product")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product: {str(e)}")
    
    def update_product(self):
        """Update selected product"""
        if not self.selected_product_id:
            messagebox.showwarning("Warning", "Please select a product to update")
            return
        
        if not self.validate_form():
            return
        
        try:
            success = self.product_model.update_product(
                product_id=self.selected_product_id,
                name=self.name_var.get().strip(),
                description=self.description_var.get().strip(),
                category=self.category_var.get().strip(),
                price=float(self.price_var.get()),
                quantity=int(self.quantity_var.get()),
                min_stock_level=int(self.min_stock_var.get()),
                supplier=self.supplier_var.get().strip()
            )
            
            if success:
                messagebox.showinfo("Success", "Product updated successfully!")
                self.refresh()
            else:
                messagebox.showerror("Error", "Failed to update product")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update product: {str(e)}")
    
    def delete_product(self):
        """Delete selected product"""
        if not self.selected_product_id:
            messagebox.showwarning("Warning", "Please select a product to delete")
            return
        
        # Confirm deletion
        result = messagebox.askyesno("Confirm Delete", 
                                   "Are you sure you want to delete this product?\n"
                                   "This action cannot be undone.")
        if not result:
            return
        
        try:
            success = self.product_model.delete_product(self.selected_product_id)
            if success:
                messagebox.showinfo("Success", "Product deleted successfully!")
                self.clear_form()
                self.refresh()
            else:
                messagebox.showerror("Error", "Failed to delete product")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete product: {str(e)}")
    
    def clear_form(self):
        """Clear all form fields"""
        self.selected_product_id = None
        self.name_var.set("")
        self.description_var.set("")
        self.category_var.set("")
        self.price_var.set("")
        self.quantity_var.set("")
        self.min_stock_var.set("")
        self.supplier_var.set("")
        
        # Clear selection
        for item in self.products_tree.selection():
            self.products_tree.selection_remove(item)
