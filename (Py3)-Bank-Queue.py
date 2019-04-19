"""
https://open.kattis.com/problems/bank
A program to find the most money you can get from customers that must be served before various times.
"""


customer_dict = {}
possible_money_to_collect = []
total_sum = 0

initial_input = input()
initial_input_list = initial_input.split(' ')
amount_people_in_queue = int(initial_input_list[0])
time_until_close = int(initial_input_list[1])

# Take in N more inputs, where N is the number of people in the queue
# Split each input into two variables: Money that customer n has to deposit, and time they'll wait until leaving
for customer in range(amount_people_in_queue):
    current_line_input = input()
    current_line_list = current_line_input.split(' ')
    money_to_deposit = int(current_line_list[0])
    time_until_leave = int(current_line_list[1])
    # Group each customer who will wait t minutes into one list, storing the money that each of those customers
    # has to deposit
    customer_dict.setdefault(time_until_leave, []).append(money_to_deposit)

# We can take in T customers, where T is the time we have until closing
for time in range(time_until_close)[::-1]:
    # For each element in the customer_dict for time t, add that element to our possible_money_to_collect list
    if time in customer_dict.keys():
        for money in customer_dict[time]:
            possible_money_to_collect.append(money)
        # After filling our possible_money_to_collect list, take the maximum element from it and add it to our
        # total_sum: This is the most money we can take as late as time t
        if possible_money_to_collect:
            total_sum += max(possible_money_to_collect)
            possible_money_to_collect.remove(max(possible_money_to_collect))

# After iterating through every minute the bank is open, we have our greedy solution
print(total_sum)
