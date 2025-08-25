/*  Aim : Apply the concept of Linked list and write code to Insert and Delete an element
at the beginning and end in Doubly and Circular Linked List. */

#include <iostream>
using namespace std;

class Node {
public:
    int data;
    Node* prev;
    Node* next;
    Node(int val) {
        data = val;
        prev = NULL;
        next = NULL;
    }
};

class DLinkedList {
    Node* head;
public:
    DLinkedList() { head = NULL; }

    void insertFront(int val) {
        Node* node = new Node(val);
        if (!head) { head = node; cout << val << " inserted at front in Doubly Linked List\n"; return; }
        node->next = head;
        head->prev = node;
        head = node;
        cout << val << " inserted at front in Doubly Linked List\n";
    }

    void insertBack(int val) {
        Node* node = new Node(val);
        if (!head) { head = node; cout << val << " inserted at back in Doubly Linked List\n"; return; }
        Node* temp = head;
        while (temp->next) temp = temp->next;
        temp->next = node;
        node->prev = temp;
        cout << val << " inserted at back in Doubly Linked List\n";
    }

    void deleteFront() {
        if (!head) { cout << "Doubly Linked List is empty, nothing to delete from front\n"; return; }
        Node* temp = head;
        cout << temp->data << " deleted from front in Doubly Linked List\n";
        head = head->next;
        if (head) head->prev = NULL;
        delete temp;
    }

    void deleteBack() {
        if (!head) { cout << "Doubly Linked List is empty, nothing to delete from back\n"; return; }
        Node* temp = head;
        while (temp->next) temp = temp->next;
        cout << temp->data << " deleted from back in Doubly Linked List\n";
        if (temp->prev) temp->prev->next = NULL;
        else head = NULL;
        delete temp;
    }

    void show() {
        Node* temp = head;
        cout << "Doubly LL: ";
        while (temp) {
            cout << temp->data << " ";
            temp = temp->next;
        }
        cout << endl;
    }
};

class CLinkedList {
    Node* head;
public:
    CLinkedList() { head = NULL; }

    void insertFront(int val) {
        Node* node = new Node(val);
        if (!head) { head = node; head->next = head; cout << val << " inserted at front in Circular Linked List\n"; return; }
        Node* last = head;
        while (last->next != head) last = last->next;
        last->next = node;
        node->next = head;
        head = node;
        cout << val << " inserted at front in Circular Linked List\n";
    }

    void insertBack(int val) {
        Node* node = new Node(val);
        if (!head) { head = node; head->next = head; cout << val << " inserted at back in Circular Linked List\n"; return; }
        Node* last = head;
        while (last->next != head) last = last->next;
        last->next = node;
        node->next = head;
        cout << val << " inserted at back in Circular Linked List\n";
    }

    void deleteFront() {
        if (!head) { cout << "Circular Linked List is empty, nothing to delete from front\n"; return; }
        if (head->next == head) { 
            cout << head->data << " deleted from front in Circular Linked List\n";
            delete head; head = NULL; return; 
        }
        Node* temp = head;
        Node* last = head;
        while (last->next != head) last = last->next;
        head = head->next;
        last->next = head;
        cout << temp->data << " deleted from front in Circular Linked List\n";
        delete temp;
    }

    void deleteBack() {
        if (!head) { cout << "Circular Linked List is empty, nothing to delete from back\n"; return; }
        if (head->next == head) { 
            cout << head->data << " deleted from back in Circular Linked List\n";
            delete head; head = NULL; return; 
        }
        Node* temp = head;
        while (temp->next->next != head) temp = temp->next;
        Node* del = temp->next;
        cout << del->data << " deleted from back in Circular Linked List\n";
        temp->next = head;
        delete del;
    }

    void show() {
        if (!head) { cout << "Circular LL: empty\n"; return; }
        Node* temp = head;
        cout << "Circular LL: ";
        do {
            cout << temp->data << " ";
            temp = temp->next;
        } while (temp != head);
        cout << endl;
    }
};

int main() {
    DLinkedList dlist;
    dlist.insertFront(11);
    dlist.insertBack(25);
    dlist.insertFront(6);
    dlist.show();
    dlist.deleteFront();
    dlist.deleteBack();
    dlist.show();

    CLinkedList clist;
    clist.insertFront(15);
    clist.insertBack(30);
    clist.insertFront(7);
    clist.show();
    clist.deleteFront();
    clist.deleteBack();
    clist.show();
    return 0;
}
