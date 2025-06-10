import sys

class ATM:
    def __init__(self, initial_balance=0):
        self.balance = initial_balance
        self.transaction_history = []

    def display_menu(self):
        print("\n================ Welcome to the Python ATM =================")
        print("Please select an option:")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. View Transaction History")
        print("5. Exit")
        print("\n=============================================================")

    def check_balance(self):
        print(f"\nYour current balance is: ${self.balance:.2f}")

    def deposit_money(self):
        while True:
            amount_str = input("\nEnter the amount to deposit: $")
            try:
                amount = float(amount_str)
                if amount <= 0:
                    print("Please enter a positive amount to deposit.")
                else:
                    self.balance += amount
                    self.transaction_history.append(f"Deposited: +${amount:.2f}")
                    print(f"Successfully deposited ${amount:.2f}. New balance is ${self.balance:.2f}")
                    break
            except ValueError:
                print("Invalid amount. Please enter a numeric value.")

    def withdraw_money(self):
        while True:
            amount_str = input("\nEnter the amount to withdraw: $")
            try:
                amount = float(amount_str)
                if amount <= 0:
                    print("Please enter a positive amount to withdraw.")
                elif amount > self.balance:
                    print("Insufficient balance for this withdrawal.")
                else:
                    self.balance -= amount
                    self.transaction_history.append(f"Withdrew: -${amount:.2f}")
                    print(f"Successfully withdrew ${amount:.2f}. New balance is ${self.balance:.2f}")
                    break
            except ValueError:
                print("Invalid amount. Please enter a numeric value.")

    def view_transaction_history(self):
        print("\nTransaction History:")
        if not self.transaction_history:
            print("No transactions yet.")
        else:
            for i, record in enumerate(self.transaction_history, 1):
                print(f"{i}. {record}")

    def exit_atm(self):
        print("\nThank you for using Python ATM. Have a great day!")
        sys.exit()

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-5): ").strip()
            if choice == '1':
                self.check_balance()
            elif choice == '2':
                self.deposit_money()
            elif choice == '3':
                self.withdraw_money()
            elif choice == '4':
                self.view_transaction_history()
            elif choice == '5':
                self.exit_atm()
            else:
                print("Invalid option. Please select a valid choice (1-5).")

if __name__ == "__main__":
    atm = ATM(initial_balance=1000.00)  # Starting with $1000 for demo purposes
    atm.run()