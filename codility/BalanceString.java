// you can also use imports, for example:
import java.util.*;

// you can use System.out.println for debugging purposes, e.g.
// System.out.println("this is a debug message");

public class BalanceString {
    public int solution(String S) {
        // write your code in Java SE 8
        int s = 0; 
        for(int i = 0; i < S.length() ;i++){
            char c = S.charAt(i); 
            if (c == '('){
                s++; 
            }
            else if (c == ')'){
                s--; 
            }
            if (s < 0){
                return 0;
            }
        }
        if (s != 0){
            return 0;
        }
        return 1; 
    }

    public static void main(String[] args){
        BalanceString s = new BalanceString(); 
        System.out.println(s.solution("(()(())())"));
        System.out.println(s.solution("(()"));
    }
}
