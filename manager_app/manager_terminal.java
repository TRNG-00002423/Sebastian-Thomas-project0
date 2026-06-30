import models.*;
import dao.*;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.io.IOException;

public class manager_terminal
{
    private static Scanner scanner;
    private static UserDao userDao = new UserDao();
    private static ExpenseDao expenseDao = new ExpenseDao();
    private static ApprovalDao approvalDao = new ApprovalDao();


    private static User validateLogin(String username, String password)
    {
        try
        {
            return userDao.validateManagerLogin(username, password);
        }
        catch (SQLException e)
        {
            System.out.println("Unable to validate login: " + e.getMessage());
            return null;
        }
    }

    //Quality of life methods

    private static void clearConsole(){
        try {
            if (System.getProperty("os.name").contains("Windows")) {
                // For Windows systems
                new ProcessBuilder("cmd", "/c", "cls").inheritIO().start().waitFor();
            } else {
                // For Linux and macOS systems
                new ProcessBuilder("clear").inheritIO().start().waitFor();
            }
        } catch (IOException | InterruptedException ex) {
            ex.printStackTrace();
        }
    }

    private static Integer validateNumber(String userInput){
        try {
            return Integer.parseInt(userInput.trim());
        }
        catch (NumberFormatException e){
            return null;
        }
    }

    private static Integer validateNumber(String userInput, String errorMessage){
        try {
            return Integer.parseInt(userInput.trim());
        }
        catch (NumberFormatException e){
            System.out.println(errorMessage);
            return null;
        }
    }
    //Quality of life methods end

    private static void approveExpense(User user, int expenseID){
        try {
            Expense expense = expenseDao.findById(expenseID);
            if (expense == null) {
                System.out.println("Invalid expense ID, press enter to try again!.");
                scanner.next();
                return;

            }
            clearConsole();
            System.out.printf("========== Expense #%d ==========\n\n", expense.getId());
            System.out.println("Employee: "+ userDao.findById(expense.getUser_id()).getUsername());
            System.out.println("Amount: "+ expense.getAmount());
            System.out.println("Date: "+ expense.getDate());
            System.out.println("Description: "+ expense.getDescription());

            System.out.printf("\n\nStatus: %s\n\n", approvalDao.findByExpenseId(expense.getId()).getStatus());
            System.out.println("_".repeat(30));
            System.out.println("1. Approve\n2. Deny\n3. Back");
            Integer parsedChoice = null;
            do{
                String choice = scanner.next();
                parsedChoice = validateNumber(choice);
                if (parsedChoice==null){
                    System.out.println("Invalid choice, please try again:");
                }
            }while(parsedChoice == null);

             String comment;
            switch (parsedChoice){
                case 1:
                    System.out.print("Would you like to enter a comment: ");
                    comment = scanner.nextLine();
                    approvalDao.updateStatus(expense.getId(), "approved", user.getId(), comment);
                    break;
                case 2:
                    System.out.print("Would you like to enter a comment: ");
                    comment = scanner.nextLine();
                    approvalDao.updateStatus(expense.getId(), "approved", user.getId(), comment);
                    break;                
                case 3:
                    return;
            }
        }
        catch (SQLException e){
            System.out.println("Unable to load expense: " + e.getMessage());
        }
    }

    private static List<Expense> getPendingExpenses(){
        try {
            return expenseDao.findByStatus("pending");
        } catch (SQLException e) {
            System.out.println("Unable to load expenses: " + e.getMessage());
            return new ArrayList<>();
        }
    }

    private static String getEmployeeName(int userId){
        try {
            User employee = userDao.findById(userId);
            if (employee != null) return employee.getUsername();
        }
        catch (SQLException e){
            System.out.println("Unable to load employee name: " + e.getMessage());
        }
        return "Unknown";
    }

    private static List<Expense> filterExpenses(){
        while (true){
            clearConsole();
            System.out.println("Filter Expenses Search:");
            System.out.println("S - Status");
            System.out.println("U - User ID");
            System.out.println("D - Date");
            System.out.println("Q - Quit\n\n\n");
            String choice = scanner.next();

            if (choice.equalsIgnoreCase("q")) return null;
            while (!choice.equalsIgnoreCase("s") && !choice.equalsIgnoreCase("u") && !choice.equalsIgnoreCase("d")){
                clearConsole();
                System.out.println("Filter Expenses Search:");
                System.out.println("S - Status");
                System.out.println("U - User ID");
                System.out.println("D - Date");
                System.out.println("Q - Quit\n\n\n");
                System.out.print("***Please enter a valid option:");
                choice = scanner.next();
                if (choice.equalsIgnoreCase("q")) return null;
            }
            try {
                switch (choice.toUpperCase()){
                    case "S":
                        clearConsole();
                        System.out.println("Filter Expenses Search(Status):");
                        System.out.println("A - Approved");
                        System.out.println("P - Pending");
                        System.out.println("D - Denied");
                        System.out.println("Q - Quit\n\n\n");
                        choice = scanner.next();

                        if (choice.equalsIgnoreCase("q")) return null;
                         while (!choice.equalsIgnoreCase("a") && !choice.equalsIgnoreCase("p") && !choice.equalsIgnoreCase("d")){
                            clearConsole();
                            System.out.println("Filter Expenses Search(Status):");
                            System.out.println("A - Approved");
                            System.out.println("P - Pending");
                            System.out.println("D - Denied");
                            System.out.println("Q - Quit\n\n\n");
                            System.out.print("***Please enter a valid option:");
                            choice = scanner.next();
                            if (choice.equalsIgnoreCase("q")) return null;
                        }
                        switch(choice.toUpperCase()){
                            case "A":
                                return expenseDao.findByStatus("approved");
                            case "P":
                                return expenseDao.findByStatus("pending");
                            case "D":
                                return expenseDao.findByStatus("denied");
                        }                
                        break;
                    case "U":
                        clearConsole();
                        List<Expense> expenses = new ArrayList<>();
                        int numChoice = 0;
                        while (true){
                            System.out.println("Filter Expenses Search(User ID):");
                            System.out.println("Q - Quit\n\n\n");
                            System.out.print("Enter User ID:");
                            choice = scanner.next();                    
                            if (choice.equalsIgnoreCase("q")) return null;
                            Integer parsedChoice = validateNumber(choice);
                            if (parsedChoice != null) {
                                numChoice = parsedChoice;
                                break;
                            }
                            clearConsole();
                            System.out.println("Please enter a number as user ID.");
                        }
                        expenses = expenseDao.findByUserId(numChoice);
                        while (expenses.size() == 0){
                            clearConsole();
                            System.out.println("***The user ID provided was not valid, please try again.");
                            System.out.println("Filter Expenses Search(User ID):");
                            System.out.println("Q - Quit\n\n\n");
                            choice = scanner.next();
                            if (choice.equalsIgnoreCase("q")) return null;
                            Integer parsedChoice = validateNumber(choice);
                            if (parsedChoice != null) {
                                numChoice = parsedChoice;
                                expenses = expenseDao.findByUserId(numChoice);
                            }
                            else {
                                clearConsole();
                                System.out.println("Please enter a number as user ID.");
                            }
                        }
                        return expenses;
                    case "D":
                        clearConsole();
                        System.out.println("Filter Expenses Search(Date):");
                        System.out.println("Q - Quit\n\n\n");
                        System.out.print("Enter Date (YYYY-MM-DD):");
                        choice = scanner.next();
                        if (choice.equalsIgnoreCase("q")) return null;
                        return expenseDao.findByDate(choice);
                }
            } catch (SQLException e) {
                System.out.println("Unable to filter expenses: " + e.getMessage());
                return new ArrayList<>();
            }
        }
    }

    private static void viewExpenses(User user){
        clearConsole();
        List<Expense> expenses = getPendingExpenses();

        int rowsPerPage = 5;
        int currentPage = 1;
        boolean viewing = true;
        while (viewing){
            clearConsole();
            int totalPages = Math.max(1, (int)Math.ceil(expenses.size() / (double)rowsPerPage));
            if (currentPage > totalPages) currentPage = totalPages;
            System.out.printf("Pending Expenses (Page %d/%d)\n\n", currentPage, totalPages);
            System.out.println("Expense ID\tEmployee\tAmount");
            System.out.println("-".repeat(40));
            int startIndex = (currentPage - 1) * rowsPerPage;
            int endIndex = Math.min(startIndex + rowsPerPage, expenses.size());
            for (int i = startIndex; i < endIndex; i++){
                String username = getEmployeeName(expenses.get(i).getUser_id());
                System.out.printf("%d\t\t%s\t\t\t\t$%.2f\n", expenses.get(i).getId(), username, expenses.get(i).getAmount());
            }
            if (expenses.size() == 0) System.out.println("No expenses found.");
            System.out.println();
            System.out.println("N - Next Page");
            System.out.println("P - Previous Page");
            System.out.println("R - Review Expense");
            System.out.println("F - Filter");
            System.out.println("Q - Back");

            switch (scanner.next().toUpperCase()){
                case "N":
                    if (currentPage<totalPages){ 
                        currentPage++;
                    } 
                    else{
                        currentPage = 1;
                    }
                    break;
                case "P":
                    if (currentPage>1){ 
                        currentPage--;
                    } 
                    else{
                        currentPage = totalPages;
                    }
                    break;
                case "R":
                    clearConsole();
                    Integer parsedInput = -1;
                    do{
                        scanner.next();
                        System.out.print("Enter expense ID to review:");
                        parsedInput = validateNumber(scanner.next(), "Invalid input, please enter a number!");

                    }while(parsedInput == null || parsedInput == -1);
                    approveExpense(user, parsedInput);
                    break;
                case "F":
                    List<Expense> filteredExpenses = filterExpenses();
                    if (filteredExpenses != null){
                        expenses = filteredExpenses;
                        currentPage = 1;
                    }
                    break;
                case "Q":
                    scanner.nextLine();
                    return;
            }
        }


    }

    private static void dashboard(User user)
    {
        clearConsole();
        boolean runningDash = true;
        System.out.printf("\nWelcome Manager %s!\n", user.getUsername());

        while (runningDash)
        {
            System.out.println("1. View Expenses");
            System.out.println("2. Generate Expense Report");
            System.out.println("3. Logout");

            String userInput = scanner.nextLine();

            Integer userCommand = validateNumber(userInput, "Invalid input. Please enter a valid number.");
            if (userCommand == null)
            {
                continue;
            }
            if (userCommand < 1 || userCommand > 3)
            {
                System.out.println("Invalid operation. Please enter a valid option.");
                continue;
            }

            if (userCommand == 1)
            {
                viewExpenses(user);
            }
            else if (userCommand == 2)
            {
                // TODO: implement logic for approvaing an expense report
            }
            else if (userCommand == 3)
            {
                runningDash = false;
            }
        }
    }

    public static void main(String[] agrs)
    {
        clearConsole();
        scanner = new Scanner(System.in);
        boolean runningMain = true;

        System.out.println("Welcome to the Manager App!");
        
        while (runningMain)
        {
            System.out.print("Please type 1 to login or 2 to exit: ");
            String userInput = scanner.nextLine();

            Integer userCommand = validateNumber(userInput, "Invalid input. Please enter 1 or 2.");
            if (userCommand == null)
            {
                continue;
            }
            if (userCommand < 1 || userCommand > 2)
            {
                System.out.print("Invalid operation. Please enter 1 or 2.");
                continue;
            }
            if (userCommand == 1)
            {
                System.out.print("Enter your username: ");
                String username = scanner.nextLine();
                System.out.print("Enter your password: ");
                String password = scanner.nextLine();
                User user = validateLogin(username, password);
                if (user != null)
                {
                    dashboard(user);
                }
                else
                {
                    System.out.println("Incorrect username or password");
                }
            }
            if (userCommand == 2)
            {
                System.out.println("Goodbye!");
                runningMain = false;
            }
        }
    }
}
