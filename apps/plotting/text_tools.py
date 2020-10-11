# Functions included in this file:
# # word_wrap

def word_wrap(string, n):
    string_list = string.split()
    parsed_list = [string_list[n * i:n * (i + 1)] for i in range((len(string_list) + n - 1) // n)]
    joined_string_list = [' '.join(parsed_list[i]) for i in range(len(parsed_list))]
    final_list = ['<br>'.join(joined_string_list)]
    return final_list[0]
