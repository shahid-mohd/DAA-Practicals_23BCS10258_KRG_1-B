// Aim : Code implement power function in O(logn) time complexity.

class Solution {
public:
    double myPow(double x, long n) {
        if(n < 0) {
            x = 1/x;
            n = -n;
        }
        double res = 1;
        while(n > 0) {
            if(n & 1) {
                res = res * x;
            }
            x = x * x;
            n = n >> 1;
        }
        return res;
    }
};
