import random


def random_number() -> int:
    """Generate and return a 6 digit random integer

    Returns:
        int: A random integer
    """
    return random.randint(100000, 999999)
