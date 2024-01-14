# Random id with nanoid
from nanoid import generate

def generate_id():
    return generate()

def generate_code():
    return generate('1234567890ABCDEF', 10)

