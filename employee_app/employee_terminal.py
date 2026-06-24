from models.approvals import Approval
from models.expenses import Expense
from models.users import User

import controllers.approvals as controller_approval
import controllers.expenses as controller_expense
import controllers.users as controller_user
from db.db import init_db
import os

def submit_expense(user:User):
    #clears the console, regardless of it is in windows or mac/linux
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{'='*25}\nExpense Report Submission\n{'='*25}\n")
    while True:
        amount = input("Please enter the amount of the expense: ")
        try:
            amount = int(amount)
            break
        except ValueError:
            print("\nInvalid input. Please enter a valid number.")
        
    description = input("Please enter the description of the expense: ")
    date = input("Please enter the date of the expense: ") 
    
    controller_expense.create(Expense(user.id, amount, description, date))
    print("\n")

#todo
def get_all_non_pending_user(user:User): 
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{'='*25}\n{user.username}'s Approved or Denied Expense Reports\n{'='*25}\n")
    for expense in controller_expense.get_all_non_pending_user(user.id):
        print(expense)
    print("\n")



def get_all_expenses(user:User):
    #clears the console, regardless of it is in windows or mac/linux
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{'='*25}\n{user.username}'s Expense Reports\n{'='*25}\n")
    for expense in controller_expense.get_all_by_user(user.id):
        print(expense)
    print("\n")

def edit_expense(user:User):
    os.system('cls' if os.name == 'nt' else 'clear')
        
    print(f"{'='*25}\nEdit Expense Report\n{'='*25}\n")
    while True:
        user_input = input("Please enter the expense id you would like to edit or 'exit' to exit: ")
        if user_input == 'exit':
            return
        try:
            id = int(user_input)
            expense = controller_expense.get_from_id(id)
            if (expense is None):
                print("Expense does not exist. Please enter a valid expense.\n")
            elif expense.user_id != user.id:
                print("Invalid operation. You can only delete your own expense reports\n")
            else:
                break
        except ValueError:
            print("\nInvalid input. Please enter a valid number.\n")
    while True:
        amount = input(f"Please enter the new amount (Current: ${expense.amount}): ")
        try:
            amount = int(amount)
            expense.amount = amount
            break
        except ValueError:
            print("\nInvalid input. Please enter a valid number.")

    expense.description = input(f"Please enter the new description: ")
    expense.date = input(f"Please enter the new date : ")
    controller_expense.edit(expense)

def delete_expense(user:User):
    os.system('cls' if os.name == 'nt' else 'clear')
        
    print(f"{'='*25}\nRemove Expense Report\n{'='*25}\n")
    while True:
        user_input = input("Please enter the expense id you would like to remove or 'exit' to exit: ").strip().lower()
        if user_input == 'exit':
            return
        try:
            id = int(user_input)
            expense = controller_expense.get_from_id(id)
            if (expense is None):
                print("Expense does not exist. Please enter a valid expense.\n")
            elif expense.user_id != user.id:
                print("Invalid operation. You can only delete your own expense reports\n")
            else:
                controller_expense.remove(id)
                break
        except ValueError:
            print("\nInvalid input. Please enter a valid number.\n")



def dashboard(user:User):
    running_dash = True
    print(f"\nWelcome Employee {user.username}!")

    while running_dash:
        print("\n1. Submit a new expense report")
        print("2. View the status of all your submitted expense reports")
        print("3. Edit a pending expense report")
        print("4. Delete a pending expense report")
        print("5. View a history of all your approved or denied expense reports")
        print("6. Logout")

        user_input = input("Please select an option: ")
        try:
            user_command = int(user_input)
            if user_command < 1 or user_command > 6:
                print("Invalid operation. Please enter a valid option.")
                continue
        except ValueError as e:
            print("\nInvalid input. Please enter a valid number.")
            continue
        
        if user_command == 1:
            submit_expense(user)
        elif user_command == 2:
            get_all_expenses(user)
        elif user_command == 3:
            edit_expense(user)
        elif user_command == 4:
            delete_expense(user)
        elif user_command == 5:
            get_all_non_pending_user(user)
        elif user_command == 6:
            running_dash = False

def main():
    init_db()
    print("Welcome to the Employee App!")

    running_main = True

    while running_main:
        user_input = input("Please type 1 to login or 2 to exit: ")
        try:
            user_command = int(user_input)
            if user_command < 1 or user_command > 2:
                print("Invalid operation. Please enter 1 or 2.")
        except ValueError as e:
            print("Invalid input. Please enter a valid number.")
        
        if user_command == 1:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            user = user = controller_user.get_from_username_password(username, password)
            if user is not None:
                dashboard(user)
            else:
                print("Username or password not valid, Please try again!")
        if user_command == 2:
            print("Goodbye!")
            running_main = False
    

if __name__ == "__main__":
    main()