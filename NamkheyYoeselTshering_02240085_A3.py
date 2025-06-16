
import random
import tkinter as tk
import tkinter.simpledialog as simpledialog
from tkinter import messagebox



"""This error appears when you pick an option that doesn't exist in the menu"""

class Invalid_Menu_Choice_Exception(Exception):
    "Raised when a user inputs an invalid menu choice."
    pass


""" This error appears when a money transfercan't be completed. """

class Invalid_Transfer_Exception(Exception):
    "Raised for invalid money transfer operations."
    pass



""" Class made to represent a general bank account. """
class BankAccount:
    
    def __init__(self, account_id, passcode, account_category, funds=0):

        """ Initialize a bank account.

        account_id: Unique account identifier
        passcode: 4-digit security code
        account_category: 'Personal' or 'Business'
        funds: Starting balance (default 0)"""

        # Generates a 5-digit account number, a 4-digit pin, account type and the current balance 
        self.account_id = account_id
        self.passcode = passcode
        self.account_category = account_category
        self.funds = funds


    # Adds money to the account if the amount is valid
    def deposit(self, amount):
        """
        Add money to the account.
        Args:
            amount: Positive value to deposit
        Returns:
            Transaction status message
        """

        # Allowe only positive deposits
        if amount > 0:
            self.funds += amount 
            return "Deposit completed."             
        return "Invalid amount for deposit."        # Returns Invalid amount error, funds must be greater than zero



    # Takes the money out of the account if there is enough amount
    def withdraw(self, amount):
        """
        Remove money from account if sufficient funds exist.
        
        Args:
            amount: Positive value to withdraw
            
        Returns:
            Transaction status message
        """

        if 0 < amount <= self.funds:
            self.funds -= amount
            return "Withdrawal completed."
        return "Insufficiency of funds or invalid withdrawal sum."   # Returns insufficiency of funds because there is not enough money ofr withdrawl



    # Sends money to another account
    def transfer(self, amount, recipient_account):
        """
        Transfer money to another account.
        
        Args:
            amount: Positive value to transfer
            recipient_account (BankAccount): Target account
            
        Returns:
            Transaction status message
        """

        # First attempt withdrawal from this account
        withdrawal_message = self.withdraw(amount)
        if withdrawal_message == "Withdrawal completed.":
            recipient_account.deposit(amount)
            return "Transfer completed."
        return withdrawal_message
    


    # Adds credit to a phone number if valid
    def top_up_mobile(self, number, amount):
        """
        Purchase mobile phone credit.
        
        Args:
            number: 8-digit phone number
            amount: Positive top-up amount
            
        Returns:
            Transaction status message
        """
        if len(number) == 8 and number.isdigit() and amount > 0 and amount <= self.funds:
            self.funds -= amount
            return f"Mobile number {number} topped up with {amount}."
        return "Invalid phone number or insufficient balance."


# Class made for Personal Account
class PersonalAccount(BankAccount):

    # A regular account made  for individual people.
    def __init__(self, account_id, passcode, funds=0):
        """
        Initialize personal account.
        
        Args:
            account_id: 5-digit account number
            passcode: 4-digit PIN
            funds: Starting balance (default 0)
        """
        super().__init__(account_id, passcode, "Personal", funds)



# Class made for Business Account

class BusinessAccount(BankAccount):
    # A bank account for businesses and companies
    def __init__(self, account_id, passcode, funds=0):
        """
        Initialize business account.
        
        Args:
            account_id: 5-digit account number
            passcode: 4-digit PIN
            funds: Starting balance (default 0)
        """
        super().__init__(account_id, passcode, "Business", funds)


# Class made to handle all the banks 
class BankingSystem:

    def __init__(self, filename = "accounts.txt"):
        """
        Initialize banking system.
        
        Args:
            filename: Account data storage file (default 'accounts.txt')
        """

        # Starts up the banking system nd loads existing accounts
        self.filename = filename
        self.accounts = self.load_accounts()  # Gets all the saved account


    def load_accounts(self):

        # Loads account from file when the systems starts
        
        accounts = {} # Creates a dictionary where each account is stored with its ID as the key
        

        # Reads all the saved accounts from a file when the bank starts
        try:
            # Open accouts file for reading
            with open(self.filename, "r") as file:

                # Read eaach account line by line
                for line in file:

                    # Split the line into account details like id,passwoer,categories,etcc
                    account_id, passcode, account_category, funds = line.strip().split(",")

                    # Convert balance to the number
                    funds = float(funds)


                    # Creates appriopriate account type
                    if account_category == "Personal":
                        account = PersonalAccount(account_id, passcode, funds)
                    else:
                        account = BusinessAccount(account_id, passcode, funds)
                    
                    # Stores account in the dictionary with ID as key
                    accounts[account_id] = account

        # IF the file doesn't exits yet, it starts with an empty account
        except FileNotFoundError:
            pass
        return accounts


    
    # Saves all accounts to the file after changes

    def save_accounts(self):

        # Open the file for writing
        with open(self.filename, "w") as file:

            # Write each account as a line in the file
            for account in self.accounts.values():
                file.write(f"{account.account_id},{account.passcode},{account.account_category},{account.funds}\n")


    
    # Makes a new personal and business account

    def create_account(self, account_type):
        """
        Create new bank account.
        
        Args:
            account_type: 'Personal' or 'Business'
            
        Returns:
            BankAccount: Newly created account
        """

        # Generate a random 5- digit caccount ID and a 4-digit passwords
        account_id = str(random.randint(10000, 99999))
        passcode = str(random.randint(1000, 9999))

        # Create a account type
        if account_type == "Personal":
            account = PersonalAccount(account_id, passcode)
        else:
            account = BusinessAccount(account_id, passcode)

        # Add a new account to system and save
        self.accounts[account_id] = account
        self.save_accounts()

        # Return the new account
        return account


    # Checks if the login details are correct
    def login(self, account_id, passcode):
        """
        Authenticate user credentials.
        
        Args:
            account_id: Account number
            passcode: Account PIN
            
        Returns:
            BankAccount: Authenticated account object
            
        Raises:
            ValueError: If authentication fails
        """

        # Check if the account exists or not
        account = self.accounts.get(account_id)

        # Verify of the passwords matches or not
        if account and account.passcode == passcode:
            return account
        
        # If either checks, it fails        
        raise ValueError("Account number or password is not recognized")


    # Removes an account from the system
    def delete_account(self, account_id):
        """
        Permanently remove account.
        
        Args:
            account_id: Account number to delete
            
        Raises:
            ValueError: If account doesn't exist
        """

        # Check if the account exists
        if account_id in self.accounts:

            # Remove from the memory and update the file 
            del self.accounts[account_id]
            self.save_accounts()
        else:
            raise ValueError("Account does not exist")



    # Handles whatever action the user want to do

    def process_User_Input(self, account, choice, amount=None, recipient_id=None, number=None):
        """
        Execute user-selected banking operation.
        
        Args:
            account (BankAccount): Source account
            choice: Menu selection (1-6)
            amount: Transaction amount
            recipient_id: Target account ID
            number: Mobile number
            
        Returns:
            Operation result message
            
        Raises:
            Invalid_Menu_Choice_Exception: For invalid menu selections
            Invalid_Transfer_Exception: For failed transfers
        """
        
        # Checks the balance of the account
        if choice == "1":
            return f"Your balance is {account.funds}"
        
        # Deposit the money to the account
        elif choice == "2":
            result = account.deposit(amount)
        
        # Withdrw the money from the account
        elif choice == "3":
            result = account.withdraw(amount)

        # Transfer the momney from the account
        elif choice == "4":
            # First check if the recipient exist
            if recipient_id not in self.accounts:
                raise Invalid_Transfer_Exception("Recipient account does not exist.")
            result = account.transfer(amount, self.accounts[recipient_id])

        # Mobile top-up
        elif choice == "5":
            result = account.top_up_mobile(number, amount)

        # Deletes an account
        elif choice == "6":
            self.delete_account(account.account_id)
            result = "Account successfully deleted."

        # Invaild choice
        else:
            raise Invalid_Menu_Choice_Exception("Invalid menu choice")
        
        # Saves any changes made
        self.save_accounts()
        return result



class BankingGUI:
    """Graphical user interface for banking application"""

    def __init__(self, system):
        """
        Initialize banking GUI.
        
        Args:
            system (BankingSystem): Connected banking system
        """

        # It sets up the main banking application window
        self.system = system
        self.account = None

        # Creates the main window
        self.window = tk.Tk()
        self.window.title("Banking Application")

        # Creates an account ID and passwords entry fields

        self.id_entry = tk.Entry(self.window)
        self.pass_entry = tk.Entry(self.window, show="*")  # Hides the passwords characters

        # Creates status display label
        self.output = tk.Label(self.window, text="Welcome to the Bank!", wraplength=300)

        # Adds labels and entry fields to window
        tk.Label(self.window, text="Account ID").pack()
        self.id_entry.pack()
        tk.Label(self.window, text="Passcode").pack()
        self.pass_entry.pack()

        # Add action buttons
        tk.Button(self.window, text="Login", command=self.login).pack()
        tk.Button(self.window, text="Create Personal Account", command=lambda: self.create_account("Personal")).pack()
        tk.Button(self.window, text="Create Business Account", command=lambda: self.create_account("Business")).pack()

        # Displays everyting
        self.output.pack()
        self.window.mainloop()


    def create_account(self, account_type):

        # Creates new account and show the credentials details to the user
        account = self.system.create_account(account_type)
        self.output.config(text=f"Created {account_type} Account. ID: {account.account_id}, Pass: {account.passcode}")


    def login(self):

        # Attempts to log in with entered credentitals
        acc_id = self.id_entry.get()
        passcode = self.pass_entry.get()

        try:
            self.account = self.system.login(acc_id, passcode)
            self.show_logged_in_options()
        except ValueError as e:
            messagebox.showerror("Login Failed", str(e))


    def show_logged_in_options(self):
        # Display banking options after successful login
        self.clear_widgets()

        # Shows all the avaolable banking options 
        options = [
            ("Check Balance", "1"),
            ("Deposit", "2"),
            ("Withdraw", "3"),
            ("Transfer", "4"),
            ("Top-Up Mobile", "5"),
            ("Delete Account", "6"),
            ("Logout", "logout")
        ]

        # Creates a button for each options
        for text, val in options:
            tk.Button(self.window, text=text, command=lambda v=val: self.handle_action(v)).pack()
        self.output.pack()



    # Process user's sleected banking operations
    def handle_action(self, choice):

        try:
            if choice == "logout":
                # Return to login screen
                self.account = None
                self.clear_widgets()
                self.__init__(self.system)
                return
            
            # Handles the deposit
            if choice == "2":
                amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:", minvalue=0.01)
                if amount is None: return
                result = self.system.process_User_Input(self.account, choice, amount=amount)

            # Handles the withdrawls
            elif choice == "3":
                amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:", minvalue=0.01)
                if amount is None: return
                result = self.system.process_User_Input(self.account, choice, amount=amount)


            # Handles the transfer
            elif choice == "4":
                recipient_id = simpledialog.askstring("Transfer", "Enter recipient account ID:")
                if recipient_id is None: return
                amount = simpledialog.askfloat("Transfer", "Enter amount to transfer:", minvalue=0.01)
                if amount is None: return
                result = self.system.process_User_Input(self.account, choice, amount=amount, recipient_id=recipient_id)

            # Handles the mobile top-up
            elif choice == "5":
                number = simpledialog.askstring("Mobile Top-Up", "Enter mobile number (8 digits):")
                if number is None: return
                amount = simpledialog.askfloat("Mobile Top-Up", "Enter top-up amount:", minvalue=0.01)
                if amount is None: return
                result = self.system.process_User_Input(self.account, choice, number=number, amount=amount)

            elif choice == "6":
                confirm = messagebox.askyesno(
                    "Confirm Deletion",
                    "Permanently delete this account?\nThis cannot be undone!",
                    parent=self.window
                )
                if confirm:
                    result = self.system.process_User_Input(self.account, choice)
                    messagebox.showinfo("Account Deleted", result)
                    self.account = None
                    self.clear_widgets()
                    self.__init__(self.system)

            # Handles simple commands like checking the balance
            else:
                result = self.system.process_User_Input(self.account, choice)

            # Shows operation result to the user
            self.output.config(text=result)

        # Shows any error that occurs
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def clear_widgets(self):

        # Removes all widgets except the status display

        for widget in self.window.winfo_children():
            if widget != self.output:
                widget.destroy()


if __name__ == "__main__":
    # Start the bankig application

    # Creates the banking system 
    system = BankingSystem() 
    
    # Launch the GUI
    BankingGUI(system)
