import java.util.Scanner;
public class Area_and_Perimeter {
    public static void main(String[]args){
        Scanner sc = new Scanner(System.in);  
        long x=0,y=0,z=0,s=0;long area=0;long perimeter=0; int ch=0;
        System.out.println("Enter your choice");
        System.out.println("1 for Square");
        System.out.println("2 for Rectangle");
        System.out.println("3 for Triangle ");
        System.out.println("4 for Circle");
        ch = sc.nextInt();
        switch(ch){
            case 1:System.out.println("Enter the side of the square...");
                x=sc.nextInt();
                area=x*x;
                perimeter=x*4;
                System.out.println("The area is..."+ area);
                System.out.println("The perimeter is..."+ perimeter);
                break;
            case 2:System.out.println("Enter the length and breadth of the Rectangle...");
                x=sc.nextInt();
                y=sc.nextInt();
                area=x*y;
                perimeter=2*(x+y);
                System.out.println("The perimeter is..."+ perimeter);
                System.out.println("The area is..."+ area);
                break;
            case 3:System.out.println("Enter the sides of the triangle...");
                x=sc.nextInt();
                y=sc.nextInt();
                z=sc.nextInt();
                perimeter=x+y+z;
                s = (x+y+z)/2;
                area = (long) Math.sqrt(s* (s - x) * (s - y) * (s - z));
                System.out.println("The area is..."+ area);
                System.out.println("The perimeter is..."+ perimeter);
                break;
            case 4:System.out.println("Enter the radius of the circle...");
                x=sc.nextInt();
                area=(long) (3.14*x*x);
                perimeter=(long) (2*3.14*x);
                System.out.println("The area is..."+ area);
                System.out.println("The perimeter is..."+ perimeter);
                break;
            default: System.out.println("YOU HAVE ENTERED AN INVALID INPUT!!");
                
        }
    }
}
