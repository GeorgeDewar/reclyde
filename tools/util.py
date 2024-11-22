def read_word(data, location):
    return int.from_bytes(data[location:location+2], 'little')
