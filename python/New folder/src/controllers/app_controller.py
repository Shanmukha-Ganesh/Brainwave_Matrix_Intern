from ..views.login_window import LoginWindow
from ..views.main_window import MainWindow

class AppController:
    def __init__(self):
        self.current_user = None
        self.main_window = None
    
    def start_application(self):
        """Start the application with login window"""
        login_window = LoginWindow(self.on_login_success)
        login_window.run()
    
    def on_login_success(self, user):
        """Handle successful login"""
        self.current_user = user
        self.show_main_window()
    
    def show_main_window(self):
        """Show main application window"""
        if self.current_user:
            self.main_window = MainWindow(self.current_user)
            self.main_window.run()
