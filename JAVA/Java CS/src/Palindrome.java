import java.util.Scanner;
public class Palindrome {
    public static void main (String[]args){
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter a word");
        String word = sc.nextLine();
        int len = word.length();
        String flipword = "";
        for (int i=len-1; i>=0; i--){
            flipword += word.charAt(i);
        }
        if(flipword.equals(word))
            System.out.println("Palindrome");
        else
            System.out.println("Not a palindrome");
    }
}
        
    