import java.util.Scanner;
class Char_to_Ascii{
    public static void main(String[]args){
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter a charcter");
        char ch = sc.next().charAt(0);
        int ascii = ch;
        System.out.println(ascii);
        
    }
}