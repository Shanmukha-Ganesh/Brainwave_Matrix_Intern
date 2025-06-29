from .database import Database

class Transaction:
    def __init__(self):
        self.db = Database()
    
    def get_all_transactions(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.id, p.name, t.transaction_type, t.quantity, t.price, 
                   u.username, t.notes, t.created_at
            FROM transactions t
            JOIN products p ON t.product_id = p.id
            JOIN users u ON t.user_id = u.id
            ORDER BY t.created_at DESC
        ''')
        
        transactions = cursor.fetchall()
        conn.close()
        return transactions
    
    def get_transactions_by_product(self, product_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.id, p.name, t.transaction_type, t.quantity, t.price, 
                   u.username, t.notes, t.created_at
            FROM transactions t
            JOIN products p ON t.product_id = p.id
            JOIN users u ON t.user_id = u.id
            WHERE t.product_id = ?
            ORDER BY t.created_at DESC
        ''', (product_id,))
        
        transactions = cursor.fetchall()
        conn.close()
        return transactions
    
    def get_sales_summary(self, start_date=None, end_date=None):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT p.name, SUM(t.quantity) as total_sold, 
                   SUM(t.quantity * t.price) as total_revenue
            FROM transactions t
            JOIN products p ON t.product_id = p.id
            WHERE t.transaction_type = 'sale'
        '''
        
        params = []
        if start_date:
            query += ' AND t.created_at >= ?'
            params.append(start_date)
        if end_date:
            query += ' AND t.created_at <= ?'
            params.append(end_date)
        
        query += ' GROUP BY p.id, p.name ORDER BY total_revenue DESC'
        
        cursor.execute(query, params)
        summary = cursor.fetchall()
        conn.close()
        return summary
