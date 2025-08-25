// Aim : Code to find frequency of elements in a given array in O(n) time complexity.

class Solution {
  public:
    vector<vector<int>> countFreq(vector<int>& arr) {
        unordered_map <int,int> m;
        for( auto i: arr){
            m[i]++;
        }
        vector<vector<int>> res;
        for(auto i:m){
            res.push_back({i.first,i.second});
        }
        return res;
    }
};
