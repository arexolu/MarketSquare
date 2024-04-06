import re

STRONG_PASSWORD_PATTERN = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$"

def is_strong_password(password: str) -> bool:
    pattern: re.Pattern[str] = re.compile(STRONG_PASSWORD_PATTERN)
    return pattern.match(password)