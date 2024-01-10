import java.util.Scanner;
public class User_age {
    public static void main(String[]args){
        int age=0;
        Scanner sc = new Scanner(System.in);
        System.out.println("whats your age?");
        age=sc.nextInt();
        for(int i =1;i<=age;i++)
            System.out.println("*");
    }    
}
