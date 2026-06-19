import java.util.Scanner;

public class manager_terminal
{
    private static Scanner scanner;

    private static boolean validateLogin(String username, String password)
    {
        return true;
    }

    private static void dashboard(String username)
    {
        boolean runningDash = true;
        System.out.printf("\nWelcome Manager %s!\n", username);

        while (runningDash)
        {
            System.out.println("1. View a list of all pending expenses");
            System.out.println("2. Select an expense report to approve");
            System.out.println("3. Select an expense report to deny");
            System.out.println("4. Add a comment to a non-pending");
            System.out.println("5. Search for expense reports by employee, category, or date");
            System.out.println("6. Logout");

            String userInput = scanner.nextLine();

            int userCommand = 0;
            try
            {
                userCommand = Integer.parseInt(userInput);
                if (userCommand < 1 || userCommand > 6)
                {
                    System.out.println("Invalid operation. Please enter a valid option.");
                    continue;
                }
            }
            // change to more specfic exception(s)
            catch (Exception e)
            {
                System.out.println("Invalid input. Please enter a valid number.");
                continue;
            }

            if (userCommand == 1)
            {
                // TODO: implement logic for viewing list of all pending expeneses
            }
            else if (userCommand == 2)
            {
                // TODO: implement logic for approvaing an expense report
            }
            else if (userCommand == 3)
            {
                // TODO: implement logic for denying an expense report
            }
            else if (userCommand == 4)
            {
                // TODO: implement logic for adding a coment to a non-pending expense report
            }
            else if (userCommand == 5)
            {
                // TODO: implement logic for searching for an expense report by employee, category, or date
            }
            else if (userCommand == 6)
            {
                runningDash = false;
            }
        }
    }

    public static void main(String[] agrs)
    {
        scanner = new Scanner(System.in);
        boolean runningMain = true;

        System.out.println("Welcome to the Manager App!");
        
        while (runningMain)
        {
            System.out.println("Please type 1 to login or 2 to exit: ");
            String userInput = scanner.nextLine();

            try
            {
                int userCommand = Integer.parseInt(userInput);
                if (userCommand < 1 || userCommand > 2)
                {
                    System.out.println("Invalid operation. Please enter 1 or 2.");
                }
                if (userCommand == 1)
                {
                    System.out.println("Enter your username: ");
                    String username = scanner.nextLine();
                    System.out.println("Enter your password: ");
                    String password = scanner.nextLine();
                    if (validateLogin(username, password))
                    {
                        dashboard(username);
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
            // change to more specfic exception(s)
            catch (Exception e)
            {
                System.out.println("Invalid input. Please enter 1 or 2.");
            }
        }
    }
}
