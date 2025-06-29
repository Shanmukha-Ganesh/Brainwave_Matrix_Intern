import re

class Validator:
    @staticmethod
    def validate_username(username):
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters long"
        if not re.match("^[a-zA-Z0-9_]+$", username):
            return False, "Username can only contain letters, numbers, and underscores"
        return True, ""
    
    @staticmethod
    def validate_password(password):
        if not password or len(password) < 6:
            return False, "Password must be at least 6 characters long"
        return True, ""
    
    @staticmethod
    def validate_product_name(name):
        if not name or len(name.strip()) < 2:
            return False, "Product name must be at least 2 characters long"
        return True, ""
    
    @staticmethod
    def validate_price(price_str):
        try:
            price = float(price_str)
            if price < 0:
                return False, "Price cannot be negative"
            return True, ""
        except ValueError:
            return False, "Price must be a valid number"
    
    @staticmethod
    def validate_quantity(quantity_str):
        try:
            quantity = int(quantity_str)
            if quantity < 0:
                return False, "Quantity cannot be negative"
            return True, ""
        except ValueError:
            return False, "Quantity must be a valid integer"
