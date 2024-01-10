import java.util.Scanner;
public class Multiplication_Table {
    public static void main(String[]args){
        int product=0;
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter a number...");
        int num = sc.nextInt();
        for(int i =0; i<=12;i++){
            product=num*i;
            System.out.println(num + " X "+i+" =" + product);
        }
    }
}
