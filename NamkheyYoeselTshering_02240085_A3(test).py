# NamkheyYoeselTshering_02240085_A3(test).py

import unittest
import os
import tempfile
from NamkheyYoeselTshering_02240085_A3 import (
    BankAccount, PersonalAccount, BusinessAccount, BankingSystem,
    Invalid_Menu_Choice_Exception, Invalid_Transfer_Exception
)

class TestBankAccount(unittest.TestCase):
    """Tests for core BankAccount functionality"""
    
    def setUp(self):
        self.account = PersonalAccount("12345", "1111", 100.0)
        self.recipient = PersonalAccount("54321", "2222", 50.0)
    
    def test_deposit_positive(self):
        result = self.account.deposit(50.0)
        self.assertEqual(result, "Deposit completed.")
        self.assertEqual(self.account.funds, 150.0)
    
    def test_deposit_zero(self):
        result = self.account.deposit(0)
        self.assertEqual(result, "Invalid amount for deposit.")
        self.assertEqual(self.account.funds, 100.0)
    
    def test_deposit_negative(self):
        result = self.account.deposit(-10.0)
        self.assertEqual(result, "Invalid amount for deposit.")
        self.assertEqual(self.account.funds, 100.0)
    
    def test_withdraw_sufficient(self):
        result = self.account.withdraw(50.0)
        self.assertEqual(result, "Withdrawal completed.")
        self.assertEqual(self.account.funds, 50.0)
    
    def test_withdraw_insufficient(self):
        result = self.account.withdraw(150.0)
        self.assertEqual(result, "Insufficiency of funds or invalid withdrawal sum.")
        self.assertEqual(self.account.funds, 100.0)
    
    def test_withdraw_negative(self):
        result = self.account.withdraw(-10.0)
        self.assertEqual(result, "Insufficiency of funds or invalid withdrawal sum.")
        self.assertEqual(self.account.funds, 100.0)
    
    def test_transfer_successful(self):
        result = self.account.transfer(50.0, self.recipient)
        self.assertEqual(result, "Transfer completed.")
        self.assertEqual(self.account.funds, 50.0)
        self.assertEqual(self.recipient.funds, 100.0)
    
    def test_transfer_insufficient(self):
        result = self.account.transfer(150.0, self.recipient)
        self.assertEqual(result, "Insufficiency of funds or invalid withdrawal sum.")
        self.assertEqual(self.account.funds, 100.0)
        self.assertEqual(self.recipient.funds, 50.0)
    
    def test_transfer_negative(self):
        result = self.account.transfer(-10.0, self.recipient)
        self.assertEqual(result, "Insufficiency of funds or invalid withdrawal sum.")
        self.assertEqual(self.account.funds, 100.0)
        self.assertEqual(self.recipient.funds, 50.0)
    
    def test_valid_topup(self):
        result = self.account.top_up_mobile("12345678", 20.0)
        self.assertEqual(result, "Mobile number 12345678 topped up with 20.0.")
        self.assertEqual(self.account.funds, 80.0)
    
    def test_invalid_phone_number(self):
        result = self.account.top_up_mobile("1234", 20.0)
        self.assertEqual(result, "Invalid phone number or insufficient balance.")
        self.assertEqual(self.account.funds, 100.0)
    
    def test_insufficient_topup(self):
        result = self.account.top_up_mobile("12345678", 150.0)
        self.assertEqual(result, "Invalid phone number or insufficient balance.")
        self.assertEqual(self.account.funds, 100.0)

class TestBankingSystem(unittest.TestCase):
    """Tests for BankingSystem functionality"""
    
    def setUp(self):
        # Use a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.system = BankingSystem(self.temp_file.name)
        self.account1 = self.system.create_account("Personal")
        self.account2 = self.system.create_account("Business")
        # Set known balances for testing
        self.account1.funds = 200.0
        self.account2.funds = 100.0
        self.system.save_accounts()
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_valid_login(self):
        account = self.system.login(self.account1.account_id, self.account1.passcode)
        self.assertEqual(account.account_id, self.account1.account_id)
    
    def test_invalid_login(self):
        with self.assertRaises(ValueError):
            self.system.login("00000", "9999")
    
    def test_delete_account(self):
        acc_id = self.account1.account_id
        self.system.delete_account(acc_id)
        with self.assertRaises(ValueError):
            self.system.login(acc_id, self.account1.passcode)
    
    def test_valid_transfer(self):
        result = self.system.process_User_Input(
            self.account1, "4", 
            amount=50.0, 
            recipient_id=self.account2.account_id
        )
        self.assertEqual(result, "Transfer completed.")
        self.assertEqual(self.account1.funds, 150.0)
        self.assertEqual(self.account2.funds, 150.0)
    
    def test_transfer_nonexistent_account(self):
        with self.assertRaises(Invalid_Transfer_Exception):
            self.system.process_User_Input(
                self.account1, "4",
                amount=50.0,
                recipient_id="99999"  # Doesn't exist
            )
    
    def test_transfer_insufficient_funds(self):
        result = self.system.process_User_Input(
            self.account1, "4",
            amount=300.0,  # More than balance
            recipient_id=self.account2.account_id
        )
        self.assertEqual(result, "Insufficiency of funds or invalid withdrawal sum.")
        self.assertEqual(self.account1.funds, 200.0)
        self.assertEqual(self.account2.funds, 100.0)
    
    def test_invalid_menu_choice(self):
        with self.assertRaises(Invalid_Menu_Choice_Exception):
            self.system.process_User_Input(self.account1, "99")  # Invalid choice
    
    def test_missing_parameters(self):
        with self.assertRaises(TypeError):
            self.system.process_User_Input(self.account1, "4")  # Missing amount/recipient
    
    def test_check_balance(self):
        result = self.system.process_User_Input(self.account1, "1")
        self.assertEqual(result, "Your balance is 200.0")
    
    def test_account_creation(self):
        initial_count = len(self.system.accounts)
        self.system.create_account("Personal")
        self.assertEqual(len(self.system.accounts), initial_count + 1)

class TestEdgeCases(unittest.TestCase):
    """Tests for unusual edge cases"""
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.system = BankingSystem(self.temp_file.name)
        self.account = self.system.create_account("Personal")
        self.account.funds = 100.0
        self.system.save_accounts()
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_transfer_to_self(self):
        """Test transferring to same account (should fail)"""
        result = self.account.transfer(50.0, self.account)
        self.assertNotEqual(result, "Transfer completed.")
        self.assertEqual(self.account.funds, 100.0)
    
    def test_precision_handling(self):
        """Test floating point precision handling"""
        self.account.deposit(0.1)
        self.account.deposit(0.2)
        self.assertAlmostEqual(self.account.funds, 100.3, places=2)
    
    def test_empty_file(self):
        """Test system behavior with empty data file"""
        with open(self.temp_file.name, 'w') as f:
            f.write('')  # Empty file
        
        # Should initialize with no accounts
        system = BankingSystem(self.temp_file.name)
        self.assertEqual(len(system.accounts), 0)
    
    def test_corrupted_file(self):
        """Test system behavior with corrupted data"""
        with open(self.temp_file.name, 'w') as f:
            f.write('bad,data,here\n12345,1111,Personal,100.0')  # One good, one bad line
        
        # Should load the valid account and skip the bad line
        system = BankingSystem(self.temp_file.name)
        self.assertEqual(len(system.accounts), 1)

if __name__ == "__main__":
    unittest.main(verbosity=2)