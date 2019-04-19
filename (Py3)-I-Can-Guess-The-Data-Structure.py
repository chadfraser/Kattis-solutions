"""
https://open.kattis.com/problems/guessthedatastructure
A program to determine whether user input is imitating a stack, a queue, or a priority queue.
"""

from collections import deque
import sys

# Initialize all of the boolean variables and data structures we'll use during our tests
int_to_check = 0
stack_test_list = []
queue_test_list = deque([])
priority_test_list = []
is_boolean_possible = could_be_stack = could_be_queue = could_be_priority = True

for line in sys.stdin:
    # Check if the string has a space in it
    # If it doesn't, this should be the line that tells you how many test cases we'll need to check
    if " " not in line:
        int_to_check = int(line)

    # If the string doesn't have a space in it, it should be the line that gives us an operation and a value
    else:
        value_string = line.split(" ")
        integer_value = int(value_string[1])

        # If the string starts with a "1" (i.e., addition command), add the end of the string to each of our tests
        if value_string[0] == "1":
            stack_test_list.append(integer_value)
            queue_test_list.append(integer_value)
            priority_test_list.append(integer_value)
            int_to_check -= 1

        else:
            # If the passed value is not in any of our test structures, we know that it is an impossible request
            if not any([integer_value in stack_test_list, integer_value in queue_test_list, integer_value in
                        priority_test_list]):
                is_boolean_possible = False
            else:
                if could_be_priority:
                    # If the largest element of the list does not match the removed value, it can't be a priority queue
                    # After checking, remove that element from the priority queue test list (if it exists there)
                    if max(priority_test_list) != integer_value:
                        could_be_priority = False
                    if integer_value in priority_test_list:
                        priority_test_list.remove(integer_value)

                if could_be_queue:
                    # If the first element of the list does not match the removed value, it cannot be a queue
                    # In checking, remove the first element from the queue test deque
                    if queue_test_list.popleft() != integer_value:
                        could_be_queue = False

                if could_be_stack:
                    # If the last element of the list does not match the removed value, it cannot be a stack
                    # In checking, remove the last element from the stack test list
                    if stack_test_list.pop() != integer_value:
                        could_be_stack = False
            int_to_check -= 1

    # Each time we've checked all the test cases we were told to check, return our answer
    if int_to_check == 0:
        # If the user tried to remove an element that was not in the list, or our program returned 'False' on all of
        # the data structures (i.e., it breaks the rules of queues, stacks, and priority queues), print 'impossible'
        if not is_boolean_possible or sum([could_be_stack, could_be_queue, could_be_priority]) == 0:
            print("impossible")
        # If more than one of the possible data structures returned 'True' from our program, print 'not sure'
        elif sum([could_be_stack, could_be_queue, could_be_priority]) > 1:
            print("not sure")
        # Otherwise, print whatever data structure matched our program
        elif could_be_stack:
            print("stack")
        elif could_be_queue:
            print("queue")
        else:
            print("priority queue")

        # Reset the test values to their initial values
        stack_test_list = []
        queue_test_list = deque([])
        priority_test_list = []
        is_boolean_possible = could_be_stack = could_be_queue = could_be_priority = True
