"""
https://open.kattis.com/problems/orders
A program that uses dynamic programming to solve a variation of the knapsack problem.
"""


# This function is called whenever we have a total order price that can be made by combining the price of two or more
# (not necessarily distinct) items together
# This is necessary to prevent the program from treating permutations of the same numbers as distinct sums
# (e.g., 4 + 5 and 5 + 4 should be treated as the same sum)
def non_empty_sum_test(current_item_price, current_index):
    # Create a temporary list to compare to the sublist at the current index of our list of sums
    # The new_temp_list will be a copy of the (current_index - X)th sublist, with 1 added to the index corresponding to
    # the current menu item
    new_temp_list = list_of_ways_to_sum[current_index - current_item_price][:]
    new_temp_list[item_price_list.index(current_item_price)] += 1

    # If we've already found a different and distinct way to sum items up to make this sum (tested by comparing it to
    # the 0th index of our main list, which is always full of 0's), we know that there are at least two ways to sum
    # items up to make an order of that price
    if list_of_ways_to_sum[current_index] != list_of_ways_to_sum[0] and \
            new_temp_list != list_of_ways_to_sum[current_index]:
        list_of_ways_to_sum[current_index] = 'Ambiguous'

    # Otherwise, if our menu item costs X, and we could sum items up to make (current_index - X) in any one way, we can
    # just add one more of these menu items to trivially sum up to make current_index
    else:
        list_of_ways_to_sum[current_index] = list_of_ways_to_sum[current_index - current_item_price][:]
        list_of_ways_to_sum[current_index][item_price_list.index(current_item_price)] += 1


# Take an input first to get the amount of items on the menu
# We don't need to save this input, since we will always get that many values in the next line of input
input()
item_price_input = input()
item_price_list = item_price_input.split(' ')
item_price_list = [int(price) for price in item_price_list]

# Take an input again to get the amount of orders placed
# Again, we don't need to save this input, since we will always get that many values in the next line of input
input()
order_total_price_input = input()
order_total_price_list = order_total_price_input.split(' ')
order_total_price_list = [int(price) for price in order_total_price_list]

largest_price = max(order_total_price_list)

# For each number from 0 to the cost of our largest order, we're going to create a sublist inside of our main list with
# a 0 in every index (with one index for each menu item)
# We'll use this to represent how many copies of each menu item sum up to a given price
list_of_ways_to_sum = [[0 for item in item_price_list] for price in range(largest_price + 1)]

for price_sum in range(largest_price + 1):
    # For each sublist we create, we compare it to all of our menu items that are not cheaper than the index of that
    # sublist
    for menu_item in [item for item in item_price_list if price_sum >= item]:
        # If our menu item costs X, and we could sum items up to make (price_sum - X) in more than one way, we know
        # that we can sum items up to make price_sum in more than one way
        if list_of_ways_to_sum[price_sum - menu_item] == 'Ambiguous':
            list_of_ways_to_sum[price_sum] = 'Ambiguous'

        # If the (price_sum - X)th sublist is all zeros (i.e., we could not sum up to that calue in any way), we
        # ignore this block of code
        # Otherwise, we run the non-empty sum test function on it to determine how to fill the Xth sublist
        elif list_of_ways_to_sum[price_sum - menu_item] != list_of_ways_to_sum[0]:
            non_empty_sum_test(menu_item, price_sum)

        # When price_sum reaches the index of one of our menu items, we know that we can trivially sum up to that price
        # with one item
        elif price_sum == menu_item:

            # If we've already found a different way to sum items up to make price_sum, we know that there are at least
            # two ways to sum items up to make an order of that price
            if list_of_ways_to_sum[price_sum] != list_of_ways_to_sum[0]:
                list_of_ways_to_sum[price_sum] = 'Ambiguous'

            # Otherwise, we set the index of our sublist corresponding with that menu item to 1
            else:
                list_of_ways_to_sum[price_sum][item_price_list.index(menu_item)] += 1


# Once we've built our list of ways to sum up to every needed price, we check the values for the order prices we've
# been given
for orderPrice in order_total_price_list:
    # If the element in our list corresponding to the current order's price is a sublist of only 0's, that means there
    # was no way to sum up our menu items to make an order of that price
    if list_of_ways_to_sum[orderPrice] == list_of_ways_to_sum[0]:
        print("Impossible")

    # If the element in our list corresponding to the current order's price is the string 'ambiguous', that means there
    # was more than one way to sum up our menu items to make an order of that price
    elif list_of_ways_to_sum[orderPrice] == 'Ambiguous':
        print("Ambiguous")

    # Otherwise, we know the one way to sum items up to make the current order's price
    else:
        sumToPrint = ''
        # For each item in our sublist, we add the item's index (and a space) to our string as many times as it appears
        # in the sublist (including 0)
        for menuItemIndex, item in enumerate(list_of_ways_to_sum[orderPrice]):
            sumToPrint += (str(menuItemIndex + 1) + ' ') * item
        print(sumToPrint.rstrip())
