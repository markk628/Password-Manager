import string
import random

def generate_password():
  chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
  size = random.randint(8, 12)
  return ''.join(random.choice(chars) for x in range(size))

generate_password()