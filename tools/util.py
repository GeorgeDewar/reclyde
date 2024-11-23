def read_word(data, location):
    return int.from_bytes(data[location:location+2], 'little')

def write_word(value):
    return int.to_bytes(value, 2, 'little')
