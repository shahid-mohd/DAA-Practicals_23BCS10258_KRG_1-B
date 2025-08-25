/*Aim: Analyze if the stack is empty or full, and if elements are present, 
return the top element in the stack using templates. 
Also, perform push and pop operations on the stack.*/

#include <iostream>
using namespace std;

template <typename T>
class Stack {
private:
    int topIndex;
    int capacity;
    T* arr;

public:
    Stack(int size) {
        capacity = size;
        arr = new T[capacity];
        topIndex = -1;
    }

    ~Stack() {
        delete[] arr;
    }

    bool isEmpty() const {
        return topIndex == -1;
    }

    bool isFull() const {
        return topIndex == capacity - 1;
    }

    void push(T value) {
        if (isFull()) {
            cout << "Stack Overflow! Cannot push " << value << endl;
        } else {
            arr[++topIndex] = value;
            cout << value << " pushed to stack." << endl;
        }
    }

    void pop() {
        if (isEmpty()) {
            cout << "Stack Underflow! Cannot pop." << endl;
        } else {
            cout << arr[topIndex--] << " popped from stack." << endl;
        }
    }

    bool top(T& value) const {
        if (isEmpty()) return false;
        value = arr[topIndex];
        return true;
    }
};

int main() {
    Stack<int> st(5);
    st.push(10);
    st.push(20);
    st.push(30);
    int val;
    if (st.top(val)) cout << "Top element: " << val << endl;
    st.pop();
    if (st.top(val)) cout << "Top element after pop: " << val << endl;
    st.push(40);
    st.push(50);
    st.push(60);
    st.push(70);
    while (!st.isEmpty()) {
        if (st.top(val)) cout << "Popping: " << val << endl;
        st.pop();
    }
    if (st.top(val)) cout << val << endl;
    else cout << "Stack is empty!" << endl;
    return 0;
}
