import string
import random

# Adapted from: http://davidsj.co.uk/blog/python-generate-random-password-strings/
def random_string(size=12, with_special_chars=False) -> str:
    """Create and return a random string of given length

    Args:
        size (int): Length of string
        with_special_chars (bool): Use special chars in the string

    Returns:
        str: The random string
    """
    # Just alphanumeric characters
    chars = string.ascii_letters + string.digits
    if with_special_chars is True:
        # + special characters
        chars += string.punctuation
    return "".join((random.choice(chars)) for x in range(size))
