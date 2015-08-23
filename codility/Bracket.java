/**
 *
 * A string S consisting of N characters is considered to be properly nested if any of the following conditions is true:
 * 
 * S is empty;
 * S has the form "(U)" or "[U]" or "{U}" where U is a properly nested string;
 * S has the form "VW" where V and W are properly nested strings.
 * For example, the string "{[()()]}" is properly nested but "([)()]" is not.
 * 
 * Write a function:
 * 
 * class Solution { public int solution(String S); }
 * 
 * that, given a string S consisting of N characters, returns 1 if S is properly nested and 0 otherwise.
 * 
 * For example, given S = "{[()()]}", the function should return 1 and given S = "([)()]", the function should return 0, as explained above.
 * 
 * Assume that:
 * 
 * N is an integer within the range [0..200,000];
 * string S consists only of the following characters: "(", "{", "[", "]", "}" and/or ")".
 * Complexity:
 * 
 * expected worst-case time complexity is O(N);
 * expected worst-case space complexity is O(N) (not counting the storage required for input arguments).
 */
import java.util.*;
public class Bracket{
    private int idx(char c){
        switch(c){
            case '{':
            case '}':
                return 0; 
            case '(': 
            case ')': 
                return 1; 
            case ']':
            case '[':
                return 2; 
        }
        return -1;
    }
    private int pt(char c){
        switch(c){
            case '{':
            case '(':
            case '[':
                return 1;
            case '}':
            case ')':
            case ']':
                return -1; 
        }
        return 0;
    }

    public int solution(String S){
        int[] s = new int[3]; 
        Arrays.fill(s, 0); 

        for(int i = 0 ; i < S.length(); i++){
            char c = S.charAt(i); 
            s[this.idx(c)] += this.pt(c);
            if( s[this.idx(c)] < 0){
                return 0;    
            }
        } 

        for (int i = 0 ; i < s.length ;i++){
            if(s[i] != 0){
                return 0; 
            }
        }
        return 1; 
    }

    public int solution2(String S){
        Deque<Character> stack = new ArrayDeque<Character>(); 

        for (int i = 0 ; i < S.length(); i++){
            char c = S.charAt(i); 
            if(c == '{' || c == '(' || c== '['){
                stack.addFirst(c);            
            }
            else{
                Character p = stack.pollFirst(); 
                if (p == null){
                    return 0; 
                }
                if ((c == '}' && p != '{') || (c == ')' && p != '(') || (c ==']' && p!='[')){
                    return 0;
                }
            }
        }
        if (stack.size() > 0){
            return 0; 
        }
        return 1; 
    }

    public static void main(String[] args){
        Bracket b = new Bracket(); 
        System.out.println(b.solution("{[()()]}")); 
        System.out.println(b.solution("{[()(]}")); 
        System.out.println(b.solution2("{[()()]}")); 
        System.out.println(b.solution2("{[()(]}")); 
    }
}

