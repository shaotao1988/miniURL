import string

def shorten_URL(id :int):
    base62 = string.digits+string.ascii_letters
    shortURL = []
    if id == 0:
        shortURL.append(base62[0])
    while id > 0:
        remainder = id % 62
        id = id // 62
        shortURL.append(base62[remainder])
    
    shortURL.reverse()
    print(shortURL)

    return ''.join(shortURL)

def unshorten_URL(shortURL):
    if not shortURL:
        raise ValueError
    base62 = string.digits+string.ascii_letters
    id = 0
    length = len(shortURL)
    for i, ch in enumerate(shortURL):
        index = base62.index(ch)
        id += index*62**(length-i-1)
    return id
