/***
 *
 * A non-empty zero-indexed array A consisting of N integers is given.
 * 
 * The leader of this array is the value that occurs in more than half of the elements of A.
 * 
 * An equi leader is an index S such that 0 ≤ S < N − 1 and two sequences A[0], A[1], ..., A[S] and A[S + 1], A[S + 2], ..., A[N − 1] have leaders of the same value.
 * 
 * For example, given array A such that:
 * 
 *     A[0] = 4
 *     A[1] = 3
 *     A[2] = 4
 *     A[3] = 4
 *     A[4] = 4
 *     A[5] = 2
 * we can find two equi leaders:
 * 
 * 0, because sequences: (4) and (3, 4, 4, 4, 2) have the same leader, whose value is 4.
 * 2, because sequences: (4, 3, 4) and (4, 4, 2) have the same leader, whose value is 4.
 * The goal is to count the number of equi leaders.
 * 
 * Write a function:
 * 
 * int solution(int A[], int N);
 * 
 * that, given a non-empty zero-indexed array A consisting of N integers, returns the number of equi leaders.
 * 
 * For example, given:
 * 
 *     A[0] = 4
 *     A[1] = 3
 *     A[2] = 4
 *     A[3] = 4
 *     A[4] = 4
 *     A[5] = 2
 * the function should return 2, as explained above.
 * 
 * Assume that:
 * 
 * N is an integer within the range [1..100,000];
 * each element of array A is an integer within the range [−1,000,000,000..1,000,000,000].
 * Complexity:
 * 
 * expected worst-case time complexity is O(N);
 * expected worst-case space complexity is O(N), beyond input storage (not counting the storage required for input arguments).
 * Elements of input arrays can be modified
 */
import java.util.*;
public class EquiLeader {
    public int solution(int[] A) {
        // write your code in Java SE 8
        // equileader must be a leader 
        int leader = this.leader(A); 
        if(leader == -1){
            return 0; 
        }
        else{
            int val = A[leader];
            int count = 0; 
            for(int i = 0 ; i < A.length ;i++){
                if (A[i] == val){
                    count++; 
                }
            }
            int sofar = 0; 
            int equi = 0; 

            for (int i = 0 ; i < A.length ;i++){
                if(A[i] == val){
                    sofar ++;    
                }
                if(sofar > (i + 1)/2 && (count -sofar) > (A.length - i - 1) /2){
                    equi ++; 
                }
            }
            return equi; 
        }
    }
     
    public int leader(int[] A){
        int size, value; 
        size = 0; 
        value = 0;  
        for( int i = 0 ; i < A.length ; i++){
           if (size == 0) {
               value = A[i];
               size ++;          
           }
           else{
                if (value != A[i]){
                    size --; 
                }
                else{
                    size ++; 
                }
           }
        }
        
        if (size > 0){
            size = 0; 
            int candidate = -1; 
            for (int i = 0; i < A.length; i++){
                if (A[i] == value){
                    size++;    
                    candidate = i; 
                }
            }
            if (size > A.length / 2){
                return candidate;
            }
        }
        return -1;
    }

    public static void main(String[] args){
        EquiLeader el = new EquiLeader(); 
        System.out.println(el.solution(new int[]{4,3,4,4,4,2}));
    }
}
