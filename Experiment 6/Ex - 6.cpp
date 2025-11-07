// Aim : Given an array of positive integers arr[] and a value sum, determine if there is a subset of arr[] with sum equal to given sum. 

class Solution {
public:
    vector<vector<int>> dp;
    
    int subsetSum(int i, int target, vector<int>& arr) {
        if (target == 0) return 1;
        if (i == arr.size() - 1) return arr[i] == target;

        if (dp[i][target] != -1) return dp[i][target];

        int notPick = subsetSum(i + 1, target, arr);
        int pick = 0;
        if (arr[i] <= target)
            pick = subsetSum(i + 1, target - arr[i], arr);

        return dp[i][target] = (pick || notPick);
    }
    
    bool isSubsetSum(vector<int>& arr, int sum) {
        int n = arr.size();
        dp.assign(n, vector<int>(sum + 1, -1));
        return subsetSum(0, sum, arr);
    }
};
