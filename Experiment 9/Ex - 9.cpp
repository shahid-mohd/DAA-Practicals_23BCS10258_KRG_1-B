// Aim : Search Pattern

class Solution {
public:
    vector<int> search(string &pat, string &txt) {
        vector<int> res;
        string s = pat + "$" + txt;
        int n = s.length();
        vector<int> lps(n, 0);
        int l = 0, i = 1;
        while (i < n) {
            if (s[i] == s[l]) {
                l++;
                lps[i] = l;
                i++;
            } else {
                if (l != 0) l = lps[l - 1];
                else {
                    lps[i] = 0;
                    i++;
                }
            }
        }
        for (int i = 0; i < n; i++) {
            if (lps[i] == pat.size()) res.push_back(i - 2 * pat.size());
        }
        return res;
    }
};
