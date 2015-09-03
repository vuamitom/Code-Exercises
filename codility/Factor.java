/*
 * find all factors of N 
 */ 

public class Factor {
    public int solution(int N) {
        // write your code in Java SE 8
        int i = 0; int c = 0; 
        for(i = 1; i * i < N; i++){
            if ( N % i == 0) c += 2; 
        }
        if ( i * i == N ) c += 1; 
        return c;
    }
}
