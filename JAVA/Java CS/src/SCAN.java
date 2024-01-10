import java.util.Scanner;
public class SCAN {
    public static void main (String[]args){
        Scanner sc = new Scanner(System.in);
        long a,b, sum, subtract, multiply,divide; int choice;
        System.out.println("Type the first operand");
        a = sc.nextLong();
        System.out.println("Type the second operand");
        b = sc.nextLong();
        System.out.println("Type 1 for addition");
        System.out.println("Type 2 for subtraction");
        System.out.println("Type 3 for multiply");
        System.out.println("Type 4 for divide");
        choice = sc.nextInt();
        switch(choice){
            case 1 : sum = a+b; System.out.println("The sum is: " + sum);
            break;
            case 2 : subtract = a-b; System.out.println("The result is: " + subtract);
            break;
            case 3 : multiply = a*b; System.out.println("The result is: " + multiply);
            break;
            case 4 : divide = a/b; System.out.println("The result is: " + divide);
            break;
            default : System.out.println("THE VALUE ENTERED IS INCORRECT!!");
        }
    }
}
