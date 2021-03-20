REQUIRED_KEYS = {"CALL", "PLACE", "ADDR", "CITY", "INFO"}


def parse_email(email: str):
    """Converts email body of value pairs into dictionary

    Args:
        email (str): email body in the Cadpage format
    """
    result = email.splitlines()
    result = [line for line in result if ":" in line]
    result = [line.split(":") for line in result]
    # the fanciness with the join is in case the message has colons in it
    result = {line[0].strip(): ":".join(line[1:]).strip() for line in result}
    # make sure the required keys exist so the format is correct
    if not REQUIRED_KEYS.issubset(result.keys()):
        raise ValueError(
            f"Email is missing essential fields. found {result.keys()} expecting {REQUIRED_KEYS}"
        )

    return result
