def parse_int(string):
    end = 0

    for letter in string:
        if letter in "0123456789":
            end += 1
        else:
            break

    # TODO raise expection if no digits found
    # if end == 0:
    #     raise error
    return string[:end]
