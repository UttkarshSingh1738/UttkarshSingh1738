public class Swapping
{
public static void main(String[] args)
{
int num1= 1; int num2= 2; int num3= 3;
System.out.println("Value of number 1 is " +num1);
System.out.println("Value of number 2 is " +num2); System.out.println("Value of number 3 is " +num3);
num1 = num1+ num2+ num3; num2 = num1- (num2+ num3); num3 = num1- (num2+ num3); num1 = num1- (num2+ num3);
System.out.println("Value of number 1 is " +num1);
System.out.println("Value of number 2 is " +num2);
System.out.println("Value of number 3 is " +num3);
}
}