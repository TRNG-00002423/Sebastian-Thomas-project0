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
    
    print(f"{"="*25}\nExpense Report Submition{"="*25}\n")
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
def get_one_expense(user:User):
    #clears the console, regardless of it is in windows or mac/linux
    os.system('cls' if os.name == 'nt' else 'clear')
    #todo

def get_all_expenses(user:User):
    #clears the console, regardless of it is in windows or mac/linux
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{"="*25}\n{user.username}'s Expense Reports{"="*25}\n")
    for expense in controller_expense.get_all_by_user(user.id):
        print(expense)
    print("\n")



def dashboard(user:User):
    running_dash = True
    print(f"\nWelcome Employee {user.username}!")

    while running_dash:
        print("\n1. Submit a new expense report")
        print("2. View the status of your submitted expense reports")
        print("3. Edit a pending expense report")
        print("4. Delete a pending expense report")
        print("5. View a history of all approved and denied expense reports")
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
            # TODO: implement logic to view the status of your submitted expense reports
            pass
        elif user_command == 3:
            # TODO: implement logic to edit a pending expense report
            pass
        elif user_command == 4:
            # TODO: implement logic to delete a pending expense report
            pass
        elif user_command == 5:
            get_all_expenses(user)
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
            if  User.get_from_username_password(username,password):
                dashboard(user)
            else:
                print("Username or password not valid, Please try again!")
        if user_command == 2:
            print("Goodbye!")
            running_main = False
    

if __name__ == "__main__":
    main()