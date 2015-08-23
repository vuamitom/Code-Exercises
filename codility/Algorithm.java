import java.util.*; 

public class Algorithm{
    public static void main(String[] args){
        String[] test = {"hell", "bent", "on", "animation"};
        List<String> params = Arrays.asList(test); 
        Collections.sort(params);
        System.out.println(params); 

        Collections.shuffle(params); 
        System.out.println(params); 
        
        Collections.reverse(params); 
        System.out.println(params); 

        //Collections.addAll(params, new String[]{"Hell", "home"}); 
        Collections.addAll(params, new String[]{"hell", "home"}); 
        System.out.println(params); 
    }
}
