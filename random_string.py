import random
import string

def get_random_string(length):

    characters = string.ascii_letters + string.digits
    result = ''.join(random.choice(characters) for i in range(length))
    return result
