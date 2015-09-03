/*
 *
 * You are given integers K, M and a non-empty zero-indexed array A consisting of N integers. Every element of the array is not greater than M.
 * 
 * You should divide this array into K blocks of consecutive elements. The size of the block is any integer between 0 and N. Every element of the array should belong to some block.
 * 
 * The sum of the block from X to Y equals A[X] + A[X + 1] + ... + A[Y]. The sum of empty block equals 0.
 * 
 * The large sum is the maximal sum of any block.
 * 
 * For example, you are given integers K = 3, M = 5 and array A such that:
 * 
 *   A[0] = 2
 *   A[1] = 1
 *   A[2] = 5
 *   A[3] = 1
 *   A[4] = 2
 *   A[5] = 2
 *   A[6] = 2
 * The array can be divided, for example, into the following blocks:
 * 
 * [2, 1, 5, 1, 2, 2, 2], [], [] with a large sum of 15;
 * [2], [1, 5, 1, 2], [2, 2] with a large sum of 9;
 * [2, 1, 5], [], [1, 2, 2, 2] with a large sum of 8;
 * [2, 1], [5, 1], [2, 2, 2] with a large sum of 6.
 * The goal is to minimize the large sum. In the above example, 6 is the minimal large sum.
 * 
 * Write a function:
 * 
 * class Solution { public int solution(int K, int M, int[] A); }
 * 
 * that, given integers K, M and a non-empty zero-indexed array A consisting of N integers, returns the minimal large sum.
 * 
 * For example, given K = 3, M = 5 and array A such that:
 * 
 *   A[0] = 2
 *   A[1] = 1
 *   A[2] = 5
 *   A[3] = 1
 *   A[4] = 2
 *   A[5] = 2
 *   A[6] = 2
 * the function should return 6, as explained above.
 * 
 * Assume that:
 * 
 * N and K are integers within the range [1..100,000];
 * M is an integer within the range [0..10,000];
 * each element of array A is an integer within the range [0..M].
 * Complexity:
 * 
 * expected worst-case time complexity is O(N*log(N+M));
 * expected worst-case space complexity is O(1), beyond input storage (not counting the storage required for input arguments).
 */
import java.util.*;
public class MinMaxDivision{
    public int blocksNo(int[] A, maxblock){
        int blockNo = 1; 
        int preBlockSum = A[0]; 
        for (int i = 1 ; i < A.length; ++){
            int e = A[i]; 
            if (preBlockSum + e > maxblock){
                preBlockSum = e; 
                blockNo += 1; 
            }
            else{
                preBlockSum += e; 
            }
        }
        return blockNo; 
    }

    public int solution(int K, int M, int[] A){
        int blockNeeded = 0; 
        int upper, lower; 
        upper = 0; 
        lower = 0; 
        int result = 0; 
        for ( int i = 0 ; i < A.length ;i++){
            lower = lower > A[i] ? lower : A[i]; 
            upper += A[i]; 
        }
        
        if ( K == 1 ){
            return upper; 
        }
        else if ( K == A.length ){
            return lower; 
        }
        
        while (lower <= upper ){
            int mid = (lower + upper) / 2; 
            blockNeeded = this.blocksNo(A, mid); 
            if ( blockNeeded <= K ){
                upper = mid - 1; 
                result = mid; 
            }
            else{
                lower = mid + 1; 
            }
        }
        return result; 
    }

    public static void main(String[] args){
        MinMaxDivision d = new MinMaxDivision(); 
        d.solution(new int[] {2, 1, 5, 1, 2, 2, 2} ); 
    }
}
