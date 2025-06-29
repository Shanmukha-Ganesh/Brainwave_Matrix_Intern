from .database import Database
from datetime import datetime

class Product:
    def __init__(self):
        self.db = Database()
    
    def add_product(self, name, description, category, price, quantity, min_stock_level, supplier):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO products (name, description, category, price, quantity, min_stock_level, supplier)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, description, category, price, quantity, min_stock_level, supplier))
        
        product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return product_id
    
    def update_product(self, product_id, name, description, category, price, quantity, min_stock_level, supplier):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE products 
            SET name=?, description=?, category=?, price=?, quantity=?, 
                min_stock_level=?, supplier=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        ''', (name, description, category, price, quantity, min_stock_level, supplier, product_id))
        
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    def delete_product(self, product_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM products WHERE id=?', (product_id,))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    def get_all_products(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, description, category, price, quantity, 
                   min_stock_level, supplier, created_at, updated_at
            FROM products ORDER BY name
        ''')
        
        products = cursor.fetchall()
        conn.close()
        return products
    
    def get_product_by_id(self, product_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, description, category, price, quantity, 
                   min_stock_level, supplier, created_at, updated_at
            FROM products WHERE id=?
        ''', (product_id,))
        
        product = cursor.fetchone()
        conn.close()
        return product
    
    def search_products(self, search_term):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, description, category, price, quantity, 
                   min_stock_level, supplier, created_at, updated_at
            FROM products 
            WHERE name LIKE ? OR description LIKE ? OR category LIKE ?
            ORDER BY name
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        
        products = cursor.fetchall()
        conn.close()
        return products
    
    def get_low_stock_products(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, description, category, price, quantity, 
                   min_stock_level, supplier, created_at, updated_at
            FROM products 
            WHERE quantity <= min_stock_level
            ORDER BY quantity ASC
        ''')
        
        products = cursor.fetchall()
        conn.close()
        return products
    
    def update_stock(self, product_id, quantity_change, transaction_type, user_id, notes=""):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Get current quantity
        cursor.execute('SELECT quantity, price FROM products WHERE id=?', (product_id,))
        result = cursor.fetchone()
        if not result:
            conn.close()
            return False
        
        current_quantity, price = result
        new_quantity = current_quantity + quantity_change
        
        if new_quantity < 0:
            conn.close()
            return False
        
        # Update product quantity
        cursor.execute('''
            UPDATE products SET quantity=?, updated_at=CURRENT_TIMESTAMP 
            WHERE id=?
        ''', (new_quantity, product_id))
        
        # Record transaction
        cursor.execute('''
            INSERT INTO transactions (product_id, transaction_type, quantity, price, user_id, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (product_id, transaction_type, abs(quantity_change), price, user_id, notes))
        
        conn.commit()
        conn.close()
        return True
