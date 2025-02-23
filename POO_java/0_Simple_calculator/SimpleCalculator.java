import java.util.Scanner;

public class SimpleCalculator {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        boolean continueCalculating = true;
 
        while (continueCalculating) {
            System.out.println("Simple Calculator");
            System.out.println("1. Addition");
            System.out.println("2. Subtraction");
            System.out.println("3. Multiplication");
            System.out.println("4. Division");
            System.out.println("5. Power");
            System.out.println("6. Square");//IDE: VS Code
            System.out.println("7. Exit");
            System.out.print("Enter your choice: ");
            int choice = scanner.nextInt();

            if (choice == 7) {
                System.out.println("\nExiting calculator...");
                break;
            }

            System.out.print("Enter first number: ");
            int num1 = scanner.nextInt();
            System.out.print("Enter second number: ");
            int num2 = scanner.nextInt();
            int result = 0;

            switch (choice) {
                case 1:
                    result = num1 + num2;
                    break;
                case 2:
                    result = num1 - num2;
                    break;
                case 3:
                    result = num1 * num2;
                    break;
                case 4:
                    if (num2 != 0) {
                        result = num1 / num2;
                    } else {
                        System.out.println("Division by zero not allowed.");
                    }
                    break;
                case 5:
                    result = 1;
                    for (int i = 0; i < num2; i++) {
                        result *= num1;
                    }
                    break;
                case 6:
                    result = (int) Math.sqrt(num1); //retorna apenas parte inteira do resultado, e ignora o num2
                    break;
                default:
                    System.out.println("Invalid choice.");
                    break;
            }

            System.out.println("\nResult: " + result);
            System.out.println();
        }
        
        scanner.close();
    }
}
                   
