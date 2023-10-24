def flat_generaotor(list):

    list = [element for lists in list for element in lists]
    count = 0
    while count < len(list):
        yield list[count]
        count += 1