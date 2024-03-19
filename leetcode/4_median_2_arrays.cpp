class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        if (nums1.size() > nums2.size()) {
            swap(nums1, nums2);
        }
        
        int m = nums1.size();
        int n = nums2.size();
        int left = 0, right = m, half_len = (m + n + 1) / 2;
        
        while (left <= right) {
            int partition1 = (left + right) / 2;
            int partition2 = half_len - partition1;
            
            int max_left1 = (partition1 == 0) ? INT_MIN : nums1[partition1 - 1];
            int min_right1 = (partition1 == m) ? INT_MAX : nums1[partition1];
            
            int max_left2 = (partition2 == 0) ? INT_MIN : nums2[partition2 - 1];
            int min_right2 = (partition2 == n) ? INT_MAX : nums2[partition2];
            
            if (max_left1 <= min_right2 && max_left2 <= min_right1) {
                if ((m + n) % 2 == 0) {
                    return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0;
                } else {
                    return max(max_left1, max_left2);
                }
            } else if (max_left1 > min_right2) {
                right = partition1 - 1;
            } else {
                left = partition1 + 1;
            }
        }
        
        // This should never be reached if the input arrays are sorted correctly.
        throw invalid_argument("Input arrays are not sorted.");
    }
};