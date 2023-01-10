def check_if_all_lists_have_same_length(list_of_lists):
    return len(set(len(x) for x in list_of_lists if isinstance(x, list))) == 1


mylist = [[1, 2, 3], [4, 5, 6], [7, 8, 9], "asdfasdf", 32134123]
print(check_if_all_lists_have_same_length(mylist))
