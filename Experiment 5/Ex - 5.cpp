// Aim : Implement Quick Sort, a Divide and Conquer algorithm, to sort an array, arr[] in ascending order.

class Solution {
  public:
    void quickSort(vector<int>& arr, int low, int high) {
        if(low >= high) return;
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }

  public:
    int partition(vector<int>& arr, int low, int high) {
        int pivot = arr[high];
        int i = low;
        int j = high-1;
        while(i <= j) {
            while(arr[i] <= pivot && i <= high - 1) {
                i++;
            }
            while(arr[j] > pivot && j >= low) {
            j--;
            }
            if(i < j) {
                swap(arr[i], arr[j]);
            }
        }
        swap(arr[i], arr[high]);
        return i;
    }
};
