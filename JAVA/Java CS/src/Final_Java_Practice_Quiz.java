//https://www.examsbook.com/very-simple-gk-questions-and-answers/1 (SOURCE OF QUIZ)
import java.util.Scanner;
public class Final_Java_Practice_Quiz {
    public static void main (String[]args){
        Scanner sc =new Scanner(System.in);
        String name;
        String Question[]= {"The unit of current is?", "Thomas Cup is associated with?", "To which country does the present UN Secretary-General belongs?", " Vitamin B12 is most useful for combating?", "To prevent loss of weight plants reduce transpiration by...?", "The term which denotes that each side has made equal point at game point, in Tennis, is referred to as?", "The term butterfly is associated with?", " The velocity of sound in air (under normal condition) is?", "The velocity of light was first measured by?", " Venturi tube is used for?"};
        String Option[] = {"(A)ohm (B)watt (C)ampere (D)None of the above", "(A)badminton (B)billiards (C)lawn tennis (D)table tennis", "(A)Ghana (B)South Korea (C)Spain (D)Sweden", "(A)anemia (B)goiter (C)night blindness (D)rickets", "(A)shedding of leaves (B)reducing the size of leaves (C)developing hair around stomata (D)All of the above", "(A)baseline (B)deuce (C)fault (D)grand slam", "(A)kabaddi (B)swimming (C)Boxing (D)wrestling", "(A)30 m/sec (B)320 m/sec (C)343 m/sec (D)3,320 m/sec", "(A)Einstein (B)Newton (C)Romer (D)Galileo", "(A)measuring the intensity of earthquakes (B)measuring specific gravity (C)measuring density (D)measuring the flow of a fluid"};
        char Choice[] = new char[10];
        char Answer[] = {'c', 'a', 'b', 'a', 'd', 'b', 'b', 'c', 'c', 'd'};
        int score = 0; long percent = 0;
        //-----------------------------------------------------------------------------------
        System.out.println("What is your name?");
        name = sc.nextLine();
        System.out.println("Hi there " + name + " We will now be starting the quiz...");
        System.out.println("Make sure your answers are in lowercase letters!!!");
        for(int i = 0; i<10; i++){
            System.out.println(Question[i]);
            System.out.println(Option[i]);
            System.out.print("Enter your answer : ");
            Choice[i]= sc.next().charAt(0);
            System.out.println("");
        }
        for (int i =0; i<10; i++){
            if (Choice[i]==Answer[i]){
                score++;
            }    
        }
        percent=(score*100)/10;
        if (score<4){
            System.out.println("Hi " + name + " The quiz has concluded, you have displayed an average performance.");
            System.out.println("Your score is... " + score + "/10" + " you scored " + percent +" percent");
        }
        if (score>=4 && score<=7){
            System.out.println("Hi " + name + " The quiz has concluded, you have done very well !!!");
            System.out.println("Your score is... " + score + "/10" + " you scored " + percent +" percent");
        }
        if (score>7){
            System.out.println("Hi " + name + " The quiz has concluded, you have displayed an excellent performance.");
            System.out.println("Your score is... " + score + "/10" + " you scored " + percent +" percent");
        }
           
}
}
