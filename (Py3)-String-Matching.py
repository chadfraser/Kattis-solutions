"""
https://open.kattis.com/problems/stringmatching
A program to find all of the occurrences of a substring in a longer string.
"""

import sys


# Constructing a table of partial matches to use in the KMP algorithm
def construct_partial_match_table(pattern):
    string_length = len(pattern)
    current_prefix_length = 0

    # Initialize the table of partial matches to have 0 at all indices
    partial_match_table = [0] * string_length

    if string_length == 1:
        return partial_match_table

    # Iterate through every character in the pattern to check the partial suffixes at different points in the pattern
    # We start at index 1 because at index 0, there is trivially no possible partial suffix
    for current_index, current_char in enumerate(pattern[1:], 1):
        # If we had a partial suffix that matched a proper prefix, but the next character in our string breaks the
        # match, our maximum possible partial match length is the value of our table at the previous index (our most
        # recent match)
        # We reiterate this until the character we now point to matches our current character (or the prefix length is
        # 0, which means there is no partial match at this index)
        while current_prefix_length > 0 and pattern[current_prefix_length] != current_char:
            current_prefix_length = partial_match_table[current_prefix_length - 1]

        if pattern[current_prefix_length] == current_char:
            current_prefix_length += 1
        partial_match_table[current_index] = current_prefix_length
    return partial_match_table


# The Knuth-Morris-Pratt algorithm for string matching
def kmp_string_search(given_string, pattern):
    # Create a table of partial matches to use in the KMP search algorithm
    table = construct_partial_match_table(pattern)
    given_string_length = len(given_string)
    pattern_length = len(pattern)

    index_to_begin_search = 0
    given_index = 0
    pattern_index = 0
    locations_of_matches = []

    # Iterate through every character of the string we wish to check
    while given_string_length - index_to_begin_search > pattern_length:
        # While the current character in our substring and given string match, increment each by 1 to compare the next
        # characters (unless we reach the end of the string)
        while pattern_index < pattern_length and given_string[given_index] == pattern[pattern_index]:
            given_index += 1
            pattern_index += 1

        # pattern_index only increments while
        # substring[0:pattern_index] == given_string[index_to_begin_search:given_index]
        # So if pattern_index reaches the length of the substring, we know we've found a match for the entire substring
        if pattern_index >= pattern_length:
            locations_of_matches.append(str(index_to_begin_search))

        # We check the value in our partial match table for the most recent match we've found.
        # If this match is anywhere beyond the beginning of our string, given_index stays the same,
        # pattern_index takes this value, and index_to_begin_search intuitively becomes the difference in these numbers
        if pattern_index > 0 and table[pattern_index - 1] > 0:
            index_to_begin_search = given_index - table[pattern_index - 1]
            pattern_index = table[pattern_index - 1]

        # If this match is at the beginning of our string and we have not matched any characters in our substring at
        # the current index_to_begin_search, we increment our given_index by 1 to start searching there.
        # In any case, we update our index_to_begin_search and our pattern_index (if it's not already at the start of
        # our substring)
        else:
            if given_index == index_to_begin_search:
                given_index += 1
            index_to_begin_search = given_index
            if pattern_index > 0:
                pattern_index = table[pattern_index - 1]

    # Our code only recognizes 'finding' a substring match when we increment pattern_index beyond the length of the
    # substring, and this cannot happen once we reach the end of our given string
    # To account for this, we simply separately check if the very end of our given string matches our substring
    if given_string[-pattern_length:] == pattern:
        locations_of_matches.append(str(len(given_string) - pattern_length))
    print(' '.join(locations_of_matches))


# Initialize all of the boolean and string variables we'll use during our test
string_to_check = ''
pattern_to_check = ''
check_ready = False

# Read each line independently from the stdin
# On odd numbered lines, we're given the pattern to check for
# On even numbered lines, we're given the string to check
for line in sys.stdin:
    if not check_ready:
        pattern_to_check = line.rstrip('\n')
        check_ready = True
    else:
        string_to_check = line.rstrip('\n')
        check_ready = False
        kmp_string_search(string_to_check, pattern_to_check)
