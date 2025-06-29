import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import csv
from datetime import datetime, timedelta
from ..models.product import Product
from ..models.transaction import Transaction

class ReportsFrame(ttk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.product_model = Product()
        self.transaction_model = Transaction()
        
        self.setup_ui()
        self.refresh()
    
    def setup_ui(self):
        # Create notebook for different reports
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Inventory Report Tab
        self.inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.inventory_frame, text="Inventory Report")
        self.setup_inventory_report()
        
        # Sales Report Tab
        self.sales_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.sales_frame, text="Sales Report")
        self.setup_sales_report()
        
        # Low Stock Report Tab
        self.low_stock_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.low_stock_frame, text="Low Stock Report")
        self.setup_low_stock_report()
    
    def setup_inventory_report(self):
        # Control frame
        control_frame = ttk.Frame(self.inventory_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(control_frame, text="Inventory Summary Report", 
                 font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        
        ttk.Button(control_frame, text="Export to CSV", 
                  command=self.export_inventory_report).pack(side=tk.RIGHT, padx=5)
        ttk.Button(control_frame, text="Refresh", 
                  command=self.refresh_inventory_report).pack(side=tk.RIGHT)
        
        # Summary frame
        summary_frame = ttk.LabelFrame(self.inventory_frame, text="Summary", padding="10")
        summary_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.inventory_summary_label = ttk.Label(summary_frame, text="Loading...")
        self.inventory_summary_label.pack()
        
        # Inventory treeview
        columns = ('Product', 'Category', 'Current Stock', 'Min Stock', 'Value', 'Status')
        self.inventory_tree = ttk.Treeview(self.inventory_frame, columns=columns, show='headings')
        
        for col in columns:
            self.inventory_tree.heading(col, text=col)
        
        self.inventory_tree.column('Product', width=200)
        self.inventory_tree.column('Category', width=100)
        self.inventory_tree.column('Current Stock', width=100)
        self.inventory_tree.column('Min Stock', width=100)
        self.inventory_tree.column('Value', width=100)
        self.inventory_tree.column('Status', width=100)
        
        # Scrollbar
        inv_scroll = ttk.Scrollbar(self.inventory_frame, orient=tk.VERTICAL, 
                                  command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscrollcommand=inv_scroll.set)
        
        self.inventory_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=5)
        inv_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=5, padx=(0, 10))
    
    def setup_sales_report(self):
        # Control frame
        control_frame = ttk.Frame(self.sales_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(control_frame, text="Sales Report", 
                 font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        
        # Date range selection
        date_frame = ttk.Frame(control_frame)
        date_frame.pack(side=tk.RIGHT)
        
        ttk.Label(date_frame, text="Period:").pack(side=tk.LEFT, padx=5)
        self.period_var = tk.StringVar(value="Last 30 Days")
        period_combo = ttk.Combobox(date_frame, textvariable=self.period_var,
                                   values=["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"],
                                   state="readonly", width=15)
        period_combo.pack(side=tk.LEFT, padx=5)
        period_combo.bind('<<ComboboxSelected>>', self.refresh_sales_report)
        
        ttk.Button(date_frame, text="Export", 
                  command=self.export_sales_report).pack(side=tk.LEFT, padx=5)
        
        # Summary frame
        summary_frame = ttk.LabelFrame(self.sales_frame, text="Sales Summary", padding="10")
        summary_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.sales_summary_label = ttk.Label(summary_frame, text="Loading...")
        self.sales_summary_label.pack()
        
        # Sales treeview
        columns = ('Product', 'Quantity Sold', 'Total Revenue', 'Avg Price')
        self.sales_tree = ttk.Treeview(self.sales_frame, columns=columns, show='headings')
        
        for col in columns:
            self.sales_tree.heading(col, text=col)
        
        self.sales_tree.column('Product', width=250)
        self.sales_tree.column('Quantity Sold', width=120)
        self.sales_tree.column('Total Revenue', width=120)
        self.sales_tree.column('Avg Price', width=100)
        
        # Scrollbar
        sales_scroll = ttk.Scrollbar(self.sales_frame, orient=tk.VERTICAL, 
                                    command=self.sales_tree.yview)
        self.sales_tree.configure(yscrollcommand=sales_scroll.set)
        
        self.sales_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=5)


        self.sales_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=5)
        sales_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=5, padx=(0, 10))
    
    def setup_low_stock_report(self):
        # Control frame
        control_frame = ttk.Frame(self.low_stock_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(control_frame, text="Low Stock Alert Report", 
                 font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        
        ttk.Button(control_frame, text="Export to CSV", 
                  command=self.export_low_stock_report).pack(side=tk.RIGHT, padx=5)
        ttk.Button(control_frame, text="Refresh", 
                  command=self.refresh_low_stock_report).pack(side=tk.RIGHT)
        
        # Alert frame
        alert_frame = ttk.LabelFrame(self.low_stock_frame, text="Alert Summary", padding="10")
        alert_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.low_stock_summary_label = ttk.Label(alert_frame, text="Loading...")
        self.low_stock_summary_label.pack()
        
        # Low stock treeview
        columns = ('Product', 'Category', 'Current Stock', 'Min Stock', 'Shortage', 'Supplier')
        self.low_stock_tree = ttk.Treeview(self.low_stock_frame, columns=columns, show='headings')
        
        for col in columns:
            self.low_stock_tree.heading(col, text=col)
        
        self.low_stock_tree.column('Product', width=200)
        self.low_stock_tree.column('Category', width=100)
        self.low_stock_tree.column('Current Stock', width=100)
        self.low_stock_tree.column('Min Stock', width=100)
        self.low_stock_tree.column('Shortage', width=100)
        self.low_stock_tree.column('Supplier', width=150)
        
        # Scrollbar
        low_stock_scroll = ttk.Scrollbar(self.low_stock_frame, orient=tk.VERTICAL, 
                                        command=self.low_stock_tree.yview)
        self.low_stock_tree.configure(yscrollcommand=low_stock_scroll.set)
        
        self.low_stock_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=5)
        low_stock_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=5, padx=(0, 10))
    
    def refresh(self):
        """Refresh all reports"""
        self.refresh_inventory_report()
        self.refresh_sales_report()
        self.refresh_low_stock_report()
    
    def refresh_inventory_report(self, event=None):
        """Refresh inventory report"""
        # Clear existing items
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        # Load products
        products = self.product_model.get_all_products()
        
        total_products = len(products)
        total_value = 0
        low_stock_count = 0
        out_of_stock_count = 0
        
        for product in products:
            product_id, name, description, category, price, quantity, min_stock, supplier, created_at, updated_at = product
            
            # Calculate value
            value = price * quantity
            total_value += value
            
            # Determine status
            if quantity <= 0:
                status = "Out of Stock"
                out_of_stock_count += 1
                tags = ['out_of_stock']
            elif quantity <= min_stock:
                status = "Low Stock"
                low_stock_count += 1
                tags = ['low_stock']
            else:
                status = "In Stock"
                tags = ['in_stock']
            
            self.inventory_tree.insert('', tk.END, values=(
                name, category or "N/A", quantity, min_stock, 
                f"${value:.2f}", status
            ), tags=tags)
        
        # Configure tag colors
        self.inventory_tree.tag_configure('out_of_stock', background='#ffcccc')
        self.inventory_tree.tag_configure('low_stock', background='#fff2cc')
        self.inventory_tree.tag_configure('in_stock', background='#ccffcc')
        
        # Update summary
        summary_text = (f"Total Products: {total_products} | "
                       f"Total Inventory Value: ${total_value:.2f} | "
                       f"Low Stock: {low_stock_count} | "
                       f"Out of Stock: {out_of_stock_count}")
        self.inventory_summary_label.config(text=summary_text)
    
    def refresh_sales_report(self, event=None):
        """Refresh sales report"""
        # Clear existing items
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)
        
        # Calculate date range
        period = self.period_var.get()
        start_date = None
        
        if period == "Last 7 Days":
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        elif period == "Last 30 Days":
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        elif period == "Last 90 Days":
            start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
        
        # Load sales data
        sales_data = self.transaction_model.get_sales_summary(start_date)
        
        total_revenue = 0
        total_quantity = 0
        
        for sale in sales_data:
            product_name, quantity_sold, revenue = sale
            avg_price = revenue / quantity_sold if quantity_sold > 0 else 0
            
            total_revenue += revenue
            total_quantity += quantity_sold
            
            self.sales_tree.insert('', tk.END, values=(
                product_name, quantity_sold, f"${revenue:.2f}", f"${avg_price:.2f}"
            ))
        
        # Update summary
        summary_text = (f"Period: {period} | "
                       f"Total Revenue: ${total_revenue:.2f} | "
                       f"Total Items Sold: {total_quantity}")
        self.sales_summary_label.config(text=summary_text)
    
    def refresh_low_stock_report(self, event=None):
        """Refresh low stock report"""
        # Clear existing items
        for item in self.low_stock_tree.get_children():
            self.low_stock_tree.delete(item)
        
        # Load low stock products
        low_stock_products = self.product_model.get_low_stock_products()
        
        critical_count = 0  # Out of stock
        warning_count = 0   # Low stock
        
        for product in low_stock_products:
            product_id, name, description, category, price, quantity, min_stock, supplier, created_at, updated_at = product
            
            shortage = min_stock - quantity
            
            if quantity <= 0:
                critical_count += 1
                tags = ['critical']
            else:
                warning_count += 1
                tags = ['warning']
            
            self.low_stock_tree.insert('', tk.END, values=(
                name, category or "N/A", quantity, min_stock, 
                shortage, supplier or "N/A"
            ), tags=tags)
        
        # Configure tag colors
        self.low_stock_tree.tag_configure('critical', background='#ffcccc')
        self.low_stock_tree.tag_configure('warning', background='#fff2cc')
        
        # Update summary
        total_alerts = len(low_stock_products)
        summary_text = (f"Total Alerts: {total_alerts} | "
                       f"Critical (Out of Stock): {critical_count} | "
                       f"Warning (Low Stock): {warning_count}")
        self.low_stock_summary_label.config(text=summary_text)
    
    def export_inventory_report(self):
        """Export inventory report to CSV"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save Inventory Report"
            )
            
            if not filename:
                return
            
            products = self.product_model.get_all_products()
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(['Product Name', 'Category', 'Current Stock', 'Min Stock', 
                               'Price', 'Total Value', 'Supplier', 'Status'])
                
                # Write data
                for product in products:
                    name, description, category, price, quantity, min_stock, supplier = product[1:8]
                    value = price * quantity
                    
                    if quantity <= 0:
                        status = "Out of Stock"
                    elif quantity <= min_stock:
                        status = "Low Stock"
                    else:
                        status = "In Stock"
                    
                    writer.writerow([name, category or "N/A", quantity, min_stock, 
                                   f"${price:.2f}", f"${value:.2f}", supplier or "N/A", status])
            
            messagebox.showinfo("Success", f"Inventory report exported to {filename}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")
    
    def export_sales_report(self):
        """Export sales report to CSV"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save Sales Report"
            )
            
            if not filename:
                return
            
            # Calculate date range
            period = self.period_var.get()
            start_date = None
            
            if period == "Last 7 Days":
                start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            elif period == "Last 30 Days":
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            elif period == "Last 90 Days":
                start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
            
            sales_data = self.transaction_model.get_sales_summary(start_date)
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(['Product Name', 'Quantity Sold', 'Total Revenue', 'Average Price'])
                
                # Write data
                for sale in sales_data:
                    product_name, quantity_sold, revenue = sale
                    avg_price = revenue / quantity_sold if quantity_sold > 0 else 0
                    writer.writerow([product_name, quantity_sold, f"${revenue:.2f}", f"${avg_price:.2f}"])
            
            messagebox.showinfo("Success", f"Sales report exported to {filename}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")
    
    def export_low_stock_report(self):
        """Export low stock report to CSV"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save Low Stock Report"
            )
            
            if not filename:
                return
            
            low_stock_products = self.product_model.get_low_stock_products()
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(['Product Name', 'Category', 'Current Stock', 'Min Stock', 
                               'Shortage', 'Supplier', 'Status'])
                
                # Write data
                for product in low_stock_products:
                    name, description, category, price, quantity, min_stock, supplier = product[1:8]
                    shortage = min_stock - quantity
                    status = "Out of Stock" if quantity <= 0 else "Low Stock"
                    
                    writer.writerow([name, category or "N/A", quantity, min_stock, 
                                   shortage, supplier or "N/A", status])
            
            messagebox.showinfo("Success", f"Low stock report exported to {filename}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")
